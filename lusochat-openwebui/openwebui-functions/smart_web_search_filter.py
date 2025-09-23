"""
id: smart_google_pse_web_search
title: Smart_Google_PSE_Web_Search
author: LusoChat
version: 0.1.0
license: MIT
description: Conditionally enable Web Search using Google PSE based on the user's query and simple heuristics (RAG-first). Supports modes: off, auto, always_on. Emits status events explaining the decision.
requirements:
  
Paste this into OpenWebUI > Admin Panel > Functions > New Function
Type: Filter
Purpose: Decide when to run Web Search (instead of always-on) and route through Google PSE configured in Settings.

Notes:
- Respects Admin > Settings > Web Search (Google PSE key + engine id). This filter only toggles when to search.
- In auto mode, it runs quick heuristics to avoid searches for common "local knowledge" questions (e.g., known contacts) and enables search for time-sensitive or policy/process queries.
- Emits a status event indicating skip/enable/cause so you can observe behavior in the stream.
- Optionally invokes OpenWebUI's built-in chat_web_search_handler to prefetch results when search is enabled.

Tested against OpenWebUI 0.3x APIs; adjust imports if upstream API changes.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, List, Tuple
from pydantic import BaseModel, Field
import re

try:
    # open-webui >= 0.3.8
    from open_webui.utils.middleware import chat_web_search_handler
    from open_webui.models.users import UserModel
except Exception:  # pragma: no cover
    # Fallback if imports move upstream.
    chat_web_search_handler = None
    UserModel = None


class Filter:
    """Smart Web Search controller for Google PSE in OpenWebUI.

    Modes:
    - off:      never enable search
    - always_on: always enable search (like the simple filter)
    - auto:     enable search only when the query likely needs fresh/external info
    """

    id = "smart_google_pse_web_search"
    name = "Smart_Google_PSE_Web_Search"
    description = (
        "Conditionally enable Web Search using Google PSE based on the user's query and simple heuristics. "
        "Supports modes: off, auto, always_on."
    )
    type = "filter"

    class Valves(BaseModel):
        status: bool = Field(
            default=True, description="Enable/disable this filter"
        )
        mode: str = Field(
            default="auto", description="off | auto | always_on"
        )
        prefetch: bool = Field(
            default=True,
            description="If True, proactively invoke chat_web_search_handler. If you observe duplicate fetches, set False and rely on pipeline.",
        )
        allow_rag_first: bool = Field(
            default=True,
            description="Prefer local/RAG knowledge first; in auto mode, skip search if query looks purely local",
        )
        min_chars_for_search: int = Field(
            default=12, description="Auto mode: minimum query length before considering web search"
        )
        aggressiveness: int = Field(
            default=0,
            description="Shift the decision score by this value (-2..+2 typical); higher = more searches",
        )
        force_threshold: int = Field(
            default=1,
            description="Minimum decision score to enable search in auto mode",
        )
        soften_skip_keywords: bool = Field(
            default=True,
            description="When True, skip keywords subtract from the score instead of blocking outright",
        )
        debug_decision: bool = Field(
            default=False,
            description="Emit extra status with scoring details and write web_search_reason to features",
        )
        # Gating and context awareness
        strict_domain_intent: bool = Field(
            default=True,
            description="Only enable search when query looks like institutional/resource-related (see resource/domain keywords)",
        )
        followup_cooldown_turns: int = Field(
            default=2,
            description="If recent assistant messages had links/citations, skip searches for this many turns on vague/anaphoric follow-ups",
        )
        penalize_anaphora: bool = Field(
            default=True,
            description="Reduce likelihood of search when the query is anaphoric/vague (e.g., 'e isso?', 'e quando?')",
        )
        # Keyword sets for gating
        resource_keywords: List[str] = Field(
            default_factory=lambda: [
                "candidatura",
                "candidaturas",
                "admissão",
                "admissao",
                "propina",
                "propinas",
                "prazo",
                "prazos",
                "calendário",
                "horário",
                "regulamento",
                "regulamentos",
                "bolsa",
                "bolsas",
                "serviços",
                "servicos",
                "curso",
                "cursos",
                "plano de estudos",
                "ects",
                "estatuto",
                "edital",
            ],
            description="Words that indicate the user is asking about institutional resources/processes",
        )
        domain_keywords: List[str] = Field(
            default_factory=lambda: [
                "lusófona",
                "lusofona",
                "universidade lusófona",
                "ulusofona",
                "ulusofona.pt",
            ],
            description="Domain/brand indicators for the institution",
        )
        chitchat_skip_keywords: List[str] = Field(
            default_factory=lambda: [
                "olá",
                "ola",
                "obrigado",
                "obrigada",
                "ok",
                "sim",
                "não",
                "nao",
                "bom dia",
                "boa tarde",
                "boa noite",
                "valeu",
            ],
            description="If a query is mostly chitchat and not resource-related, skip search",
        )
        # Dynamic result count by category
        result_count_simple: int = Field(
            default=2, description="Result count to request for simple/time-sensitive queries"
        )
        result_count_complex: int = Field(
            default=5, description="Result count to request for complex/broader queries"
        )
        result_count_default: int = Field(
            default=3, description="Result count to request when category is unclear"
        )
        force_keywords: List[str] = Field(
            default_factory=lambda: [
                # Portuguese/English time-sensitive or policy/process queries
                "agora",
                "hoje",
                "atualizado",
                "atualização",
                "prazo",
                "prazos",
                "deadline",
                "calendário",
                "horário",
                "propina",
                "propinas",
                "candidatura",
                "candidaturas",
                "inscrição",
                "inscrições",
                "regulamento",
                "regulamentos",
                "news",
                "novidade",
                "novidades",
                "ranking",
                "publicado",
                "edital",
                "bolsa",
                "bolsas",
                "apoio",
                "apoios",
                "resultado",
                "resultados",
                "202",
                "2024",
                "2025",
                "site",
                "website",
                "página",
                "páginas",
            ],
            description="If any of these appear, prefer enabling web search in auto mode",
        )
        skip_keywords: List[str] = Field(
            default_factory=lambda: [
                # Common "local facts" we likely have in RAG/system prompt
                "contacto",
                "contactos",
                "contact",
                "contacts",
                "email",
                "e-mail",
                "telefone",
                "telemóvel",
                "whatsapp",
                "morada",
                "endereço",
                "address",
                "extensão",
                "ramal",
                "número",
                "numero",
                "location",
                "localização",
                "onde fica",
            ],
            description="If these dominate the query, prefer skipping web search in auto mode",
        )
        force_if_user_requests_search: bool = Field(
            default=True,
            description="If user explicitly asks to search or reference web/google, force enable",
        )
        max_result_count_override: Optional[int] = Field(
            default=None,
            description="Optional override for search result count (if supported by current OpenWebUI build)",
        )

    def __init__(self):
        self.valves = self.Valves()

    # ---- helpers ----
    async def emit_status(
        self,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ) -> None:
        if self.valves.status:
            await __event_emitter__(
                {
                    "type": level,
                    "data": {
                        "description": message,
                        "done": done,
                    },
                }
            )

    def _get_last_user_text(self, body: dict) -> str:
        msgs = body.get("messages") or []
        for m in reversed(msgs):
            if (m.get("role") or "").lower() == "user":
                content = m.get("content")
                if isinstance(content, str):
                    return content
                try:
                    # Some UIs send content as [{type: 'text', text: '...'}]
                    if isinstance(content, list) and content and isinstance(content[0], dict):
                        return content[0].get("text", "") or ""
                except Exception:
                    pass
        return body.get("prompt") or ""

    def _contains_any(self, text: str, words: List[str]) -> int:
        if not text or not words:
            return 0
        score = 0
        lowered = text.lower()
        for w in words:
            try:
                if not w:
                    continue
                # whole word or substring match; keep simple
                if re.search(r"\b" + re.escape(w.lower()) + r"\b", lowered) or w.lower() in lowered:
                    score += 1
            except re.error:
                # If a valve value contains a bad regex fragment, ignore it
                if w.lower() in lowered:
                    score += 1
        return score

    def _user_requested_search(self, text: str) -> bool:
        if not text:
            return False
        triggers = [
            "pesquisa",
            "pesquisar",
            "procura",
            "procurar",
            "web",
            "google",
            "fonte",
            "fontes",
            "link",
            "links",
            "sítio",
            "site",
            "página",
        ]
        return self._contains_any(text, triggers) > 0

    def _get_last_assistant_text(self, body: dict) -> str:
        msgs = body.get("messages") or []
        for m in reversed(msgs):
            if (m.get("role") or "").lower() == "assistant":
                content = m.get("content")
                if isinstance(content, str):
                    return content
                try:
                    if isinstance(content, list) and content and isinstance(content[0], dict):
                        return content[0].get("text", "") or ""
                except Exception:
                    pass
        return ""

    def _recent_assistant_had_links(self, body: dict, within_turns: int) -> bool:
        msgs = body.get("messages") or []
        count = 0
        for m in reversed(msgs):
            role = (m.get("role") or "").lower()
            if role == "assistant":
                count += 1
                content = m.get("content")
                text = content if isinstance(content, str) else (
                    (content[0].get("text", "") if isinstance(content, list) and content and isinstance(content[0], dict) else "")
                )
                if any(s in (text or "") for s in ["http://", "https://", "Fonte", "Fontes"]):
                    return True
                if count >= within_turns:
                    break
        return False

    def _is_anaphoric(self, text: str) -> bool:
        t = (text or "").strip().lower()
        if not t:
            return False
        if len(t) < 10:
            return True
        return self._contains_any(
            t,
            [
                "e isto",
                "e isso",
                "e aquilo",
                "e quando",
                "e onde",
                "e como",
                "e mais",
                "e então",
                "e agora",
                "e depois",
            ],
        ) > 0

    def _has_institutional_intent(self, text: str) -> bool:
        t = (text or "").lower()
        resource = self._contains_any(t, self.valves.resource_keywords)
        domain = self._contains_any(t, self.valves.domain_keywords)
        # Consider intent present if either set is hit; stronger if both
        return (resource > 0) or (domain > 0)

    def _decide_auto(self, text: str, body: dict) -> Tuple[bool, str]:
        # Basic guardrails
        if not text:
            return False, "empty_text"
        if self.valves.force_if_user_requests_search and self._user_requested_search(text):
            return True, "user_requested_search"
        if self.valves.allow_rag_first and len(text.strip()) < self.valves.min_chars_for_search:
            return False, "too_short_rag_first"

        # Skip chitchat if not clearly resource-related
        if self._contains_any(text, self.valves.chitchat_skip_keywords) > 0 and not self._has_institutional_intent(text):
            return False, "chitchat_skip"

        # Enforce institutional intent if enabled
        if self.valves.strict_domain_intent and not self._has_institutional_intent(text):
            return False, "no_domain_intent"

        # Follow-up cooldown: if we recently provided links and this looks anaphoric/vague, skip
        if self.valves.followup_cooldown_turns > 0 and self._recent_assistant_had_links(body, self.valves.followup_cooldown_turns):
            if self.valves.penalize_anaphora and self._is_anaphoric(text):
                return False, "cooldown_followup"

        force_hits = self._contains_any(text, self.valves.force_keywords)
        skip_hits = self._contains_any(text, self.valves.skip_keywords)

        score = 0
        score += force_hits
        # Question cues
        score += self._contains_any(
            text,
            [
                "?",
                "como",
                "quando",
                "onde",
                "qual",
                "quais",
                "quem",
                "o que",
                "como faço",
                "como posso",
                "link",
                "site",
                "página",
            ],
        )
        # Years or numbers: often need verification
        if re.search(r"\b20\d{2}\b", text):
            score += 1
        if re.search(r"\b\d{4,}\b", text):
            score += 1
        # Handle two-digit year references like "25" when paired with specific domain terms
        if re.search(r"\b(24|25)\b", text) and self._contains_any(
            text,
            [
                "candidatura",
                "candidaturas",
                "prazo",
                "prazos",
                "calendário",
                "horário",
                "propina",
                "propinas",
                "regulamento",
            ],
        ):
            score += 1
        # Brand/domain terms: favor official sources
        score += self._contains_any(text, ["lusófona", "lusofona", "ulusofona", "universidade lusófona"]) 

        # Apply skip influence
        if self.valves.soften_skip_keywords:
            score -= skip_hits
        else:
            if skip_hits > 0 and force_hits == 0:
                return False, "skip_keywords_block"

        # History nudge: if last assistant had no links/citations and user asks again, search
        last_assistant = self._get_last_assistant_text(body)
        if last_assistant:
            has_link = ("http://" in last_assistant) or ("https://" in last_assistant) or ("Fonte" in last_assistant) or ("Fontes" in last_assistant)
            if not has_link:
                score += 1

        # Aggressiveness and final threshold
        score += int(self.valves.aggressiveness)
        enable = score >= int(self.valves.force_threshold)
        reason = f"score={score}, force={force_hits}, skip={skip_hits}, aggr={self.valves.aggressiveness}, thr={self.valves.force_threshold}"
        return enable, reason

    def _classify_category(self, text: str) -> Tuple[str, int]:
        """Classify query into simple/complex/default and pick a result count.

        - simple: time-sensitive or specific single-page answers (prazos, propinas, calendário, horário, regulamento), esp. with year cues
        - complex: broader program info (condições de entrada, requisitos, plano de estudos)
        - default: fallback
        """
        t = (text or "").lower()
        simple_hits = self._contains_any(
            t,
            [
                "prazo",
                "prazos",
                "propina",
                "propinas",
                "calendário",
                "horário",
                "regulamento",
                "taxa",
                "propinas 2025",
                "propinas 2024",
            ],
        )
        complex_hits = self._contains_any(
            t,
            [
                "condições de entrada",
                "condicoes de entrada",
                "requisitos",
                "admissão",
                "admissao",
                "critérios",
                "criterios",
                "plano de estudos",
                "currículo",
                "curriculo",
                "ects",
            ],
        )

        has_year = bool(re.search(r"\b20\d{2}\b", t)) or bool(re.search(r"\b(24|25)\b", t))

        if simple_hits > 0 and has_year:
            return "simple_recent", int(self.valves.result_count_simple)
        if simple_hits > 0 and complex_hits == 0:
            return "simple", int(self.valves.result_count_simple)
        if complex_hits > 0:
            return "complex", int(self.valves.result_count_complex)
        return "default", int(self.valves.result_count_default)

    # ---- filter hooks ----
    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        """Decide whether to enable web search and optionally prefetch using OpenWebUI's handler.

        Behavior by mode:
        - off:       leaves web_search untouched/False
        - always_on: sets web_search=True and prefetches
        - auto:      simple heuristics decide; in allow_rag_first mode, tries to avoid unnecessary searches
        """

        try:
            features = body.get("features") or {}
            msg_text = self._get_last_user_text(body)

            # Optional per-request result count override (depends on OpenWebUI build support)
            if self.valves.max_result_count_override is not None:
                features["web_search_result_count"] = int(self.valves.max_result_count_override)

            mode = (self.valves.mode or "auto").lower()

            if mode == "off":
                features["web_search"] = False
                body["features"] = features
                await self.emit_status(
                    __event_emitter__,
                    level="info",
                    message="Smart search: disabled (mode=off)",
                    done=True,
                )
                return body

            if mode == "always_on":
                features["web_search"] = True
                body["features"] = features
                await self.emit_status(
                    __event_emitter__,
                    level="info",
                    message="Smart search: enabled (mode=always_on)",
                    done=True,
                )
                if self.valves.prefetch:
                    await self._maybe_prefetch(__request__, body, __event_emitter__, __user__)
                return body

            # Auto mode
            enable, reason = self._decide_auto(msg_text, body)
            category, cat_count = self._classify_category(msg_text)
            features["web_search"] = bool(enable)
            # If enabling search and no explicit override set, apply category-based count
            if enable and self.valves.max_result_count_override is None:
                features["web_search_result_count"] = int(cat_count)
            body["features"] = features

            if enable:
                await self.emit_status(
                    __event_emitter__,
                    level="info",
                    message=(
                        "Smart search: enabled (auto mode)"
                        + (f" — cat={category}, count={cat_count}" if self.valves.debug_decision else "")
                        + (f" — {reason}" if self.valves.debug_decision else "")
                    ),
                    done=True,
                )
                if self.valves.debug_decision:
                    features["web_search_reason"] = reason
                if self.valves.prefetch:
                    await self._maybe_prefetch(__request__, body, __event_emitter__, __user__)
            else:
                await self.emit_status(
                    __event_emitter__,
                    level="info",
                    message=(
                        "Smart search: skipped (RAG/local likely sufficient)"
                        + (f" — cat={category}" if self.valves.debug_decision else "")
                        + (f" — {reason}" if self.valves.debug_decision else "")
                    ),
                    done=True,
                )
                if self.valves.debug_decision:
                    features["web_search_reason"] = reason

        except Exception as e:  # pragma: no cover
            print(f"[Smart Google PSE Filter] Error: {e}")

        return body

    async def _maybe_prefetch(
        self,
        __request__: Any,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __user__: Optional[dict],
    ) -> None:
        """Invoke the built-in web search handler to prefetch results if available."""
        if chat_web_search_handler is None or UserModel is None:
            print(
                "[Smart Google PSE Filter] INFO: Using flag-only mode; chat_web_search_handler/UserModel not available."
            )
            return

        try:
            user_obj = None
            if __user__:
                user_data = dict(__user__)
                user_data.setdefault("profile_image_url", "")
                user_data.setdefault("last_active_at", 0)
                user_data.setdefault("updated_at", 0)
                user_data.setdefault("created_at", 0)
                user_obj = UserModel(**user_data)

            await chat_web_search_handler(
                __request__,
                body,
                {"__event_emitter__": __event_emitter__},
                user_obj,
            )
        except Exception as e:  # pragma: no cover
            print(f"[Smart Google PSE Filter] Prefetch error: {e}")
