# OpenWebUI: Always-On Google PSE Web Search Filter

This folder contains a ready-to-copy Function (Filter) for OpenWebUI that forces the built-in Web Search to be enabled for every request and routes through your existing Google Programmable Search Engine (PSE) configuration.

## What you get
- `always_on_google_pse_filter.py`: a Filter you can paste directly into OpenWebUI Admin > Functions
- Works without Pipelines; uses OpenWebUI's native `chat_web_search_handler`
- Respects your Admin > Settings > Web Search configuration (Google PSE API Key + Engine ID)

## Prerequisites
- OpenWebUI running with Admin access
- Google PSE already configured in OpenWebUI (Admin > Settings > Web Search)

## Install in OpenWebUI
1. Open OpenWebUI as an Admin.
2. Go to: Admin Panel → Functions → New Function.
3. Set Type = Filter.
4. Fill in the fields:
    - ID (required; only letters, numbers, and underscores):
       ```
       always_on_google_pse_web_search
       ```
    - Name (display label):
       - Preferred: `Always On Google PSE Web Search`
       - If your UI enforces the same character rules on Name, use:
          ```
          Always_On_Google_PSE_Web_Search
          ```
    - Description:
       ```
       Forces web search to be enabled for every request, routing through your configured Google PSE engine. Overrides the UI toggle and emits a status event ("Web search automatically enabled") to confirm activation.
       ```
5. Copy all content from `always_on_google_pse_filter.py` and paste into the editor.
6. Save. Ensure the function is Enabled.
7. (Optional) Scope it to specific models/workspaces if you prefer.

## Test it
- Start a new chat and ask something that would require browsing, e.g. "What is on our website about <topic>?".
- In the streaming events, you should see: "Web search automatically enabled".
- The assistant's response will include up-to-date info retrieved via your Google PSE engine.

If you ever need to temporarily disable it, open the function and toggle the `status` valve to `false`.

## Notes
- If you see an import warning in your server logs about `chat_web_search_handler` or `UserModel`, your OpenWebUI version may have moved modules. Update the import paths accordingly.
- This function intentionally sets `body["features"]["web_search"] = True` for every request to bypass the UI toggle and ensure consistent search behavior.
