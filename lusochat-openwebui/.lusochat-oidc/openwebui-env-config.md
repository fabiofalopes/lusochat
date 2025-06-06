Open WebUI provides a large range of environment variables that allow you to customize and configure various aspects of the application. This page serves as a comprehensive reference for all available environment variables, providing their types, default values, and descriptions. As new variables are introduced, this page will be updated to reflect the growing configuration options.

info

This page is up to date with Open WebUI release version , but is still a work in progress to later include more accurate descriptions, listing out options available for environment variables, defaults, and improving descriptions.

note

When launching Open WebUI for the first time, all environment variables are treated equally and can be used to configure the application. However, for environment variables marked as `PersistentConfig`, their values are persisted and stored internally.

After the initial launch, if you restart the container, `PersistentConfig` environment variables will no longer use the external environment variable values. Instead, they will use the internally stored values.

In contrast, regular environment variables will continue to be updated and applied on each subsequent restart.

You can update the values of `PersistentConfig` environment variables directly from within Open WebUI, and these changes will be stored internally. This allows you to manage these configuration settings independently of the external environment variables.

Please note that `PersistentConfig` environment variables are clearly marked as such in the documentation below, so you can be aware of how they will behave.

The following environment variables are used by `backend/open_webui/config.py` to provide Open WebUI startup configuration. Please note that some variables may have different default values depending on whether you're running Open WebUI directly or via Docker. For more information on logging environment variables, see our [logging documentation](https://docs.openwebui.com/getting-started/advanced-topics/logging) ).

- Type: `str` (enum: `dev`, `prod` )
- Options:
	- `dev` - Enables the FastAPI API docs on `/docs`
	- `prod` - Automatically configures several environment variables
- Default:
	- **Backend Default**: `dev`
	- **Docker Default**: `prod`
- Description: Environment setting.
- Type: `str`
- Description: Sets `WEBUI_NAME` but polls **api.openwebui.com** for metadata.
- Type: `str`
- Default: `Open WebUI`
- Description: Sets the main WebUI name. Appends `(Open WebUI)` if overridden.
- Type: `str`
- Default: `http://localhost:3000`
- Description: Specifies the URL where the Open WebUI is reachable. Currently used for search engine support.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `8080`
- Description: Sets the port to run Open WebUI from.
info

If you're running the application via Python and using the `open-webui serve` command, you cannot set the port using the `PORT` configuration. Instead, you must specify it directly as a command-line argument using the `--port` flag. For example:

```prism
open-webui serve --port 9999
```

This will run the Open WebUI on port `9999`. The `PORT` environment variable is disregarded in this mode.

- Type: `bool`
- Default: `True`
- Description: Toggles user account creation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Toggles email, password, sign in and "or" (only when `ENABLE_OAUTH_SIGNUP` is set to True) elements.
- Persistence: This environment variable is a `PersistentConfig` variable.
danger

