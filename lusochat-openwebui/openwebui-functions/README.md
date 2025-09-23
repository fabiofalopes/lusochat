# OpenWebUI: Google PSE Web Search Filters

This folder contains ready-to-copy Functions (Filters) for OpenWebUI to control when and how the built-in Web Search is used with your Google Programmable Search Engine (PSE) configuration.

## What you get
- `always_on_google_pse_filter.py`: forces web search on every request
- `smart_web_search_filter.py`: conditionally enables web search (off | auto | always_on) using simple heuristics
- Both work without Pipelines; they use OpenWebUI's native `chat_web_search_handler` when available
- Both respect your Admin > Settings > Web Search configuration (Google PSE API Key + Engine ID)

## Prerequisites
- OpenWebUI running with Admin access
- Google PSE already configured in OpenWebUI (Admin > Settings > Web Search)

## Install in OpenWebUI
1. Open OpenWebUI as an Admin.
2. Go to: Admin Panel → Functions → New Function.
3. Set Type = Filter.
4. Fill in the fields:
    - ID (required; only letters, numbers, and underscores):
          - Always-on filter:
             ```
             always_on_google_pse_web_search
             ```
          - Smart filter:
             ```
             smart_google_pse_web_search
             ```
    - Name (display label):
          - Always-on: `Always On Google PSE Web Search` (or `Always_On_Google_PSE_Web_Search`)
          - Smart: `Smart Google PSE Web Search` (or `Smart_Google_PSE_Web_Search`)
    - Description:
          - Always-on:
             ```
             Forces web search to be enabled for every request, routing through your configured Google PSE engine. Overrides the UI toggle and emits a status event ("Web search automatically enabled") to confirm activation.
             ```
          - Smart:
             ```
             Conditionally enables Web Search using Google PSE based on the user's query and heuristics (RAG-first). Supports modes: off, auto, always_on. Emits status events explaining the decision.
             ```
5. Copy the content from the relevant `.py` file and paste into the editor.
6. Save. Ensure the function is Enabled.
7. (Optional) Scope it to specific models/workspaces if you prefer.

## Test it
- Start a new chat and ask something that would require browsing, e.g. "What is on our website about <topic>?".
- For Always-on: you should see: "Web search automatically enabled".
- For Smart: you should see one of: "Smart search: enabled (auto mode)", "Smart search: skipped", or mode-specific messages.
- The assistant's response will include up-to-date info retrieved via your Google PSE engine.

If you ever need to temporarily disable it, open the function and toggle the `status` valve to `false`.

## Notes
- If you see an import warning in your server logs about `chat_web_search_handler` or `UserModel`, your OpenWebUI version may have moved modules. Update the import paths accordingly.
- Always-on sets `body["features"]["web_search"] = True` for every request.
- Smart filter valves:
   - `mode`: `off | auto | always_on`
   - `allow_rag_first`: when True, skips search for very short or clearly local queries
   - `min_chars_for_search`: ignore very short messages in auto mode
   - `force_keywords` / `skip_keywords`: customize for your domain and language
   - `max_result_count_override`: optional per-request override if your OpenWebUI build supports `features.web_search_result_count`

