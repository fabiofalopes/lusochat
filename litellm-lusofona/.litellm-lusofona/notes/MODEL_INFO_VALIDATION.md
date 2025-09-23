# LiteLLM Model Config Validation – Notes

Date: 2025-09-23
Author: Team LusoChat

## Summary
We audited and cleaned our LiteLLM model configuration files to remove unsupported/ignored fields and align with LiteLLM’s actual schema and behavior. This ensures predictable behavior, cleaner /model/info output, and avoids misleading metadata.

Files updated:
- `models/groq.yaml`
- `models/sambanova.yaml`
- `models/openai.yaml`
- `models/on-premise.yaml`

## What’s valid in model_info
Based on LiteLLM’s source (schema + utils + router):
- mode: one of chat, embedding, completion, image_generation, audio_transcription, responses (provider dependent)
- max_tokens, max_input_tokens, max_output_tokens
- input_cost_per_token, output_cost_per_token (note: typically we override pricing via `litellm_params` per deployment, but these values are surfaced by /model/info)
- Capability flags: supports_vision, supports_function_calling, supports_audio_input, supports_prompt_caching, …
- litellm_provider (optional override)

Where rate limits & pricing belong:
- rpm, tpm, input_cost_per_token, output_cost_per_token are configured under `litellm_params` for the deployment and used for routing & cost tracking.

## What we removed (unsupported/ignored)
- speed_tokens_per_second – not used anywhere in LiteLLM
- context_window – replaced with `max_tokens`
- model_alias – not used by router/UI
- host_node – not used by router/UI
- pricing_tier – not used by router/UI
- Non-standard modes (e.g., moderation, prompt_injection_detection) – normalized to `mode: chat` for safety models; set `audio_transcription` for STT; `embedding` for embedding models; `text_to_speech` only where applicable.

OpenAI-specific normalization we applied:
- Replaced `context_window` with `max_tokens` across chat models
- Removed `model_alias`, `host_node`, `pricing_tier`, `note`
- Whisper: converted `max_file_size` → `max_file_size_mb`
- Embeddings: used `output_vector_size` instead of `embedding_dimensions`
- TTS models: used `input_cost_per_character` (LiteLLM convention) instead of `output_cost_per_character`
- Image models: used `output_cost_per_image` where applicable and kept text prompt costs in `input_cost_per_token`

## Evidence (authoritative references)
- Docs: Model Management (structure and /model/info response)
  - https://docs.litellm.ai/docs/proxy/model_management
- Implementation: `get_model_info()` and fields mapped
  - https://github.com/BerriAI/litellm/blob/main/litellm/utils.py
- Types (canonical accepted keys)
  - https://github.com/BerriAI/litellm/blob/main/litellm/types/utils.py
  - https://github.com/BerriAI/litellm/blob/main/litellm/types/router.py
- Public cost map (merged into /model/info)
  - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json

## What changed
- `groq.yaml`
  - Removed: speed_tokens_per_second, context_window, model_alias, host_node, pricing_tier
  - Replaced `context_window` → `max_tokens`
  - Modes: chat (LLMs, safety), audio_transcription (Whisper), text_to_speech (PlayAI TTS)
  - Kept: max_output_tokens, supports_vision, supports_function_calling, max_file_size_mb

- `sambanova.yaml`
  - Removed: host_node, category, rpd, context_window
  - Replaced `context_window` → `max_tokens`
  - Modes: chat (LLMs/vision), audio_transcription (Whisper), embedding (embedding model)
  - Kept: max_output_tokens, supports_vision, max_file_size_mb

- `on-premise.yaml`
  - Removed: model_alias, host_node, provider (non-schema fields)
  - Added/normalized modes: `embedding` for Ollama embeddings, `rerank` for rerankers, `chat` for LLMs
  - Added pricing placeholders for cost tracking: embeddings `input_cost_per_token: 0.0`, rerankers `input_cost_per_query: 0.0`, chat LLMs `input_cost_per_token: 0.0` + `output_cost_per_token: 0.0`
  - These can be replaced with your internal cost model; alternatively use `input_cost_per_second` if you prefer time-based accounting
  - Added comprehensive internal rate card guidance with 3 calculation methods: GPU cost amortization, cloud equivalency, and operational cost approaches
  - Provided example rates: embeddings ~0.5¢/1M tokens, chat models ~10-20¢/1M tokens, rerankers ~0.01¢/query

- `openai.yaml`
  - Removed: model_alias, host_node, pricing_tier, context_window, non-schema keys (voices, output_formats, supported_sizes, quality_options)
  - Added/normalized: `mode: chat` for all chat models; `max_tokens` set; Whisper `max_file_size_mb` set; embeddings `output_vector_size`; DALL·E & GPT-Image `output_cost_per_image`

## How to verify
1) YAML syntax
   - Both configs validated with Python `yaml.safe_load`.

2) Proxy output
   - Call your proxy `/v1/model/info` to confirm only supported fields are returned and that removed fields do not appear.

3) Quick smoke calls
   - Run a small chat completion against a cleaned model and confirm cost tracking and rpm/tpm limits behave as expected (from `litellm_params`).

## Notes
- Even if unsupported fields are present, LiteLLM ignores them; but cleaning avoids confusion and keeps UI and audits consistent.
- If you add new providers, use these notes and the links above to validate fields.
