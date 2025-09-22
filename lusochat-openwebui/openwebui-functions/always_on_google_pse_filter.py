"""
id: always_on_google_pse_web_search
title: Always_On_Google_PSE_Web_Search
author: LusoChat
version: 1.0.0
license: MIT
description: Force-enable Web Search for every request and route through the configured Google PSE engine. Overrides the UI toggle and emits a status event ("Web search automatically enabled").
requirements:
  
Paste this into OpenWebUI > Admin Panel > Functions > New Function
Type: Filter
Purpose: Force-enable Web Search and route through Google PSE configured in Settings

Notes:
- Relies on OpenWebUI's built-in web search handler and your pre-configured Google PSE keys in Admin > Settings > Web Search.
- Works regardless of the UI toggle; it sets web_search on for every request.
- Emits a small status event so you can see it's active in the chat stream ("Web search automatically enabled").

Tested against OpenWebUI 0.3x APIs; adjust imports if upstream API changes.
"""

# Optional module-level identifiers (for reference/logging)
ID = "always_on_google_pse_web_search"
NAME = "Always_On_Google_PSE_Web_Search"
DESCRIPTION = (
    "Force-enable Web Search for every request and route through the configured Google PSE engine. "
    "Overrides the UI toggle and emits a status event."
)

from typing import Any, Awaitable, Callable, Optional
from pydantic import BaseModel, Field

try:
    # open-webui >= 0.3.8
    from open_webui.utils.middleware import chat_web_search_handler
    from open_webui.models.users import UserModel
except Exception:  # pragma: no cover
    # Fallback import paths if they change upstream. Update as needed.
    chat_web_search_handler = None
    UserModel = None


class Filter:
    # Explicit metadata for OpenWebUI
    id = "always_on_google_pse_web_search"
    name = "Always_On_Google_PSE_Web_Search"
    description = (
        "Force-enable Web Search for every request and route through the configured Google PSE engine. "
        "Overrides the UI toggle and emits a status event."
    )
    type = "filter"

    class Valves(BaseModel):
        status: bool = Field(
            default=True,
            description="Enable/disable this filter",
        )
        force_search_for_all: bool = Field(
            default=True,
            description="Force web search for every query regardless of content",
        )

    def __init__(self):
        self.valves = self.Valves()

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

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        """
        Mutates the request body to ensure web search is enabled and triggers
        OpenWebUI's built-in web search pipeline. Returns (possibly) modified body.
        """
        try:
            # Always force-enable the web_search flag so downstream respects search context
            features = body.get("features") or {}
            features["web_search"] = True
            body["features"] = features

            # Let the chat stream know we activated search
            await self.emit_status(
                __event_emitter__,
                level="info",
                message="Web search automatically enabled",
                done=True,
            )

            # If handler and model are available in this OpenWebUI build, invoke it to prefetch results
            if chat_web_search_handler is not None and UserModel is not None:
                # Build a UserModel from provided __user__ (OpenWebUI passes a dict)
                user_obj = None
                if __user__:
                    user_data = dict(__user__)
                    # Ensure required fields exist with safe defaults
                    user_data.setdefault("profile_image_url", "")
                    user_data.setdefault("last_active_at", 0)
                    user_data.setdefault("updated_at", 0)
                    user_data.setdefault("created_at", 0)
                    user_obj = UserModel(**user_data)

                # Invoke the built-in web search handler. This enriches the request
                # with search results using your configured Google PSE engine.
                await chat_web_search_handler(
                    __request__,
                    body,
                    {"__event_emitter__": __event_emitter__},
                    user_obj,
                )
            else:
                # Imports not found; rely on OpenWebUI's internal flow to trigger search via the flag.
                print(
                    "[Always-On Google PSE Filter] INFO: Using flag-only mode; "
                    "chat_web_search_handler/UserModel not available in imports."
                )

        except Exception as e:  # pragma: no cover
            print(f"[Always-On Google PSE Filter] Error: {e}")

        return body