This should **only** ever be set to `False` when [ENABLE\_OAUTH\_SIGNUP](https://docs.openwebui.com/getting-started/env-configuration/#enable_oauth_signup) is also being used and set to `True`. Failure to do so will result in the inability to login.

- Type: `bool`
- Default: `False`
- Description: When enabled, the system saves each chunk of streamed chat data to the database in real time to ensure maximum data persistency. This feature provides robust data recovery and allows accurate session tracking. However, the tradeoff is increased latency, as saving to the database introduces a delay. Disabling this feature can improve performance and reduce delays, but it risks potential data loss in the event of a system failure or crash. Use based on your application's requirements and acceptable tradeoffs.
- Type: `bool`
- Default: `True`
- Description: Controls whether admin users can export data.
- Type: `bool`
- Default: `True`
- Description: Enables admin users to access all chats.
- Type: `bool`
- Default: `False`
- Description: Enables or disables channel support.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the admin email shown by `SHOW_ADMIN_DETAILS`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Toggles whether to show admin user details in the interface.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Bypasses model access control.
- Type: `str`
- Default: empty string (' '), since `None` is set as default
- Description: Sets a default Language Model.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` (enum: `pending`, `user`, `admin` )
- Options:
	- `pending` - New users are pending until their accounts are manually activated by an admin.
	- `user` - New users are automatically activated with regular user permissions.
	- `admin` - New users are automatically activated with administrator permissions.
- Default: `pending`
- Description: Sets the default role assigned to new users.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `en`
- Description: Sets the default locale for the application.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets a webhook for integration with Discord/Slack/Microsoft Teams.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `dev-build`
- Description: Used for identifying the Git SHA of the build for releases.
- Type: `list` of `dict`
- Default: `[]`
- Description: List of banners to show to users. Format of banners are:

```prism
[{"id": "string","type": "string [info, success, warning, error]","title": "string","content": "string","dismissible": False,"timestamp": 1000}]
```

- Persistence: This environment variable is a `PersistentConfig` variable.
info

When setting this environment variable in a `.env` file, make sure to escape the quotes by wrapping the entire value in double quotes and using escaped quotes ( `\"` ) for the inner quotes. Example:

```prism
WEBUI_BANNERS="[{\"id\": \"1\", \"type\": \"warning\", \"title\": \"Your messages are stored.\", \"content\": \"Your messages are stored and may be reviewed by human people. LLM's are prone to hallucinations, check sources.\", \"dismissible\": true, \"timestamp\": 1000}]"
```

- Type: `int`
- Default: `-1`
- Description: Sets the JWT expiration time in seconds. Valid time units: `s`, `m`, `h`, `d`, `w` or `-1` for no expiration.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with NVIDIA CUDA support. Enables GPU acceleration for local Whisper and embeddings.
- Type: `int`
- Default: `300`
- Description: Specifies the timeout duration in seconds for the aiohttp client. This impacts things such as connections to Ollama and OpenAI endpoints.
info

This is the maximum amount of time the client will wait for a response before timing out. If set to an empty string (' '), the timeout will be set to `None`, effectively disabling the timeout and allowing the client to wait indefinitely.

- Type: `int`
- Description: Sets the timeout in seconds for fetching the model list. This can be useful in cases where network latency requires a longer timeout duration to successfully retrieve the model list.
- Type: `int`
- Description: Sets the timeout in seconds for fetching the model list. This can be useful in cases where network latency requires a longer timeout duration to successfully retrieve the model list.
- Type: `str`
- Default: `./data`
- Description: Specifies the base directory for data storage, including uploads, cache, vector database, etc.
- Type: `str`
- Description: Specifies the directory for fonts.
- Type: `str`
- Default: `../build`
- Description: Specifies the location of the built frontend files.
- Type: `str`
- Default: `./static`
- Description: Specifies the directory for static files, such as the favicon.
- Type: `bool`
- Default: `True`
- Description: Enables the use of Ollama APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `http://localhost:11434`
- Docker Default:
	- If `K8S_FLAG` is set: `http://ollama-service.open-webui.svc.cluster.local:11434`
	- If `USE_OLLAMA_DOCKER=True`: `http://localhost:11434`
	- Else `http://host.docker.internal:11434`
- Description: Configures the Ollama backend URL.
- Type: `str`
- Description: Configures load-balanced Ollama backend hosts, separated by `;`. See [`OLLAMA_BASE_URL`](https://docs.openwebui.com/getting-started/#ollama_base_url). Takes precedence over [`OLLAMA_BASE_URL`](https://docs.openwebui.com/getting-started/#ollama_base_url).
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with a bundled Ollama instance.
- Type: `bool`
- Default: `False`
- Description: If set, assumes Helm chart deployment and sets [`OLLAMA_BASE_URL`](https://docs.openwebui.com/getting-started/#ollama_base_url) to `http://ollama-service.open-webui.svc.cluster.local:11434`
- Type: `bool`
- Default: `True`
- Description: Enables the use of OpenAI APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `https://api.openai.com/v1`
- Description: Configures the OpenAI base API URL.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Supports balanced OpenAI base API URLs, semicolon-separated.
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the OpenAI API key.
- Example: `sk-124781258123`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Supports multiple OpenAI API keys, semicolon-separated.
- Example: `sk-124781258123;sk-4389759834759834`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation when using Ollama models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation when using OpenAI-compatible endpoints.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Prompt to use when generating chat titles.
- Default: The value of `DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE` environment variable.

Template:

```prism
### Task:
Generate a concise, 3-5 word title with an emoji summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the chat's primary language; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
### Output:
JSON format: { "title": "your concise title here" }
### Examples:
- { "title": "📉 Stock Market Trends" },
- { "title": "🍪 Perfect Chocolate Chip Recipe" },
- { "title": "Evolution of Music Streaming" },
- { "title": "Remote Work Productivity Tips" },
- { "title": "Artificial Intelligence in Healthcare" },
- { "title": "🎮 Video Game Development Insights" }
### Chat History:
<chat_history>
{{MESSAGES:END:2}}
</chat_history>
```

- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Prompt to use when calling tools.
- Default: The value of `DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE` environment variable.

Template:

```prism
Available Tools: {{TOOLS}}\nReturn an empty string if no tools match the query. If a function tool matches, construct and return a JSON object in the format {\"name\": \"functionName\", \"parameters\": {\"requiredFunctionParamKey\": \"requiredFunctionParamValue\"}} using the appropriate tool and its parameters. Only return the object and limit the response to the JSON object without additional text.
```

- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
info

When enabling `ENABLE_AUTOCOMPLETE_GENERATION`, ensure that you also configure `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH` and `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` accordingly.

- Type: `int`
- Default: `-1`
- Description: Sets the maximum input length for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: The value of `DEFAULT_AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` environment variable.

Template:

```prism
### Task:
You are an autocompletion system. Continue the text in \`<text>\` based on the **completion type** in \`<type>\` and the given language.  

### **Instructions**:
1. Analyze \`<text>\` for context and meaning.  
2. Use \`<type>\` to guide your output:  
   - **General**: Provide a natural, concise continuation.  
   - **Search Query**: Complete as if generating a realistic search query.  
3. Start as if you are directly continuing \`<text>\`. Do **not** repeat, paraphrase, or respond as a model. Simply complete the text.  
4. Ensure the continuation:
   - Flows naturally from \`<text>\`.  
   - Avoids repetition, overexplaining, or unrelated ideas.  
5. If unsure, return: \`{ "text": "" }\`.  

### **Output Rules**:
- Respond only in JSON format: \`{ "text": "<your_completion>" }\`.

### **Examples**:
#### Example 1:  
Input:  
<type>General</type>  
<text>The sun was setting over the horizon, painting the sky</text>  
Output:  
{ "text": "with vibrant shades of orange and pink." }

#### Example 2:  
Input:  
<type>Search Query</type>  
<text>Top-rated restaurants in</text>  
Output:  
{ "text": "New York City for Italian cuisine." }  

---
### Context:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>
<type>{{TYPE}}</type>  
<text>{{PROMPT}}</text>  
#### Output:
```

- Description: Sets the prompt template for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables evaluation arena models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables message rating feature.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Controls whether users are shown the share to community button.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables tags generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: The value of `DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE` environment variable.

Template:

```prism
### Task:
Generate 1-3 broad tags categorizing the main themes of the chat history, along with 1-3 more specific subtopic tags.

### Guidelines:
- Start with high-level domains (e.g. Science, Technology, Philosophy, Arts, Politics, Business, Health, Sports, Entertainment, Education)
- Consider including relevant subfields/subdomains if they are strongly represented throughout the conversation
- If content is too short (less than 3 messages) or too diverse, use only ["General"]
- Use the chat's primary language; default to English if multilingual
- Prioritize accuracy over specificity

### Output:
JSON format: { "tags": ["tag1", "tag2", "tag3"] }

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>
```

- Description: Sets the prompt template for tags generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables API key endpoint restrictions for added security and configurability.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Specifies a comma-separated list of allowed API endpoints when API key endpoint restrictions are enabled.
- Persistence: This environment variable is a `PersistentConfig` variable.
note

The value of `API_KEY_ALLOWED_ENDPOINTS` should be a comma-separated list of endpoint URLs, such as `/api/v1/messages, /api/v1/channels`.

- type: `bool`
- Default: `False`
- Description: Forwards user information (name, id, email, and role) as X-headers to OpenAI API and Ollama API. If enabled, the following headers are forwarded:
	- `X-OpenWebUI-User-Name`
	- `X-OpenWebUI-User-Id`
	- `X-OpenWebUI-User-Email`
	- `X-OpenWebUI-User-Role`
- Type: `bool`
- Default: `False`
- Description: Enables local web fetching for RAG. Enabling this allows Server Side Request Forgery attacks against local network resources.
- Type: `bool`
- Default: `True`
- Description: Bypass SSL Verification for RAG on Websites.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` (enum: `lax`, `strict`, `none` )
- Options:
	- `lax` - Sets the `SameSite` attribute to lax, allowing session cookies to be sent with requests initiated by third-party websites.
	- `strict` - Sets the `SameSite` attribute to strict, blocking session cookies from being sent with requests initiated by third-party websites.
	- `none` - Sets the `SameSite` attribute to none, allowing session cookies to be sent with requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for session cookies.
warning

When `ENABLE_OAUTH_SIGNUP` is enabled, setting `WEBUI_SESSION_COOKIE_SAME_SITE` to `strict` can cause login failures. This is because Open WebUI uses a session cookie to validate the callback from the OAuth provider, which helps prevent CSRF attacks.

However, a `strict` session cookie is not sent with the callback request, leading to potential login issues. If you experience this problem, use the default `lax` value instead.

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for session cookies if set to `True`.
- Type: `str` (enum: `lax`, `strict`, `none` )
- Options:
	- `lax` - Sets the `SameSite` attribute to lax, allowing auth cookies to be sent with requests initiated by third-party websites.
	- `strict` - Sets the `SameSite` attribute to strict, blocking auth cookies from being sent with requests initiated by third-party websites.
	- `none` - Sets the `SameSite` attribute to none, allowing auth cookies to be sent with requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for auth cookies.
info

If the value is not set, `WEBUI_SESSION_COOKIE_SAME_SITE` will be used as a fallback.

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for auth cookies if set to `True`.
info

If the value is not set, `WEBUI_SESSION_COOKIE_SECURE` will be used as a fallback.

- Type: `bool`
- Default: `True`
- Description: This setting enables or disables authentication.
danger

If set to `False`, authentication will be disabled for your Open WebUI instance. However, it's important to note that turning off authentication is only possible for fresh installations without any existing users. If there are already users registered, you cannot disable authentication directly. Ensure that no users are present in the database, if you intend to turn off `WEBUI_AUTH`.

- Type: `str`
- Default: `t0p-s3cr3t`
- Docker Default: Randomly generated on first start
- Description: Overrides the randomly generated string used for JSON Web Token.
info

When deploying Open-WebUI in a multiple node cluster with a load balancer, you must ensure that the WEBUI\_SECRET\_KEY value is the same across all instances in order to enable users to continue working if a node is recycled or their session is transferred to a different node. Without it, they will need to sign in again each time the underlying node changes.

- Type: `bool`
- Default: `False`
- Description: Enables or disables offline mode.
- Type: `bool`
- Default: `False`
- Description: Resets the `config.json` file on startup.
- Type: `bool`
- Default: `False`
- Description: Enables safe mode, which disables potentially unsafe features, deactivating all functions.
- Type: `str`
- Default: `*`
- Description: Sets the allowed origins for Cross-Origin Resource Sharing (CORS).
- Type: `bool`
- Default: `False`
- Description: Determines whether or not to allow custom models defined on the Hub in their own modeling files.
- Type: `bool`
- Default: `False`
- Description: Determines whether or not to allow custom models defined on the Hub in their own modeling files for reranking.
- Type: `bool`
- Default: `True`
- Description: Toggles automatic update of the Sentence-Transformer model.
- Type: `bool`
- Default: `True`
- Description: Toggles automatic update of the reranking model.
- Type: `bool`
- Default: `False`
- Description: Toggles automatic update of the Whisper model.
- Type: `str`
- Options:
- `chroma`, `milvus`, `qdrant`, `opensearch`, `pgvector`
- Default: `chroma`
- Description: Specifies which vector database system to use. This setting determines which vector storage system will be used for managing embeddings.
- Type: `str` (enum: `ollama`, `openai` )
- Options:
	- Leave empty for `Default (SentenceTransformers)` - Uses SentenceTransformers for embeddings.
	- `ollama` - Uses the Ollama API for embeddings.
	- `openai` - Uses the OpenAI API for embeddings.
- Description: Selects an embedding engine to use for RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `sentence-transformers/all-MiniLM-L6-v2`
- Description: Sets a model for embeddings. Locally, a Sentence-Transformer model is used.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables the use of ensemble search with `BM25` + `ChromaDB`, with reranking using `sentence_transformers` models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` ( `tika` )
- Options:
	- Leave empty to use default
	- `tika` - Use a local Apache Tika server
- Description: Sets the content extraction engine to use for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `3`
- Description: Sets the default number of results to consider when using RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `float`
- Default: `0.0`
- Description: Sets the relevance threshold to consider for documents when used with reranking.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: The value of `DEFAULT_RAG_TEMPLATE` environment variable.

Template:

```prism
### Task:
Respond to the user query using the provided context, incorporating inline citations in the format [source_id] **only when the <source_id> tag is explicitly provided** in the context.

### Guidelines:
- If you don't know the answer, clearly state that.
- If uncertain, ask the user for clarification.
- Respond in the same language as the user's query.
- If the context is unreadable or of poor quality, inform the user and provide the best possible answer.
- If the answer isn't present in the context but you possess the knowledge, explain this to the user and provide the answer using your own understanding.
- **Only include inline citations using [source_id] when a <source_id> tag is explicitly provided in the context.**  
- Do not cite if the <source_id> tag is not provided in the context.  
- Do not use XML tags in your response.
- Ensure citations are concise and directly related to the information provided.

### Example of Citation:
If the user asks about a specific topic and the information is found in "whitepaper.pdf" with a provided <source_id>, the response should include the citation like so:  
* "According to the study, the proposed method increases efficiency by 20% [whitepaper.pdf]."
If no <source_id> is present, the response should omit the citation.

### Output:
Provide a clear and direct response to the user's query, including inline citations in the format [source_id] only when the <source_id> tag is present in the context.

<context>
{{CONTEXT}}
</context>

<user_query>
{{QUERY}}
</user_query>
```

- Description: Template to use when injecting RAG documents into chat completion
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Options: `character`, `token`
- Default: `character`
- Description: Sets the text splitter for RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `{CACHE_DIR}/tiktoken`
- Description: Sets the directory for TikiToken cache.
- Type: `str`
- Default: `cl100k_base`
- Description: Sets the encoding name for TikiToken.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `1000`
- Description: Sets the document chunk size for embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `100`
- Description: Specifies how much overlap there should be between chunks.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Extracts images from PDFs using OCR when loading documents.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Description: Sets the maximum size of a file in megabytes that can be uploaded for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Description: Sets the maximum number of files that can be uploaded at once for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.
info

When configuring `RAG_FILE_MAX_SIZE` and `RAG_FILE_MAX_COUNT`, ensure that the values are reasonable to prevent excessive file uploads and potential performance issues.

- Type: `str`
- Description: Sets a model for reranking results. Locally, a Sentence-Transformer model is used.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI base API URL to use for RAG embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the OpenAI API key to use for RAG embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `1`
- Description: Sets the batch size for OpenAI embeddings.
- Type: `int`
- Default: `1`
- Description: Sets the batch size for embedding in RAG (Retrieval-Augmented Generator) models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Ollama API used in RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the base URL for Ollama API used in RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables retrieval query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: The value of `DEFAULT_QUERY_GENERATION_PROMPT_TEMPLATE` environment variable.

Template:

```prism
### Task:
Analyze the chat history to determine the necessity of generating search queries, in the given language. By default, **prioritize generating 1-3 broad and relevant search queries** unless it is absolutely certain that no additional information is required. The aim is to retrieve comprehensive, updated, and valuable information even with minimal uncertainty. If no search is unequivocally needed, return an empty list.

### Guidelines:
- Respond **EXCLUSIVELY** with a JSON object. Any form of extra commentary, explanation, or additional text is strictly prohibited.
- When generating search queries, respond in the format: { "queries": ["query1", "query2"] }, ensuring each query is distinct, concise, and relevant to the topic.
- If and only if it is entirely certain that no useful results can be retrieved by a search, return: { "queries": [] }.
- Err on the side of suggesting search queries if there is **any chance** they might provide useful or updated information.
- Be concise and focused on composing high-quality search queries, avoiding unnecessary elaboration, commentary, or assumptions.
- Today's date is: {{CURRENT_DATE}}.
- Always prioritize providing actionable and broad queries that maximize informational coverage.

### Output:
Strictly return in JSON format: 
{
  "queries": ["query1", "query2"]
}

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>
```

- Description: Sets the prompt template for query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `http://localhost:9998`
- Description: Sets the URL for the Apache Tika server.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: the value of `chromadb.DEFAULT_TENANT` (a constant in the `chromadb` module)
- Description: Sets the tenant for ChromaDB to use for RAG embeddings.
- Type: `str`
- Default: the value of `chromadb.DEFAULT_DATABASE` (a constant in the `chromadb` module)
- Description: Sets the database in the ChromaDB tenant to use for RAG embeddings.
- Type: `str`
- Description: Specifies the hostname of a remote ChromaDB Server. Uses a local ChromaDB instance if not set.
- Type: `int`
- Default: `8000`
- Description: Specifies the port of a remote ChromaDB Server.
- Type: `str`
- Description: Comma-separated list of HTTP headers to include with every ChromaDB request.
- Example: `Authorization=Bearer heuhagfuahefj,User-Agent=OpenWebUI`.
- Type: `bool`
- Default: `False`
- Description: Controls whether or not SSL is used for ChromaDB Server connections.
- Type: `str`
- Description: Specifies auth provider for remote ChromaDB Server.
- Example: `chromadb.auth.basic_authn.BasicAuthClientProvider`
- Type: `str`
- Description: Specifies auth credentials for remote ChromaDB Server.
- Example: `username:password`
- Type: `bool`
- Default: `False`
- Description: Enables or disables Google Drive integration. If set to true, and `GOOGLE_DRIVE_CLIENT_ID` & `GOOGLE_DRIVE_API_KEY` are both configured, Google Drive will appear as an upload option in the chat UI.
- Persistence: This environment variable is a `PersistentConfig` variable.
info

When enabling `GOOGLE_DRIVE_INTEGRATION`, ensure that you have configured `GOOGLE_DRIVE_CLIENT_ID` and `GOOGLE_DRIVE_API_KEY` correctly, and have reviewed Google's terms of service and usage guidelines.

- Type: `str`
- Description: Sets the client ID for Google Drive (client must be configured with Drive API and Picker API enabled).
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Google Drive integration.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${DATA_DIR}/vector_db/milvus.db`
- Description: Specifies the URI for connecting to the Milvus vector database. This can point to a local or remote Milvus server based on the deployment configuration.
- Type: `str`
- Default: `default`
- Description: Specifies the database to connect to within a milvus instance
- Type: `str`
- Default: `None`
- Description: Specifies the connection token for Milvus, optional.
- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenSearch certificate verification.
- Type: `str`
- Description: Sets the password for OpenSearch.
- Type: `bool`
- Default: `True`
- Description: Enables or disables SSL for OpenSearch.
- Type: `str`
- Default: `https://localhost:9200`
- Description: Sets the URI for OpenSearch.
- Type: `str`
- Description: Sets the username for OpenSearch.
- Type: `str`
- Default: The value of `DATABASE_URL` environment variable
- Description: Sets the database URL for model storage.
- Type: `str`
- Description: Sets the API key for Qdrant.
- Type: `str`
- Description: Sets the URI for Qdrant.
- Type: `bool`
- Default: `False`
- Description: Enable web search toggle
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables search query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables proxy set by `http_proxy` and `https_proxy` during web search content fetching.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `3`
- Description: Maximum number of search results to crawl.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `10`
- Description: Number of concurrent requests to crawl web pages returned from search results.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` (enum: `searxng`, `google_pse`, `brave`, `kagi`, `mojeek`, `serpstack`, `serper`, `serply`, `searchapi`, `duckduckgo`, `tavily`, `jina`, `bing` )
- Options:
	- `searxng` - Uses the [SearXNG](https://github.com/searxng/searxng) search engine.
	- `google_pse` - Uses the [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/).
	- `brave` - Uses the [Brave search engine](https://brave.com/search/api/).
	- `kagi` - Uses the [Kagi](https://www.kagi.com/) search engine.
	- `mojeek` - Uses the [Mojeek](https://www.mojeek.com/) search engine.
	- `serpstack` - Uses the [Serpstack](https://serpstack.com/) search engine.
	- `serper` - Uses the [Serper](https://serper.dev/) search engine.
	- `serply` - Uses the [Serply](https://serply.io/) search engine.
	- `searchapi` - Uses the [SearchAPI](https://www.searchapi.io/) search engine.
	- `duckduckgo` - Uses the [DuckDuckGo](https://duckduckgo.com/) search engine.
	- `tavily` - Uses the [Tavily](https://tavily.com/) search engine.
	- `jina` - Uses the [Jina](https://jina.ai/) search engine.
	- `bing` - Uses the [Bing](https://www.bing.com/) search engine.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `safe_web`
- Description: Specifies the loader to use for retrieving and processing web content. Options include:
	- `safe_web` - Uses the `requests` module with enhanced error handling.
	- `playwright` - Uses Playwright for more advanced web page rendering and interaction.
- Persistence: This environment variable is a `PersistentConfig` variable.
info

When using `playwright`, you have two options:

1. If `PLAYWRIGHT_WS_URI` is not set, Playwright with Chromium dependencies will be automatically installed in the Open WebUI container on launch.
2. If `PLAYWRIGHT_WS_URI` is set, Open WebUI will connect to a remote browser instance instead of installing dependencies locally.

- Type: `str`
- Default: `None`
- Description: Specifies the WebSocket URI of a remote Playwright browser instance. When set, Open WebUI will use this remote browser instead of installing browser dependencies locally. This is particularly useful in containerized environments where you want to keep the Open WebUI container lightweight and separate browser concerns. Example: `ws://playwright:3000`
- Persistence: This environment variable is a `PersistentConfig` variable.
tip

Using a remote Playwright browser via `PLAYWRIGHT_WS_URI` can be beneficial for:

- Reducing the size of the Open WebUI container
- Using a different browser other than the default Chromium
- Connecting to a non-headless (GUI) browser

- Type: `str`
- Description: The [SearXNG search API](https://docs.searxng.org/dev/search_api.html) URL supporting JSON output. `<query>` is replaced with the search query. Example: `http://searxng.local/search?q=<query>`
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for the Google Programmable Search Engine (PSE) service.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: The engine ID for the Google Programmable Search Engine (PSE) service.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for the Brave Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Kagi Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Mojeek Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Serpstack search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Configures the use of HTTPS for Serpstack requests. Free tier requests are restricted to HTTP only.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Serper search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Serply search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for SearchAPI.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the SearchAPI engine.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Tavily search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Jina.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the endpoint for Bing Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `https://api.bing.microsoft.com/v7.0/search`
- Description: Sets the subscription key for Bing Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the proxy URL for YouTube loader.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `en`
- Description: Sets the language to use for YouTube video loading.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `base`
- Description: Sets the Whisper model to use for Speech-to-Text. The backend used is faster\_whisper with quantization to `int8`.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${DATA_DIR}/cache/whisper/models`
- Description: Specifies the directory to store Whisper model files.
- Type: `str` (enum: `openai` )
- Options:
	- Leave empty to use local Whisper engine for Speech-to-Text.
	- `openai` - Uses OpenAI engine for Speech-to-Text.
- Description: Specifies the Speech-to-Text engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `whisper-1`
- Description: Specifies the Speech-to-Text model to use for OpenAI-compatible endpoints.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the OpenAI API key to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for Text-to-Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` (enum: `azure`, `elevenlabs`, `openai`, `transformers` )
- Options:
	- Leave empty to use built-in WebAPI engine for Text-to-Speech.
	- `azure` - Uses Azure engine for Text-to-Speech.
	- `elevenlabs` - Uses ElevenLabs engine for Text-to-Speech
	- `openai` - Uses OpenAI engine for Text-to-Speech.
	- `transformers` - Uses SentenceTransformers for Text-to-Speech.
- Description: Specifies the Text-to-Speech engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `tts-1`
- Description: Specifies the OpenAI text-to-speech model to use.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the output format for Azure Text to Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the region for Azure Text to Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for text-to-speech.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the API key to use for text-to-speech.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `punctuation`
- Description: Sets the OpenAI text-to-speech split on to use.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `alloy`
- Description: Sets the OpenAI text-to-speech voice to use.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables image generation features.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str` (enum: `openai`, `comfyui`, `automatic1111` )
- Options:
	- `openai` - Uses OpenAI DALL-E for image generation.
	- `comfyui` - Uses ComfyUI engine for image generation.
	- `automatic1111` - Uses Automatic1111 engine for image generation (default).
- Default: `openai`
- Description: Specifies the engine to use for image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Default model to use for image generation
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `512x512`
- Description: Sets the default image size to generate.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `50`
- Description: Sets the default iteration steps for image generation. Used for ComfyUI and AUTOMATIC1111.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the Automatic1111 API authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Specifies the URL to Automatic1111's Stable Diffusion API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `float`
- Description: Sets the scale for Automatic1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the sampler for Automatic1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the scheduler for Automatic1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Specifies the URL to the ComfyUI image generation API.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the API key for ComfyUI.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default:

```prism
{
  "3": {
    "inputs": {
      "seed": 0,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "model.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "Prompt",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
```

- Description: Sets the ComfyUI workflow.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for DALL-E image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the API key to use for DALL-E image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables account creation when sighting up via OAuth. Distinct from `ENABLE_SIGNUP`.
- Persistence: This environment variable is a `PersistentConfig` variable.
danger

`ENABLE_LOGIN_FORM` must be set to `False` when `ENABLE_OAUTH_SIGNUP` is set to `True`. Failure to do so will result in the inability to login.

- Type: `bool`
- Default: `True`
- Description: Enables API key authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables role management to oauth delegation.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables OAUTH group management.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: If enabled, merges OAuth accounts with existing accounts using the same email address. This is considered unsafe as not all OAuth providers will verify email addresses and can lead to potential account takeovers.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `name`
- Description: Set username claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `email`
- Description: Set email claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `picture`
- Description: Set picture (avatar) claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `groups`
- Description: Specifies the group claim for OAUTH authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `roles`
- Description: Sets the roles claim to look for in the OIDC token.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for OIDC authentication. `openid` and `email` are required.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `*`
- Description: Specifies the allowed domains for OAUTH authentication. (e.g. "example1.com,example2.com").
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `user,admin`
- Description: Sets the roles that are allowed access to the platform.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `admin`
- Description: Sets the roles that are considered administrators.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Defines the trusted request header for authentication. See [SSO docs](https://docs.openwebui.com/features/sso).
- Type: `str`
- Description: Defines the trusted request header for the username of anyone registering with the `WEBUI_AUTH_TRUSTED_EMAIL_HEADER` header. See [SSO docs](https://docs.openwebui.com/features/sso).

See [https://support.google.com/cloud/answer/6158849?hl=en](https://support.google.com/cloud/answer/6158849?hl=en)

- Type: `str`
- Description: Sets the client ID for Google OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the client secret for Google OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Google OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `<backend>/oauth/google/callback`
- Description: Sets the redirect URI for Google OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.

See [https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

- Type: `str`
- Description: Sets the client ID for Microsoft OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the client secret for Microsoft OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the tenant ID for Microsoft OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Microsoft OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `<backend>/oauth/microsoft/callback`
- Description: Sets the redirect URI for Microsoft OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.

See

- Type: `str`
- Description: Sets the client ID for Github OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the client secret for Github OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `user:email`
- Description: Sets the scope for Github OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `<backend>/oauth/github/callback`
- Description: Sets the redirect URI for Github OAuth
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the client ID for OIDC
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the client secret for OIDC
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Path to the `.well-known/openid-configuration` endpoint
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `SSO`
- Description: Sets the name for the OIDC provider.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `<backend>/oauth/oidc/callback`
- Description: Sets the redirect URI for OIDC
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the distinguished name for LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the password for LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the attribute to use as username for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the attribute to use as mail for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the path to LDAP CA certificate file.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `ALL`
- Description: Sets the ciphers to use for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the base to search for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the filter to use for LDAP search.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Default: `localhost`
- Description: Sets the hostname of LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `str`
- Description: Sets the label of LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `int`
- Default: `389`
- Description: Sets the port number of LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables TLS for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace models.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace knowledge.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace tools.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to upload files to chats.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to delete chats.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to edit chats.
- Persistence: This environment variable is a `PersistentConfig` variable.
- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to create temporary chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

These variables are not specific to Open WebUI but can still be valuable in certain contexts.

- Type: `str`
- Options:
	- `s3` - uses S3 client library and related environment variables mentioned in [Amazon S3 Storage](https://docs.openwebui.com/getting-started/#amazon-s3-storage)
	- `gcs` - uses GCS client library and related environment variables mentioned in [Google Cloud Storage](https://docs.openwebui.com/getting-started/#google-cloud-storage)
	- `azure` - uses Azure client library and related environment variables mentioned in [Microsoft Azure Storage](https://docs.openwebui.com/getting-started/#microsoft-azure-storage)
- Default: empty string (' '), which defaults to `local`
- Description: Sets the storage provider.
- Type: `str`
- Description: Sets the access key ID for S3 storage.
- Type: `str`
- Description: Sets the bucket name for S3 storage.
- Type: `str`
- Description: Sets the endpoint URL for S3 storage.
- Type: `str`
- Description: Sets the key prefix for a S3 object.
- Type: `str`
- Description: Sets the region name for S3 storage.
- Type: `str`
- Description: Sets the secret access key for S3 storage.
- Type: `str`
- Description: Contents of Google Application Credentials JSON file.
	- Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Google Metadata server if run on a Google Compute Engine.
	- File can be generated for a service account following this [guide](https://developers.google.com/workspace/guides/create-credentials#service-account)
- Type: `str`
- Description: Sets the bucket name for Google Cloud Storage. Bucket must already exist.
- Type: `str`
- Description: Sets the endpoint URL for Azure Storage.
- Type: `str`
- Description: Sets the container name for Azure Storage.
- Type: `str`
- Description: Set the access key for Azure Storage.
	- Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Managed Identity if run in Azure services.
- Type: `str`
- Default: `sqlite:///${DATA_DIR}/webui.db`
- Description: Specifies the database URL to connect to.
info

Supports SQLite and Postgres. Changing the URL does not migrate data between databases. Documentation on URL scheme available [here](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).

- Type: `int`
- Default: `0`
- Description: Specifies the size of the database pool. A value of `0` disables pooling.
- Type: `int`
- Default: `0`
- Description: Specifies the database pool max overflow.
info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow).

- Type: `int`
- Default: `30`
- Description: Specifies the database pool timeout in seconds to get a connection.
info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.timeout).

- Type: `int`
- Default: `3600`
- Description: Specifies the database pool recycle time in seconds.
info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#setting-pool-recycle).

- Type: `bool`
- Default: `False`
- Description: Enables websocket support in Open WebUI (used with Redis).
- Type: `str`
- Default: `redis`
- Description: Specifies the websocket manager to use (in this case, Redis).
- Type: `str`
- Default: `redis://localhost:6379/0`
- Description: Specifies the URL of the Redis instance for websocket communication.

Open WebUI supports using proxies for HTTP and HTTPS retrievals. To specify proxy settings, Open WebUI uses the following environment variables:

- Type: `str`
- Description: Sets the URL for the HTTP proxy.
- Type: `str`
- Description: Sets the URL for the HTTPS proxy.
- Type: `str`
- Description: Lists domain extensions (or IP addresses) for which the proxy should not be used, separated by commas. For example, setting no\_proxy to '.mit.edu' ensures that the proxy is bypassed when accessing documents from MIT.

Open WebUI provides environment variables to customize the pip installation process. Below are the environment variables used by Open WebUI for adjusting package installation behavior:

- Type: `str`
- Description: Specifies additional command-line options that pip should use when installing packages. For example, you can include flags such as `--upgrade`, `--user`, or `--no-cache-dir` to control the installation process.
- Type: `str`
- Description: Defines custom package index behavior for pip. This can include specifying additional or alternate index URLs (e.g., `--extra-index-url` ), authentication credentials, or other parameters to manage how packages are retrieved from different locations.