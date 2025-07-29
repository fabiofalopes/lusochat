```yaml
environment_variables: {}

model_list:
  - model_name: string
    litellm_params: {}
    model_info:
      id: string
      mode: embedding
      input_cost_per_token: 0
      output_cost_per_token: 0
      max_tokens: 2048
      base_model: gpt-4-1106-preview
      additionalProp1: {}

litellm_settings:
  # Logging/Callback settings
  success_callback: ["langfuse"]  # list of success callbacks
  failure_callback: ["sentry"]  # list of failure callbacks
  callbacks: ["otel"]  # list of callbacks - runs on success and failure
  service_callbacks: ["datadog", "prometheus"]  # logs redis, postgres failures on datadog, prometheus
  turn_off_message_logging: boolean  # prevent the messages and responses from being logged to on your callbacks, but request metadata will still be logged.
  redact_user_api_key_info: boolean  # Redact information about the user api key (hashed token, user_id, team id, etc.), from logs. Currently supported for Langfuse, OpenTelemetry, Logfire, ArizeAI logging.
  langfuse_default_tags: ["cache_hit", "cache_key", "proxy_base_url", "user_api_key_alias", "user_api_key_user_id", "user_api_key_user_email", "user_api_key_team_alias", "semantic-similarity", "proxy_base_url"] # default tags for Langfuse Logging
  
  # Networking settings
  request_timeout: 10 # (int) llm requesttimeout in seconds. Raise Timeout error if call takes longer than 10s. Sets litellm.request_timeout 
  force_ipv4: boolean # If true, litellm will force ipv4 for all LLM requests. Some users have seen httpx ConnectionError when using ipv6 + Anthropic API
  
  set_verbose: boolean # sets litellm.set_verbose=True to view verbose debug logs. DO NOT LEAVE THIS ON IN PRODUCTION
  json_logs: boolean # if true, logs will be in json format

  # Fallbacks, reliability
  default_fallbacks: ["claude-opus"] # set default_fallbacks, in case a specific model group is misconfigured / bad.
  content_policy_fallbacks: [{"gpt-3.5-turbo-small": ["claude-opus"]}] # fallbacks for ContentPolicyErrors
  context_window_fallbacks: [{"gpt-3.5-turbo-small": ["gpt-3.5-turbo-large", "claude-opus"]}] # fallbacks for ContextWindowExceededErrors

  # Caching settings
  cache: true 
  cache_params:        # set cache params for redis
    type: redis        # type of cache to initialize

    # Optional - Redis Settings
    host: "localhost"  # The host address for the Redis cache. Required if type is "redis".
    port: 6379  # The port number for the Redis cache. Required if type is "redis".
    password: "your_password"  # The password for the Redis cache. Required if type is "redis".
    namespace: "litellm.caching.caching" # namespace for redis cache
  
    # Optional - Redis Cluster Settings
    redis_startup_nodes: [{"host": "127.0.0.1", "port": "7001"}] 

    # Optional - Redis Sentinel Settings
    service_name: "mymaster"
    sentinel_nodes: [["localhost", 26379]]

    # Optional - Qdrant Semantic Cache Settings
    qdrant_semantic_cache_embedding_model: openai-embedding # the model should be defined on the model_list
    qdrant_collection_name: test_collection
    qdrant_quantization_config: binary
    similarity_threshold: 0.8   # similarity threshold for semantic cache

    # Optional - S3 Cache Settings
    s3_bucket_name: cache-bucket-litellm   # AWS Bucket Name for S3
    s3_region_name: us-west-2              # AWS Region Name for S3
    s3_aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID  # us os.environ/<variable name> to pass environment variables. This is AWS Access Key ID for S3
    s3_aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY  # AWS Secret Access Key for S3
    s3_endpoint_url: https://s3.amazonaws.com  # [OPTIONAL] S3 endpoint URL, if you want to use Backblaze/cloudflare s3 bucket

    # Common Cache settings
    # Optional - Supported call types for caching
    supported_call_types: ["acompletion", "atext_completion", "aembedding", "atranscription"]
                          # /chat/completions, /completions, /embeddings, /audio/transcriptions
    mode: default_off # if default_off, you need to opt in to caching on a per call basis
    ttl: 600 # ttl for caching
    disable_copilot_system_to_assistant: False  # If false (default), converts all 'system' role messages to 'assistant' for GitHub Copilot compatibility. Set to true to disable this behavior.

callback_settings:
  otel:
    message_logging: boolean  # OTEL logging callback specific settings

general_settings:
  completion_model: string
  disable_spend_logs: boolean  # turn off writing each transaction to the db
  disable_master_key_return: boolean  # turn off returning master key on UI (checked on '/user/info' endpoint)
  disable_retry_on_max_parallel_request_limit_error: boolean  # turn off retries when max parallel request limit is reached
  disable_reset_budget: boolean  # turn off reset budget scheduled task
  disable_adding_master_key_hash_to_db: boolean  # turn off storing master key hash in db, for spend tracking
  enable_jwt_auth: boolean  # allow proxy admin to auth in via jwt tokens with 'litellm_proxy_admin' in claims
  enforce_user_param: boolean  # requires all openai endpoint requests to have a 'user' param
  allowed_routes: ["route1", "route2"]  # list of allowed proxy API routes - a user can access. (currently JWT-Auth only)
  key_management_system: google_kms  # either google_kms or azure_kms
  master_key: string
  maximum_spend_logs_retention_period: 30d # The maximum time to retain spend logs before deletion.
  maximum_spend_logs_retention_interval: 1d # interval in which the spend log cleanup task should run in.

  # Database Settings
  database_url: string
  database_connection_pool_limit: 0  # default 100
  database_connection_timeout: 0  # default 60s
  allow_requests_on_db_unavailable: boolean  # if true, will allow requests that can not connect to the DB to verify Virtual Key to still work 

  custom_auth: string
  max_parallel_requests: 0  # the max parallel requests allowed per deployment 
  global_max_parallel_requests: 0  # the max parallel requests allowed on the proxy all up 
  infer_model_from_keys: true
  background_health_checks: true
  health_check_interval: 300
  alerting: ["slack", "email"]
  alerting_threshold: 0
  use_client_credentials_pass_through_routes: boolean  # use client credentials for all pass through routes like "/vertex-ai", /bedrock/. When this is True Virtual Key auth will not be applied on these endpoints
```

### litellm\_settings - Reference

| Name | Type | Description |
| --- | --- | --- |
| success\_callback | array of strings | List of success callbacks. [Doc Proxy logging callbacks](https://docs.litellm.ai/docs/proxy/logging), [Doc Metrics](https://docs.litellm.ai/docs/proxy/prometheus) |
| failure\_callback | array of strings | List of failure callbacks [Doc Proxy logging callbacks](https://docs.litellm.ai/docs/proxy/logging), [Doc Metrics](https://docs.litellm.ai/docs/proxy/prometheus) |
| callbacks | array of strings | List of callbacks - runs on success and failure [Doc Proxy logging callbacks](https://docs.litellm.ai/docs/proxy/logging), [Doc Metrics](https://docs.litellm.ai/docs/proxy/prometheus) |
| service\_callbacks | array of strings | System health monitoring - Logs redis, postgres failures on specified services (e.g. datadog, prometheus) [Doc Metrics](https://docs.litellm.ai/docs/proxy/prometheus) |
| turn\_off\_message\_logging | boolean | If true, prevents messages and responses from being logged to callbacks, but request metadata will still be logged [Proxy Logging](https://docs.litellm.ai/docs/proxy/logging) |
| modify\_params | boolean | If true, allows modifying the parameters of the request before it is sent to the LLM provider |
| enable\_preview\_features | boolean | If true, enables preview features - e.g. Azure O1 Models with streaming support. |
| redact\_user\_api\_key\_info | boolean | If true, redacts information about the user api key from logs [Proxy Logging](https://docs.litellm.ai/docs/proxy/logging#redacting-userapikeyinfo) |
| langfuse\_default\_tags | array of strings | Default tags for Langfuse Logging. Use this if you want to control which LiteLLM-specific fields are logged as tags by the LiteLLM proxy. By default LiteLLM Proxy logs no LiteLLM-specific fields as tags. [Further docs](https://docs.litellm.ai/docs/proxy/logging#litellm-specific-tags-on-langfuse---cache_hit-cache_key) |
| set\_verbose | boolean | If true, sets litellm.set\_verbose=True to view verbose debug logs. DO NOT LEAVE THIS ON IN PRODUCTION |
| json\_logs | boolean | If true, logs will be in json format. If you need to store the logs as JSON, just set the `litellm.json_logs = True`. We currently just log the raw POST request from litellm as a JSON [Further docs](https://docs.litellm.ai/docs/proxy/debugging) |
| default\_fallbacks | array of strings | List of fallback models to use if a specific model group is misconfigured / bad. [Further docs](https://docs.litellm.ai/docs/proxy/reliability#default-fallbacks) |
| request\_timeout | integer | The timeout for requests in seconds. If not set, the default value is `6000 seconds`. [For reference OpenAI Python SDK defaults to `600 seconds`.](https://github.com/openai/openai-python/blob/main/src/openai/_constants.py) |
| force\_ipv4 | boolean | If true, litellm will force ipv4 for all LLM requests. Some users have seen httpx ConnectionError when using ipv6 + Anthropic API |
| content\_policy\_fallbacks | array of objects | Fallbacks to use when a ContentPolicyViolationError is encountered. [Further docs](https://docs.litellm.ai/docs/proxy/reliability#content-policy-fallbacks) |
| context\_window\_fallbacks | array of objects | Fallbacks to use when a ContextWindowExceededError is encountered. [Further docs](https://docs.litellm.ai/docs/proxy/reliability#context-window-fallbacks) |
| cache | boolean | If true, enables caching. [Further docs](https://docs.litellm.ai/docs/proxy/caching) |
| cache\_params | object | Parameters for the cache. [Further docs](https://docs.litellm.ai/docs/proxy/caching#supported-cache_params-on-proxy-configyaml) |
| disable\_end\_user\_cost\_tracking | boolean | If true, turns off end user cost tracking on prometheus metrics + litellm spend logs table on proxy. |
| disable\_end\_user\_cost\_tracking\_prometheus\_only | boolean | If true, turns off end user cost tracking on prometheus metrics only. |
| key\_generation\_settings | object | Restricts who can generate keys. [Further docs](https://docs.litellm.ai/docs/proxy/virtual_keys#restricting-key-generation) |
| disable\_add\_transform\_inline\_image\_block | boolean | For Fireworks AI models - if true, turns off the auto-add of `#transform=inline` to the url of the image\_url, if the model is not a vision model. |
| disable\_hf\_tokenizer\_download | boolean | If true, it defaults to using the openai tokenizer for all models (including huggingface models). |
| enable\_json\_schema\_validation | boolean | If true, enables json schema validation for all requests. |
| disable\_copilot\_system\_to\_assistant | boolean | If false (default), converts all 'system' role messages to 'assistant' for GitHub Copilot compatibility. Set to true to disable this behavior. Useful for tools (like Claude Code) that send system messages, which Copilot does not support. |

### general\_settings - Reference

| Name | Type | Description |
| --- | --- | --- |
| completion\_model | string | The default model to use for completions when `model` is not specified in the request |
| disable\_spend\_logs | boolean | If true, turns off writing each transaction to the database |
| disable\_spend\_updates | boolean | If true, turns off all spend updates to the DB. Including key/user/team spend updates. |
| disable\_master\_key\_return | boolean | If true, turns off returning master key on UI. (checked on '/user/info' endpoint) |
| disable\_retry\_on\_max\_parallel\_request\_limit\_error | boolean | If true, turns off retries when max parallel request limit is reached |
| disable\_reset\_budget | boolean | If true, turns off reset budget scheduled task |
| disable\_adding\_master\_key\_hash\_to\_db | boolean | If true, turns off storing master key hash in db |
| enable\_jwt\_auth | boolean | allow proxy admin to auth in via jwt tokens with 'litellm\_proxy\_admin' in claims. [Doc on JWT Tokens](https://docs.litellm.ai/docs/proxy/token_auth) |
| enforce\_user\_param | boolean | If true, requires all OpenAI endpoint requests to have a 'user' param. [Doc on call hooks](https://docs.litellm.ai/docs/proxy/call_hooks) |
| allowed\_routes | array of strings | List of allowed proxy API routes a user can access [Doc on controlling allowed routes](https://docs.litellm.ai/docs/proxy/enterprise#control-available-public-private-routes) |
| key\_management\_system | string | Specifies the key management system. [Doc Secret Managers](https://docs.litellm.ai/docs/secret) |
| master\_key | string | The master key for the proxy [Set up Virtual Keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| database\_url | string | The URL for the database connection [Set up Virtual Keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| database\_connection\_pool\_limit | integer | The limit for database connection pool [Setting DB Connection Pool limit](https://docs.litellm.ai/docs/proxy/#configure-db-pool-limits--connection-timeouts) |
| database\_connection\_timeout | integer | The timeout for database connections in seconds [Setting DB Connection Pool limit, timeout](https://docs.litellm.ai/docs/proxy/#configure-db-pool-limits--connection-timeouts) |
| allow\_requests\_on\_db\_unavailable | boolean | If true, allows requests to succeed even if DB is unreachable. **Only use this if running LiteLLM in your VPC** This will allow requests to work even when LiteLLM cannot connect to the DB to verify a Virtual Key [Doc on graceful db unavailability](https://docs.litellm.ai/docs/proxy/prod#5-if-running-litellm-on-vpc-gracefully-handle-db-unavailability) |
| custom\_auth | string | Write your own custom authentication logic [Doc Custom Auth](https://docs.litellm.ai/docs/proxy/virtual_keys#custom-auth) |
| max\_parallel\_requests | integer | The max parallel requests allowed per deployment |
| global\_max\_parallel\_requests | integer | The max parallel requests allowed on the proxy overall |
| infer\_model\_from\_keys | boolean | If true, infers the model from the provided keys |
| background\_health\_checks | boolean | If true, enables background health checks. [Doc on health checks](https://docs.litellm.ai/docs/proxy/health) |
| health\_check\_interval | integer | The interval for health checks in seconds [Doc on health checks](https://docs.litellm.ai/docs/proxy/health) |
| alerting | array of strings | List of alerting methods [Doc on Slack Alerting](https://docs.litellm.ai/docs/proxy/alerting) |
| alerting\_threshold | integer | The threshold for triggering alerts [Doc on Slack Alerting](https://docs.litellm.ai/docs/proxy/alerting) |
| use\_client\_credentials\_pass\_through\_routes | boolean | If true, uses client credentials for all pass-through routes. [Doc on pass through routes](https://docs.litellm.ai/docs/proxy/pass_through) |
| health\_check\_details | boolean | If false, hides health check details (e.g. remaining rate limit). [Doc on health checks](https://docs.litellm.ai/docs/proxy/health) |
| public\_routes | List\[str\] | (Enterprise Feature) Control list of public routes |
| alert\_types | List\[str\] | Control list of alert types to send to slack (Doc on alert types)\[./alerting.md\] |
| enforced\_params | List\[str\] | (Enterprise Feature) List of params that must be included in all requests to the proxy |
| enable\_oauth2\_auth | boolean | (Enterprise Feature) If true, enables oauth2.0 authentication |
| use\_x\_forwarded\_for | str | If true, uses the X-Forwarded-For header to get the client IP address |
| service\_account\_settings | List\[Dict\[str, Any\]\] | Set `service_account_settings` if you want to create settings that only apply to service account keys (Doc on service accounts)\[./service\_accounts.md\] |
| image\_generation\_model | str | The default model to use for image generation - ignores model set in request |
| store\_model\_in\_db | boolean | If true, enables storing model + credential information in the DB. |
| store\_prompts\_in\_spend\_logs | boolean | If true, allows prompts and responses to be stored in the spend logs table. |
| max\_request\_size\_mb | int | The maximum size for requests in MB. Requests above this size will be rejected. |
| max\_response\_size\_mb | int | The maximum size for responses in MB. LLM Responses above this size will not be sent. |
| proxy\_budget\_rescheduler\_min\_time | int | The minimum time (in seconds) to wait before checking db for budget resets. **Default is 597 seconds** |
| proxy\_budget\_rescheduler\_max\_time | int | The maximum time (in seconds) to wait before checking db for budget resets. **Default is 605 seconds** |
| proxy\_batch\_write\_at | int | Time (in seconds) to wait before batch writing spend logs to the db. **Default is 10 seconds** |
| proxy\_batch\_polling\_interval | int | Time (in seconds) to wait before polling a batch, to check if it's completed. **Default is 6000 seconds (1 hour)** |
| alerting\_args | dict | Args for Slack Alerting [Doc on Slack Alerting](https://docs.litellm.ai/docs/proxy/alerting) |
| custom\_key\_generate | str | Custom function for key generation [Doc on custom key generation](https://docs.litellm.ai/docs/proxy/virtual_keys#custom--key-generate) |
| allowed\_ips | List\[str\] | List of IPs allowed to access the proxy. If not set, all IPs are allowed. |
| embedding\_model | str | The default model to use for embeddings - ignores model set in request |
| default\_team\_disabled | boolean | If true, users cannot create 'personal' keys (keys with no team\_id). |
| alert\_to\_webhook\_url | Dict\[str\] | [Specify a webhook url for each alert type.](https://docs.litellm.ai/docs/proxy/alerting#set-specific-slack-channels-per-alert-type) |
| key\_management\_settings | List\[Dict\[str, Any\]\] | Settings for key management system (e.g. AWS KMS, Azure Key Vault) [Doc on key management](https://docs.litellm.ai/docs/secret) |
| allow\_user\_auth | boolean | (Deprecated) old approach for user authentication. |
| user\_api\_key\_cache\_ttl | int | The time (in seconds) to cache user api keys in memory. |
| disable\_prisma\_schema\_update | boolean | If true, turns off automatic schema updates to DB |
| litellm\_key\_header\_name | str | If set, allows passing LiteLLM keys as a custom header. [Doc on custom headers](https://docs.litellm.ai/docs/proxy/virtual_keys#custom-headers) |
| moderation\_model | str | The default model to use for moderation. |
| custom\_sso | str | Path to a python file that implements custom SSO logic. [Doc on custom SSO](https://docs.litellm.ai/docs/proxy/custom_sso) |
| allow\_client\_side\_credentials | boolean | If true, allows passing client side credentials to the proxy. (Useful when testing finetuning models) [Doc on client side credentials](https://docs.litellm.ai/docs/proxy/virtual_keys#client-side-credentials) |
| admin\_only\_routes | List\[str\] | (Enterprise Feature) List of routes that are only accessible to admin users. [Doc on admin only routes](https://docs.litellm.ai/docs/proxy/enterprise#control-available-public-private-routes) |
| use\_azure\_key\_vault | boolean | If true, load keys from azure key vault |
| use\_google\_kms | boolean | If true, load keys from google kms |
| spend\_report\_frequency | str | Specify how often you want a Spend Report to be sent (e.g. "1d", "2d", "30d") [More on this](https://docs.litellm.ai/docs/proxy/alerting#spend-report-frequency) |
| ui\_access\_mode | Literal\["admin\_only"\] | If set, restricts access to the UI to admin users only. [Docs](https://docs.litellm.ai/docs/proxy/ui#restrict-ui-access) |
| litellm\_jwtauth | Dict\[str, Any\] | Settings for JWT authentication. [Docs](https://docs.litellm.ai/docs/proxy/token_auth) |
| litellm\_license | str | The license key for the proxy. [Docs](https://docs.litellm.ai/docs/enterprise#how-does-deployment-with-enterprise-license-work) |
| oauth2\_config\_mappings | Dict\[str, str\] | Define the OAuth2 config mappings |
| pass\_through\_endpoints | List\[Dict\[str, Any\]\] | Define the pass through endpoints. [Docs](https://docs.litellm.ai/docs/proxy/pass_through) |
| enable\_oauth2\_proxy\_auth | boolean | (Enterprise Feature) If true, enables oauth2.0 authentication |
| forward\_openai\_org\_id | boolean | If true, forwards the OpenAI Organization ID to the backend LLM call (if it's OpenAI). |
| forward\_client\_headers\_to\_llm\_api | boolean | If true, forwards the client headers (any `x-` headers and `anthropic-beta` headers) to the backend LLM call |
| maximum\_spend\_logs\_retention\_period | str | Used to set the max retention time for spend logs in the db, after which they will be auto-purged |
| maximum\_spend\_logs\_retention\_interval | str | Used to set the interval in which the spend log cleanup task should run in. |

### router\_settings - Reference

```yaml
router_settings:
  routing_strategy: usage-based-routing-v2 # Literal["simple-shuffle", "least-busy", "usage-based-routing","latency-based-routing"], default="simple-shuffle"
  redis_host: <your-redis-host>           # string
  redis_password: <your-redis-password>   # string
  redis_port: <your-redis-port>           # string
  enable_pre_call_checks: true            # bool - Before call is made check if a call is within model context window 
  allowed_fails: 3 # cooldown model if it fails > 1 call in a minute. 
  cooldown_time: 30 # (in seconds) how long to cooldown model if fails/min > allowed_fails
  disable_cooldowns: True                  # bool - Disable cooldowns for all models 
  enable_tag_filtering: True                # bool - Use tag based routing for requests
  retry_policy: {                          # Dict[str, int]: retry policy for different types of exceptions
    "AuthenticationErrorRetries": 3,
    "TimeoutErrorRetries": 3,
    "RateLimitErrorRetries": 3,
    "ContentPolicyViolationErrorRetries": 4,
    "InternalServerErrorRetries": 4
  }
  allowed_fails_policy: {
    "BadRequestErrorAllowedFails": 1000, # Allow 1000 BadRequestErrors before cooling down a deployment
    "AuthenticationErrorAllowedFails": 10, # int 
    "TimeoutErrorAllowedFails": 12, # int 
    "RateLimitErrorAllowedFails": 10000, # int 
    "ContentPolicyViolationErrorAllowedFails": 15, # int 
    "InternalServerErrorAllowedFails": 20, # int 
  }
  content_policy_fallbacks=[{"claude-2": ["my-fallback-model"]}] # List[Dict[str, List[str]]]: Fallback model for content policy violations
  fallbacks=[{"claude-2": ["my-fallback-model"]}] # List[Dict[str, List[str]]]: Fallback model for all errors
```

| Name | Type | Description |
| --- | --- | --- |
| routing\_strategy | string | The strategy used for routing requests. Options: "simple-shuffle", "least-busy", "usage-based-routing", "latency-based-routing". Default is "simple-shuffle". [More information here](https://docs.litellm.ai/docs/routing) |
| redis\_host | string | The host address for the Redis server. **Only set this if you have multiple instances of LiteLLM Proxy and want current tpm/rpm tracking to be shared across them** |
| redis\_password | string | The password for the Redis server. **Only set this if you have multiple instances of LiteLLM Proxy and want current tpm/rpm tracking to be shared across them** |
| redis\_port | string | The port number for the Redis server. **Only set this if you have multiple instances of LiteLLM Proxy and want current tpm/rpm tracking to be shared across them** |
| enable\_pre\_call\_check | boolean | If true, checks if a call is within the model's context window before making the call. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| content\_policy\_fallbacks | array of objects | Specifies fallback models for content policy violations. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| fallbacks | array of objects | Specifies fallback models for all types of errors. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| enable\_tag\_filtering | boolean | If true, uses tag based routing for requests [Tag Based Routing](https://docs.litellm.ai/docs/proxy/tag_routing) |
| cooldown\_time | integer | The duration (in seconds) to cooldown a model if it exceeds the allowed failures. |
| disable\_cooldowns | boolean | If true, disables cooldowns for all models. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| retry\_policy | object | Specifies the number of retries for different types of exceptions. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| allowed\_fails | integer | The number of failures allowed before cooling down a model. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| allowed\_fails\_policy | object | Specifies the number of allowed failures for different error types before cooling down a deployment. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| default\_max\_parallel\_requests | Optional\[int\] | The default maximum number of parallel requests for a deployment. |
| default\_priority | (Optional\[int\]) | The default priority for a request. Only for '.scheduler\_acompletion()'. Default is None. |
| polling\_interval | (Optional\[float\]) | frequency of polling queue. Only for '.scheduler\_acompletion()'. Default is 3ms. |
| max\_fallbacks | Optional\[int\] | The maximum number of fallbacks to try before exiting the call. Defaults to 5. |
| default\_litellm\_params | Optional\[dict\] | The default litellm parameters to add to all requests (e.g. `temperature`, `max_tokens`). |
| timeout | Optional\[float\] | The default timeout for a request. Default is 10 minutes. |
| stream\_timeout | Optional\[float\] | The default timeout for a streaming request. If not set, the 'timeout' value is used. |
| debug\_level | Literal\["DEBUG", "INFO"\] | The debug level for the logging library in the router. Defaults to "INFO". |
| client\_ttl | int | Time-to-live for cached clients in seconds. Defaults to 3600. |
| cache\_kwargs | dict | Additional keyword arguments for the cache initialization. |
| routing\_strategy\_args | dict | Additional keyword arguments for the routing strategy - e.g. lowest latency routing default ttl |
| model\_group\_alias | dict | Model group alias mapping. E.g. `{"claude-3-haiku": "claude-3-haiku-20240229"}` |
| num\_retries | int | Number of retries for a request. Defaults to 3. |
| default\_fallbacks | Optional\[List\[str\]\] | Fallbacks to try if no model group-specific fallbacks are defined. |
| caching\_groups | Optional\[List\[tuple\]\] | List of model groups for caching across model groups. Defaults to None. - e.g. caching\_groups=\[("openai-gpt-3.5-turbo", "azure-gpt-3.5-turbo")\] |
| alerting\_config | AlertingConfig | \[SDK-only arg\] Slack alerting configuration. Defaults to None. [Further Docs](https://docs.litellm.ai/docs/routing#alerting-) |
| assistants\_config | AssistantsConfig | Set on proxy via `assistant_settings`. [Further docs](https://docs.litellm.ai/docs/assistants) |
| set\_verbose | boolean | [DEPRECATED PARAM - see debug docs](https://docs.litellm.ai/docs/proxy/debugging) If true, sets the logging level to verbose. |
| retry\_after | int | Time to wait before retrying a request in seconds. Defaults to 0. If `x-retry-after` is received from LLM API, this value is overridden. |
| provider\_budget\_config | ProviderBudgetConfig | Provider budget configuration. Use this to set llm\_provider budget limits. example $100/day to OpenAI, $100/day to Azure, etc. Defaults to None. [Further Docs](https://docs.litellm.ai/docs/proxy/provider_budget_routing) |
| enable\_pre\_call\_checks | boolean | If true, checks if a call is within the model's context window before making the call. [More information here](https://docs.litellm.ai/docs/proxy/reliability) |
| model\_group\_retry\_policy | Dict\[str, RetryPolicy\] | \[SDK-only arg\] Set retry policy for model groups. |
| context\_window\_fallbacks | List\[Dict\[str, List\[str\]\]\] | Fallback models for context window violations. |
| redis\_url | str | URL for Redis server. **Known performance issue with Redis URL.** |
| cache\_responses | boolean | Flag to enable caching LLM Responses, if cache set under `router_settings`. If true, caches responses. Defaults to False. |
| router\_general\_settings | RouterGeneralSettings | \[SDK-Only\] Router general settings - contains optimizations like 'async\_only\_mode'. [Docs](https://docs.litellm.ai/docs/routing#router-general-settings) |
| optional\_pre\_call\_checks | List\[str\] | List of pre-call checks to add to the router. Currently supported: 'router\_budget\_limiting', 'prompt\_caching' |
| ignore\_invalid\_deployments | boolean | If true, ignores invalid deployments. Default for proxy is True - to prevent invalid models from blocking other models from being loaded. |

### environment variables - Reference

| Name | Description |
| --- | --- |
| ACTIONS\_ID\_TOKEN\_REQUEST\_TOKEN | Token for requesting ID in GitHub Actions |
| ACTIONS\_ID\_TOKEN\_REQUEST\_URL | URL for requesting ID token in GitHub Actions |
| AGENTOPS\_ENVIRONMENT | Environment for AgentOps logging integration |
| AGENTOPS\_API\_KEY | API Key for AgentOps logging integration |
| AGENTOPS\_SERVICE\_NAME | Service Name for AgentOps logging integration |
| AISPEND\_ACCOUNT\_ID | Account ID for AI Spend |
| AISPEND\_API\_KEY | API Key for AI Spend |
| AIOHTTP\_TRUST\_ENV | Flag to enable aiohttp trust environment. When this is set to True, aiohttp will respect HTTP(S)\_PROXY env vars. **Default is False** |
| ALLOWED\_EMAIL\_DOMAINS | List of email domains allowed for access |
| ARIZE\_API\_KEY | API key for Arize platform integration |
| ARIZE\_SPACE\_KEY | Space key for Arize platform |
| ARGILLA\_BATCH\_SIZE | Batch size for Argilla logging |
| ARGILLA\_API\_KEY | API key for Argilla platform |
| ARGILLA\_SAMPLING\_RATE | Sampling rate for Argilla logging |
| ARGILLA\_DATASET\_NAME | Dataset name for Argilla logging |
| ARGILLA\_BASE\_URL | Base URL for Argilla service |
| ATHINA\_API\_KEY | API key for Athina service |
| ATHINA\_BASE\_URL | Base URL for Athina service (defaults to `https://log.athina.ai`) |
| AUTH\_STRATEGY | Strategy used for authentication (e.g., OAuth, API key) |
| ANTHROPIC\_API\_KEY | API key for Anthropic service |
| AWS\_ACCESS\_KEY\_ID | Access Key ID for AWS services |
| AWS\_PROFILE\_NAME | AWS CLI profile name to be used |
| AWS\_REGION\_NAME | Default AWS region for service interactions |
| AWS\_ROLE\_NAME | Role name for AWS IAM usage |
| AWS\_SECRET\_ACCESS\_KEY | Secret Access Key for AWS services |
| AWS\_SESSION\_NAME | Name for AWS session |
| AWS\_WEB\_IDENTITY\_TOKEN | Web identity token for AWS |
| AZURE\_API\_VERSION | Version of the Azure API being used |
| AZURE\_AUTHORITY\_HOST | Azure authority host URL |
| AZURE\_CLIENT\_ID | Client ID for Azure services |
| AZURE\_CLIENT\_SECRET | Client secret for Azure services |
| AZURE\_CODE\_INTERPRETER\_COST\_PER\_SESSION | Cost per session for Azure Code Interpreter service |
| AZURE\_COMPUTER\_USE\_INPUT\_COST\_PER\_1K\_TOKENS | Input cost per 1K tokens for Azure Computer Use service |
| AZURE\_COMPUTER\_USE\_OUTPUT\_COST\_PER\_1K\_TOKENS | Output cost per 1K tokens for Azure Computer Use service |
| AZURE\_TENANT\_ID | Tenant ID for Azure Active Directory |
| AZURE\_USERNAME | Username for Azure services, use in conjunction with AZURE\_PASSWORD for azure ad token with basic username/password workflow |
| AZURE\_PASSWORD | Password for Azure services, use in conjunction with AZURE\_USERNAME for azure ad token with basic username/password workflow |
| AZURE\_FEDERATED\_TOKEN\_FILE | File path to Azure federated token |
| AZURE\_FILE\_SEARCH\_COST\_PER\_GB\_PER\_DAY | Cost per GB per day for Azure File Search service |
| AZURE\_SCOPE | For EntraID Auth, Scope for Azure services, defaults to " [https://cognitiveservices.azure.com/.default](https://cognitiveservices.azure.com/.default) " |
| AZURE\_KEY\_VAULT\_URI | URI for Azure Key Vault |
| AZURE\_OPERATION\_POLLING\_TIMEOUT | Timeout in seconds for Azure operation polling |
| AZURE\_STORAGE\_ACCOUNT\_KEY | The Azure Storage Account Key to use for Authentication to Azure Blob Storage logging |
| AZURE\_STORAGE\_ACCOUNT\_NAME | Name of the Azure Storage Account to use for logging to Azure Blob Storage |
| AZURE\_STORAGE\_FILE\_SYSTEM | Name of the Azure Storage File System to use for logging to Azure Blob Storage. (Typically the Container name) |
| AZURE\_STORAGE\_TENANT\_ID | The Application Tenant ID to use for Authentication to Azure Blob Storage logging |
| AZURE\_STORAGE\_CLIENT\_ID | The Application Client ID to use for Authentication to Azure Blob Storage logging |
| AZURE\_STORAGE\_CLIENT\_SECRET | The Application Client Secret to use for Authentication to Azure Blob Storage logging |
| AZURE\_VECTOR\_STORE\_COST\_PER\_GB\_PER\_DAY | Cost per GB per day for Azure Vector Store service |
| BATCH\_STATUS\_POLL\_INTERVAL\_SECONDS | Interval in seconds for polling batch status. Default is 3600 (1 hour) |
| BATCH\_STATUS\_POLL\_MAX\_ATTEMPTS | Maximum number of attempts for polling batch status. Default is 24 (for 24 hours) |
| BEDROCK\_MAX\_POLICY\_SIZE | Maximum size for Bedrock policy. Default is 75 |
| BERRISPEND\_ACCOUNT\_ID | Account ID for BerriSpend service |
| BRAINTRUST\_API\_KEY | API key for Braintrust integration |
| CACHED\_STREAMING\_CHUNK\_DELAY | Delay in seconds for cached streaming chunks. Default is 0.02 |
| CIRCLE\_OIDC\_TOKEN | OpenID Connect token for CircleCI |
| CIRCLE\_OIDC\_TOKEN\_V2 | Version 2 of the OpenID Connect token for CircleCI |
| CLOUDZERO\_API\_KEY | CloudZero API key for authentication |
| CLOUDZERO\_CONNECTION\_ID | CloudZero connection ID for data submission |
| CLOUDZERO\_TIMEZONE | Timezone for date handling (default: UTC) |
| CONFIG\_FILE\_PATH | File path for configuration file |
| CONFIDENT\_API\_KEY | API key for DeepEval integration |
| CUSTOM\_TIKTOKEN\_CACHE\_DIR | Custom directory for Tiktoken cache |
| CONFIDENT\_API\_KEY | API key for Confident AI (Deepeval) Logging service |
| DATABASE\_HOST | Hostname for the database server |
| DATABASE\_NAME | Name of the database |
| DATABASE\_PASSWORD | Password for the database user |
| DATABASE\_PORT | Port number for database connection |
| DATABASE\_SCHEMA | Schema name used in the database |
| DATABASE\_URL | Connection URL for the database |
| DATABASE\_USER | Username for database connection |
| DATABASE\_USERNAME | Alias for database user |
| DATABRICKS\_API\_BASE | Base URL for Databricks API |
| DAYS\_IN\_A\_MONTH | Days in a month for calculation purposes. Default is 28 |
| DAYS\_IN\_A\_WEEK | Days in a week for calculation purposes. Default is 7 |
| DAYS\_IN\_A\_YEAR | Days in a year for calculation purposes. Default is 365 |
| DD\_BASE\_URL | Base URL for Datadog integration |
| DATADOG\_BASE\_URL | (Alternative to DD\_BASE\_URL) Base URL for Datadog integration |
| \_DATADOG\_BASE\_URL | (Alternative to DD\_BASE\_URL) Base URL for Datadog integration |
| DD\_API\_KEY | API key for Datadog integration |
| DD\_SITE | Site URL for Datadog (e.g., datadoghq.com) |
| DD\_SOURCE | Source identifier for Datadog logs |
| DD\_TRACER\_STREAMING\_CHUNK\_YIELD\_RESOURCE | Resource name for Datadog tracing of streaming chunk yields. Default is "streaming.chunk.yield" |
| DD\_ENV | Environment identifier for Datadog logs. Only supported for `datadog_llm_observability` callback |
| DD\_SERVICE | Service identifier for Datadog logs. Defaults to "litellm-server" |
| DD\_VERSION | Version identifier for Datadog logs. Defaults to "unknown" |
| DEBUG\_OTEL | Enable debug mode for OpenTelemetry |
| DEFAULT\_ALLOWED\_FAILS | Maximum failures allowed before cooling down a model. Default is 3 |
| DEFAULT\_ANTHROPIC\_CHAT\_MAX\_TOKENS | Default maximum tokens for Anthropic chat completions. Default is 4096 |
| DEFAULT\_BATCH\_SIZE | Default batch size for operations. Default is 512 |
| DEFAULT\_COOLDOWN\_TIME\_SECONDS | Duration in seconds to cooldown a model after failures. Default is 5 |
| DEFAULT\_CRON\_JOB\_LOCK\_TTL\_SECONDS | Time-to-live for cron job locks in seconds. Default is 60 (1 minute) |
| DEFAULT\_FAILURE\_THRESHOLD\_PERCENT | Threshold percentage of failures to cool down a deployment. Default is 0.5 (50%) |
| DEFAULT\_FLUSH\_INTERVAL\_SECONDS | Default interval in seconds for flushing operations. Default is 5 |
| DEFAULT\_HEALTH\_CHECK\_INTERVAL | Default interval in seconds for health checks. Default is 300 (5 minutes) |
| DEFAULT\_IMAGE\_HEIGHT | Default height for images. Default is 300 |
| DEFAULT\_IMAGE\_TOKEN\_COUNT | Default token count for images. Default is 250 |
| DEFAULT\_IMAGE\_WIDTH | Default width for images. Default is 300 |
| DEFAULT\_IN\_MEMORY\_TTL | Default time-to-live for in-memory cache in seconds. Default is 5 |
| DEFAULT\_MANAGEMENT\_OBJECT\_IN\_MEMORY\_CACHE\_TTL | Default time-to-live in seconds for management objects (User, Team, Key, Organization) in memory cache. Default is 60 seconds. |
| DEFAULT\_MAX\_LRU\_CACHE\_SIZE | Default maximum size for LRU cache. Default is 16 |
| DEFAULT\_MAX\_RECURSE\_DEPTH | Default maximum recursion depth. Default is 100 |
| DEFAULT\_MAX\_RECURSE\_DEPTH\_SENSITIVE\_DATA\_MASKER | Default maximum recursion depth for sensitive data masker. Default is 10 |
| DEFAULT\_MAX\_RETRIES | Default maximum retry attempts. Default is 2 |
| DEFAULT\_MAX\_TOKENS | Default maximum tokens for LLM calls. Default is 4096 |
| DEFAULT\_MAX\_TOKENS\_FOR\_TRITON | Default maximum tokens for Triton models. Default is 2000 |
| DEFAULT\_MOCK\_RESPONSE\_COMPLETION\_TOKEN\_COUNT | Default token count for mock response completions. Default is 20 |
| DEFAULT\_MOCK\_RESPONSE\_PROMPT\_TOKEN\_COUNT | Default token count for mock response prompts. Default is 10 |
| DEFAULT\_MODEL\_CREATED\_AT\_TIME | Default creation timestamp for models. Default is 1677610602 |
| DEFAULT\_PROMPT\_INJECTION\_SIMILARITY\_THRESHOLD | Default threshold for prompt injection similarity. Default is 0.7 |
| DEFAULT\_POLLING\_INTERVAL | Default polling interval for schedulers in seconds. Default is 0.03 |
| DEFAULT\_REASONING\_EFFORT\_DISABLE\_THINKING\_BUDGET | Default reasoning effort disable thinking budget. Default is 0 |
| DEFAULT\_REASONING\_EFFORT\_HIGH\_THINKING\_BUDGET | Default high reasoning effort thinking budget. Default is 4096 |
| DEFAULT\_REASONING\_EFFORT\_LOW\_THINKING\_BUDGET | Default low reasoning effort thinking budget. Default is 1024 |
| DEFAULT\_REASONING\_EFFORT\_MEDIUM\_THINKING\_BUDGET | Default medium reasoning effort thinking budget. Default is 2048 |
| DEFAULT\_REDIS\_SYNC\_INTERVAL | Default Redis synchronization interval in seconds. Default is 1 |
| DEFAULT\_REPLICATE\_GPU\_PRICE\_PER\_SECOND | Default price per second for Replicate GPU. Default is 0.001400 |
| DEFAULT\_REPLICATE\_POLLING\_DELAY\_SECONDS | Default delay in seconds for Replicate polling. Default is 1 |
| DEFAULT\_REPLICATE\_POLLING\_RETRIES | Default number of retries for Replicate polling. Default is 5 |
| DEFAULT\_SQS\_BATCH\_SIZE | Default batch size for SQS logging. Default is 512 |
| DEFAULT\_SQS\_FLUSH\_INTERVAL\_SECONDS | Default flush interval for SQS logging. Default is 10 |
| DEFAULT\_S3\_BATCH\_SIZE | Default batch size for S3 logging. Default is 512 |
| DEFAULT\_S3\_FLUSH\_INTERVAL\_SECONDS | Default flush interval for S3 logging. Default is 10 |
| DEFAULT\_SLACK\_ALERTING\_THRESHOLD | Default threshold for Slack alerting. Default is 300 |
| DEFAULT\_SOFT\_BUDGET | Default soft budget for LiteLLM proxy keys. Default is 50.0 |
| DEFAULT\_TRIM\_RATIO | Default ratio of tokens to trim from prompt end. Default is 0.75 |
| DIRECT\_URL | Direct URL for service endpoint |
| DISABLE\_ADMIN\_UI | Toggle to disable the admin UI |
| DISABLE\_AIOHTTP\_TRANSPORT | Flag to disable aiohttp transport. When this is set to True, litellm will use httpx instead of aiohttp. **Default is False** |
| DISABLE\_AIOHTTP\_TRUST\_ENV | Flag to disable aiohttp trust environment. When this is set to True, litellm will not trust the environment for aiohttp eg. `HTTP_PROXY` and `HTTPS_PROXY` environment variables will not be used when this is set to True. **Default is False** |
| DISABLE\_SCHEMA\_UPDATE | Toggle to disable schema updates |
| DOCS\_DESCRIPTION | Description text for documentation pages |
| DOCS\_FILTERED | Flag indicating filtered documentation |
| DOCS\_TITLE | Title of the documentation pages |
| DOCS\_URL | The path to the Swagger API documentation. **By default this is "/"** |
| EMAIL\_LOGO\_URL | URL for the logo used in emails |
| EMAIL\_SUPPORT\_CONTACT | Support contact email address |
| EMAIL\_SIGNATURE | Custom HTML footer/signature for all emails. Can include HTML tags for formatting and links. |
| EMAIL\_SUBJECT\_INVITATION | Custom subject template for invitation emails. |
| EMAIL\_SUBJECT\_KEY\_CREATED | Custom subject template for key creation emails. |
| EXPERIMENTAL\_MULTI\_INSTANCE\_RATE\_LIMITING | Flag to enable new multi-instance rate limiting. **Default is False** |
| FIREWORKS\_AI\_4\_B | Size parameter for Fireworks AI 4B model. Default is 4 |
| FIREWORKS\_AI\_16\_B | Size parameter for Fireworks AI 16B model. Default is 16 |
| FIREWORKS\_AI\_56\_B\_MOE | Size parameter for Fireworks AI 56B MOE model. Default is 56 |
| FIREWORKS\_AI\_80\_B | Size parameter for Fireworks AI 80B model. Default is 80 |
| FIREWORKS\_AI\_176\_B\_MOE | Size parameter for Fireworks AI 176B MOE model. Default is 176 |
| FUNCTION\_DEFINITION\_TOKEN\_COUNT | Token count for function definitions. Default is 9 |
| GALILEO\_BASE\_URL | Base URL for Galileo platform |
| GALILEO\_PASSWORD | Password for Galileo authentication |
| GALILEO\_PROJECT\_ID | Project ID for Galileo usage |
| GALILEO\_USERNAME | Username for Galileo authentication |
| GOOGLE\_SECRET\_MANAGER\_PROJECT\_ID | Project ID for Google Secret Manager |
| GCS\_BUCKET\_NAME | Name of the Google Cloud Storage bucket |
| GCS\_PATH\_SERVICE\_ACCOUNT | Path to the Google Cloud service account JSON file |
| GCS\_FLUSH\_INTERVAL | Flush interval for GCS logging (in seconds). Specify how often you want a log to be sent to GCS. **Default is 20 seconds** |
| GCS\_BATCH\_SIZE | Batch size for GCS logging. Specify after how many logs you want to flush to GCS. If `BATCH_SIZE` is set to 10, logs are flushed every 10 logs. **Default is 2048** |
| GCS\_PUBSUB\_TOPIC\_ID | PubSub Topic ID to send LiteLLM SpendLogs to. |
| GCS\_PUBSUB\_PROJECT\_ID | PubSub Project ID to send LiteLLM SpendLogs to. |
| GENERIC\_AUTHORIZATION\_ENDPOINT | Authorization endpoint for generic OAuth providers |
| GENERIC\_CLIENT\_ID | Client ID for generic OAuth providers |
| GENERIC\_CLIENT\_SECRET | Client secret for generic OAuth providers |
| GENERIC\_CLIENT\_STATE | State parameter for generic client authentication |
| GENERIC\_SSO\_HEADERS | Comma-separated list of additional headers to add to the request - e.g. Authorization=Bearer `<token>`, Content-Type=application/json, etc. |
| GENERIC\_INCLUDE\_CLIENT\_ID | Include client ID in requests for OAuth |
| GENERIC\_SCOPE | Scope settings for generic OAuth providers |
| GENERIC\_TOKEN\_ENDPOINT | Token endpoint for generic OAuth providers |
| GENERIC\_USER\_DISPLAY\_NAME\_ATTRIBUTE | Attribute for user's display name in generic auth |
| GENERIC\_USER\_EMAIL\_ATTRIBUTE | Attribute for user's email in generic auth |
| GENERIC\_USER\_FIRST\_NAME\_ATTRIBUTE | Attribute for user's first name in generic auth |
| GENERIC\_USER\_ID\_ATTRIBUTE | Attribute for user ID in generic auth |
| GENERIC\_USER\_LAST\_NAME\_ATTRIBUTE | Attribute for user's last name in generic auth |
| GENERIC\_USER\_PROVIDER\_ATTRIBUTE | Attribute specifying the user's provider |
| GENERIC\_USER\_ROLE\_ATTRIBUTE | Attribute specifying the user's role |
| GENERIC\_USERINFO\_ENDPOINT | Endpoint to fetch user information in generic OAuth |
| GALILEO\_BASE\_URL | Base URL for Galileo platform |
| GALILEO\_PASSWORD | Password for Galileo authentication |
| GALILEO\_PROJECT\_ID | Project ID for Galileo usage |
| GALILEO\_USERNAME | Username for Galileo authentication |
| GITHUB\_COPILOT\_TOKEN\_DIR | Directory to store GitHub Copilot token for `github_copilot` llm provider |
| GITHUB\_COPILOT\_API\_KEY\_FILE | File to store GitHub Copilot API key for `github_copilot` llm provider |
| GITHUB\_COPILOT\_ACCESS\_TOKEN\_FILE | File to store GitHub Copilot access token for `github_copilot` llm provider |
| GREENSCALE\_API\_KEY | API key for Greenscale service |
| GREENSCALE\_ENDPOINT | Endpoint URL for Greenscale service |
| GOOGLE\_APPLICATION\_CREDENTIALS | Path to Google Cloud credentials JSON file |
| GOOGLE\_CLIENT\_ID | Client ID for Google OAuth |
| GOOGLE\_CLIENT\_SECRET | Client secret for Google OAuth |
| GOOGLE\_KMS\_RESOURCE\_NAME | Name of the resource in Google KMS |
| GUARDRAILS\_AI\_API\_BASE | Base URL for Guardrails AI API |
| HEALTH\_CHECK\_TIMEOUT\_SECONDS | Timeout in seconds for health checks. Default is 60 |
| HF\_API\_BASE | Base URL for Hugging Face API |
| HCP\_VAULT\_ADDR | Address for [Hashicorp Vault Secret Manager](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HCP\_VAULT\_CLIENT\_CERT | Path to client certificate for [Hashicorp Vault Secret Manager](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HCP\_VAULT\_CLIENT\_KEY | Path to client key for [Hashicorp Vault Secret Manager](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HCP\_VAULT\_NAMESPACE | Namespace for [Hashicorp Vault Secret Manager](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HCP\_VAULT\_TOKEN | Token for [Hashicorp Vault Secret Manager](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HCP\_VAULT\_CERT\_ROLE | Role for [Hashicorp Vault Secret Manager Auth](https://docs.litellm.ai/docs/secret#hashicorp-vault) |
| HELICONE\_API\_KEY | API key for Helicone service |
| HELICONE\_API\_BASE | Base URL for Helicone service, defaults to `https://api.helicone.ai` |
| HOSTNAME | Hostname for the server, this will be [emitted to `datadog` logs](https://docs.litellm.ai/docs/proxy/logging#datadog) |
| HOURS\_IN\_A\_DAY | Hours in a day for calculation purposes. Default is 24 |
| HUGGINGFACE\_API\_BASE | Base URL for Hugging Face API |
| HUGGINGFACE\_API\_KEY | API key for Hugging Face API |
| HUMANLOOP\_PROMPT\_CACHE\_TTL\_SECONDS | Time-to-live in seconds for cached prompts in Humanloop. Default is 60 |
| IAM\_TOKEN\_DB\_AUTH | IAM token for database authentication |
| INITIAL\_RETRY\_DELAY | Initial delay in seconds for retrying requests. Default is 0.5 |
| JITTER | Jitter factor for retry delay calculations. Default is 0.75 |
| JSON\_LOGS | Enable JSON formatted logging |
| JWT\_AUDIENCE | Expected audience for JWT tokens |
| JWT\_PUBLIC\_KEY\_URL | URL to fetch public key for JWT verification |
| LAGO\_API\_BASE | Base URL for Lago API |
| LAGO\_API\_CHARGE\_BY | Parameter to determine charge basis in Lago |
| LAGO\_API\_EVENT\_CODE | Event code for Lago API events |
| LAGO\_API\_KEY | API key for accessing Lago services |
| LANGFUSE\_DEBUG | Toggle debug mode for Langfuse |
| LANGFUSE\_FLUSH\_INTERVAL | Interval for flushing Langfuse logs |
| LANGFUSE\_TRACING\_ENVIRONMENT | Environment for Langfuse tracing |
| LANGFUSE\_HOST | Host URL for Langfuse service |
| LANGFUSE\_PUBLIC\_KEY | Public key for Langfuse authentication |
| LANGFUSE\_RELEASE | Release version of Langfuse integration |
| LANGFUSE\_SECRET\_KEY | Secret key for Langfuse authentication |
| LANGSMITH\_API\_KEY | API key for Langsmith platform |
| LANGSMITH\_BASE\_URL | Base URL for Langsmith service |
| LANGSMITH\_BATCH\_SIZE | Batch size for operations in Langsmith |
| LANGSMITH\_DEFAULT\_RUN\_NAME | Default name for Langsmith run |
| LANGSMITH\_PROJECT | Project name for Langsmith integration |
| LANGSMITH\_SAMPLING\_RATE | Sampling rate for Langsmith logging |
| LANGTRACE\_API\_KEY | API key for Langtrace service |
| LASSO\_API\_BASE | Base URL for Lasso API |
| LASSO\_API\_KEY | API key for Lasso service |
| LASSO\_USER\_ID | User ID for Lasso service |
| LASSO\_CONVERSATION\_ID | Conversation ID for Lasso service |
| LENGTH\_OF\_LITELLM\_GENERATED\_KEY | Length of keys generated by LiteLLM. Default is 16 |
| LITERAL\_API\_KEY | API key for Literal integration |
| LITERAL\_API\_URL | API URL for Literal service |
| LITERAL\_BATCH\_SIZE | Batch size for Literal operations |
| LITELLM\_DONT\_SHOW\_FEEDBACK\_BOX | Flag to hide feedback box in LiteLLM UI |
| LITELLM\_DROP\_PARAMS | Parameters to drop in LiteLLM requests |
| LITELLM\_MODIFY\_PARAMS | Parameters to modify in LiteLLM requests |
| LITELLM\_EMAIL | Email associated with LiteLLM account |
| LITELLM\_GLOBAL\_MAX\_PARALLEL\_REQUEST\_RETRIES | Maximum retries for parallel requests in LiteLLM |
| LITELLM\_GLOBAL\_MAX\_PARALLEL\_REQUEST\_RETRY\_TIMEOUT | Timeout for retries of parallel requests in LiteLLM |
| LITELLM\_MIGRATION\_DIR | Custom migrations directory for prisma migrations, used for baselining db in read-only file systems. |
| LITELLM\_HOSTED\_UI | URL of the hosted UI for LiteLLM |
| LITELM\_ENVIRONMENT | Environment of LiteLLM Instance, used by logging services. Currently only used by DeepEval. |
| LITELLM\_LICENSE | License key for LiteLLM usage |
| LITELLM\_LOCAL\_MODEL\_COST\_MAP | Local configuration for model cost mapping in LiteLLM |
| LITELLM\_LOG | Enable detailed logging for LiteLLM |
| LITELLM\_MASTER\_KEY | Master key for proxy authentication |
| LITELLM\_MODE | Operating mode for LiteLLM (e.g., production, development) |
| LITELLM\_RATE\_LIMIT\_WINDOW\_SIZE | Rate limit window size for LiteLLM. Default is 60 |
| LITELLM\_SALT\_KEY | Salt key for encryption in LiteLLM |
| LITELLM\_SECRET\_AWS\_KMS\_LITELLM\_LICENSE | AWS KMS encrypted license for LiteLLM |
| LITELLM\_TOKEN | Access token for LiteLLM integration |
| LITELLM\_PRINT\_STANDARD\_LOGGING\_PAYLOAD | If true, prints the standard logging payload to the console - useful for debugging |
| LITELM\_ENVIRONMENT | Environment for LiteLLM Instance. This is currently only logged to DeepEval to determine the environment for DeepEval integration. |
| LOGFIRE\_TOKEN | Token for Logfire logging service |
| MAX\_EXCEPTION\_MESSAGE\_LENGTH | Maximum length for exception messages. Default is 2000 |
| MAX\_IN\_MEMORY\_QUEUE\_FLUSH\_COUNT | Maximum count for in-memory queue flush operations. Default is 1000 |
| MAX\_LONG\_SIDE\_FOR\_IMAGE\_HIGH\_RES | Maximum length for the long side of high-resolution images. Default is 2000 |
| MAX\_REDIS\_BUFFER\_DEQUEUE\_COUNT | Maximum count for Redis buffer dequeue operations. Default is 100 |
| MAX\_SHORT\_SIDE\_FOR\_IMAGE\_HIGH\_RES | Maximum length for the short side of high-resolution images. Default is 768 |
| MAX\_SIZE\_IN\_MEMORY\_QUEUE | Maximum size for in-memory queue. Default is 10000 |
| MAX\_SIZE\_PER\_ITEM\_IN\_MEMORY\_CACHE\_IN\_KB | Maximum size in KB for each item in memory cache. Default is 512 or 1024 |
| MAX\_SPENDLOG\_ROWS\_TO\_QUERY | Maximum number of spend log rows to query. Default is 1,000,000 |
| MAX\_TEAM\_LIST\_LIMIT | Maximum number of teams to list. Default is 20 |
| MAX\_TILE\_HEIGHT | Maximum height for image tiles. Default is 512 |
| MAX\_TILE\_WIDTH | Maximum width for image tiles. Default is 512 |
| MAX\_TOKEN\_TRIMMING\_ATTEMPTS | Maximum number of attempts to trim a token message. Default is 10 |
| MAXIMUM\_TRACEBACK\_LINES\_TO\_LOG | Maximum number of lines to log in traceback in LiteLLM Logs UI. Default is 100 |
| MAX\_RETRY\_DELAY | Maximum delay in seconds for retrying requests. Default is 8.0 |
| MAX\_LANGFUSE\_INITIALIZED\_CLIENTS | Maximum number of Langfuse clients to initialize on proxy. Default is 20. This is set since langfuse initializes 1 thread everytime a client is initialized. We've had an incident in the past where we reached 100% cpu utilization because Langfuse was initialized several times. |
| MIN\_NON\_ZERO\_TEMPERATURE | Minimum non-zero temperature value. Default is 0.0001 |
| MINIMUM\_PROMPT\_CACHE\_TOKEN\_COUNT | Minimum token count for caching a prompt. Default is 1024 |
| MISTRAL\_API\_BASE | Base URL for Mistral API |
| MISTRAL\_API\_KEY | API key for Mistral API |
| MICROSOFT\_CLIENT\_ID | Client ID for Microsoft services |
| MICROSOFT\_CLIENT\_SECRET | Client secret for Microsoft services |
| MICROSOFT\_TENANT | Tenant ID for Microsoft Azure |
| MICROSOFT\_SERVICE\_PRINCIPAL\_ID | Service Principal ID for Microsoft Enterprise Application. (This is an advanced feature if you want litellm to auto-assign members to Litellm Teams based on their Microsoft Entra ID Groups) |
| NO\_DOCS | Flag to disable Swagger UI documentation |
| NO\_REDOC | Flag to disable Redoc documentation |
| NO\_PROXY | List of addresses to bypass proxy |
| NON\_LLM\_CONNECTION\_TIMEOUT | Timeout in seconds for non-LLM service connections. Default is 15 |
| OAUTH\_TOKEN\_INFO\_ENDPOINT | Endpoint for OAuth token info retrieval |
| OPENAI\_BASE\_URL | Base URL for OpenAI API |
| OPENAI\_API\_BASE | Base URL for OpenAI API |
| OPENAI\_API\_KEY | API key for OpenAI services |
| OPENAI\_FILE\_SEARCH\_COST\_PER\_1K\_CALLS | Cost per 1000 calls for OpenAI file search. Default is 0.0025 |
| OPENAI\_ORGANIZATION | Organization identifier for OpenAI |
| OPENID\_BASE\_URL | Base URL for OpenID Connect services |
| OPENID\_CLIENT\_ID | Client ID for OpenID Connect authentication |
| OPENID\_CLIENT\_SECRET | Client secret for OpenID Connect authentication |
| OPENMETER\_API\_ENDPOINT | API endpoint for OpenMeter integration |
| OPENMETER\_API\_KEY | API key for OpenMeter services |
| OPENMETER\_EVENT\_TYPE | Type of events sent to OpenMeter |
| OTEL\_ENDPOINT | OpenTelemetry endpoint for traces |
| OTEL\_EXPORTER\_OTLP\_ENDPOINT | OpenTelemetry endpoint for traces |
| OTEL\_ENVIRONMENT\_NAME | Environment name for OpenTelemetry |
| OTEL\_EXPORTER | Exporter type for OpenTelemetry |
| OTEL\_EXPORTER\_OTLP\_PROTOCOL | Exporter type for OpenTelemetry |
| OTEL\_HEADERS | Headers for OpenTelemetry requests |
| OTEL\_MODEL\_ID | Model ID for OpenTelemetry tracing |
| OTEL\_EXPORTER\_OTLP\_HEADERS | Headers for OpenTelemetry requests |
| OTEL\_SERVICE\_NAME | Service name identifier for OpenTelemetry |
| OTEL\_TRACER\_NAME | Tracer name for OpenTelemetry tracing |
| PAGERDUTY\_API\_KEY | API key for PagerDuty Alerting |
| PANW\_PRISMA\_AIRS\_API\_KEY | API key for PANW Prisma AIRS service |
| PANW\_PRISMA\_AIRS\_API\_BASE | Base URL for PANW Prisma AIRS service |
| PHOENIX\_API\_KEY | API key for Arize Phoenix |
| PHOENIX\_COLLECTOR\_ENDPOINT | API endpoint for Arize Phoenix |
| PHOENIX\_COLLECTOR\_HTTP\_ENDPOINT | API http endpoint for Arize Phoenix |
| PILLAR\_API\_BASE | Base URL for Pillar API Guardrails |
| PILLAR\_API\_KEY | API key for Pillar API Guardrails |
| PILLAR\_ON\_FLAGGED\_ACTION | Action to take when content is flagged ('block' or 'monitor') |
| POD\_NAME | Pod name for the server, this will be [emitted to `datadog` logs](https://docs.litellm.ai/docs/proxy/logging#datadog) as `POD_NAME` |
| PREDIBASE\_API\_BASE | Base URL for Predibase API |
| PRESIDIO\_ANALYZER\_API\_BASE | Base URL for Presidio Analyzer service |
| PRESIDIO\_ANONYMIZER\_API\_BASE | Base URL for Presidio Anonymizer service |
| PROMETHEUS\_BUDGET\_METRICS\_REFRESH\_INTERVAL\_MINUTES | Refresh interval in minutes for Prometheus budget metrics. Default is 5 |
| PROMETHEUS\_FALLBACK\_STATS\_SEND\_TIME\_HOURS | Fallback time in hours for sending stats to Prometheus. Default is 9 |
| PROMETHEUS\_URL | URL for Prometheus service |
| PROMPTLAYER\_API\_KEY | API key for PromptLayer integration |
| PROXY\_ADMIN\_ID | Admin identifier for proxy server |
| PROXY\_BASE\_URL | Base URL for proxy service |
| PROXY\_BATCH\_WRITE\_AT | Time in seconds to wait before batch writing spend logs to the database. Default is 10 |
| PROXY\_BATCH\_POLLING\_INTERVAL | Time in seconds to wait before polling a batch, to check if it's completed. Default is 6000s (1 hour) |
| PROXY\_BUDGET\_RESCHEDULER\_MAX\_TIME | Maximum time in seconds to wait before checking database for budget resets. Default is 605 |
| PROXY\_BUDGET\_RESCHEDULER\_MIN\_TIME | Minimum time in seconds to wait before checking database for budget resets. Default is 597 |
| PROXY\_LOGOUT\_URL | URL for logging out of the proxy service |
| QDRANT\_API\_BASE | Base URL for Qdrant API |
| QDRANT\_API\_KEY | API key for Qdrant service |
| QDRANT\_SCALAR\_QUANTILE | Scalar quantile for Qdrant operations. Default is 0.99 |
| QDRANT\_URL | Connection URL for Qdrant database |
| QDRANT\_VECTOR\_SIZE | Vector size for Qdrant operations. Default is 1536 |
| REDIS\_CONNECTION\_POOL\_TIMEOUT | Timeout in seconds for Redis connection pool. Default is 5 |
| REDIS\_HOST | Hostname for Redis server |
| REDIS\_PASSWORD | Password for Redis service |
| REDIS\_PORT | Port number for Redis server |
| REDIS\_SOCKET\_TIMEOUT | Timeout in seconds for Redis socket operations. Default is 0.1 |
| REDOC\_URL | The path to the Redoc Fast API documentation. **By default this is "/redoc"** |
| REPEATED\_STREAMING\_CHUNK\_LIMIT | Limit for repeated streaming chunks to detect looping. Default is 100 |
| REPLICATE\_MODEL\_NAME\_WITH\_ID\_LENGTH | Length of Replicate model names with ID. Default is 64 |
| REPLICATE\_POLLING\_DELAY\_SECONDS | Delay in seconds for Replicate polling operations. Default is 0.5 |
| REQUEST\_TIMEOUT | Timeout in seconds for requests. Default is 6000 |
| ROUTER\_MAX\_FALLBACKS | Maximum number of fallbacks for router. Default is 5 |
| SECRET\_MANAGER\_REFRESH\_INTERVAL | Refresh interval in seconds for secret manager. Default is 86400 (24 hours) |
| SEPARATE\_HEALTH\_APP | If set to '1', runs health endpoints on a separate ASGI app and port. Default: '0'. |
| SEPARATE\_HEALTH\_PORT | Port for the separate health endpoints app. Only used if SEPARATE\_HEALTH\_APP=1. Default: 4001. |
| SERVER\_ROOT\_PATH | Root path for the server application |
| SET\_VERBOSE | Flag to enable verbose logging |
| SINGLE\_DEPLOYMENT\_TRAFFIC\_FAILURE\_THRESHOLD | Minimum number of requests to consider "reasonable traffic" for single-deployment cooldown logic. Default is 1000 |
| SLACK\_DAILY\_REPORT\_FREQUENCY | Frequency of daily Slack reports (e.g., daily, weekly) |
| SLACK\_WEBHOOK\_URL | Webhook URL for Slack integration |
| SMTP\_HOST | Hostname for the SMTP server |
| SMTP\_PASSWORD | Password for SMTP authentication (do not set if SMTP does not require auth) |
| SMTP\_PORT | Port number for SMTP server |
| SMTP\_SENDER\_EMAIL | Email address used as the sender in SMTP transactions |
| SMTP\_SENDER\_LOGO | Logo used in emails sent via SMTP |
| SMTP\_TLS | Flag to enable or disable TLS for SMTP connections |
| SMTP\_USERNAME | Username for SMTP authentication (do not set if SMTP does not require auth) |
| SPEND\_LOGS\_URL | URL for retrieving spend logs |
| SPEND\_LOG\_CLEANUP\_BATCH\_SIZE | Number of logs deleted per batch during cleanup. Default is 1000 |
| SSL\_CERTIFICATE | Path to the SSL certificate file |
| SSL\_SECURITY\_LEVEL | \[BETA\] Security level for SSL/TLS connections. E.g. `DEFAULT@SECLEVEL=1` |
| SSL\_VERIFY | Flag to enable or disable SSL certificate verification |
| SSL\_CERT\_FILE | Path to the SSL certificate file for custom CA bundle |
| SUPABASE\_KEY | API key for Supabase service |
| SUPABASE\_URL | Base URL for Supabase instance |
| STORE\_MODEL\_IN\_DB | If true, enables storing model + credential information in the DB. |
| SYSTEM\_MESSAGE\_TOKEN\_COUNT | Token count for system messages. Default is 4 |
| TEST\_EMAIL\_ADDRESS | Email address used for testing purposes |
| TOGETHER\_AI\_4\_B | Size parameter for Together AI 4B model. Default is 4 |
| TOGETHER\_AI\_8\_B | Size parameter for Together AI 8B model. Default is 8 |
| TOGETHER\_AI\_21\_B | Size parameter for Together AI 21B model. Default is 21 |
| TOGETHER\_AI\_41\_B | Size parameter for Together AI 41B model. Default is 41 |
| TOGETHER\_AI\_80\_B | Size parameter for Together AI 80B model. Default is 80 |
| TOGETHER\_AI\_110\_B | Size parameter for Together AI 110B model. Default is 110 |
| TOGETHER\_AI\_EMBEDDING\_150\_M | Size parameter for Together AI 150M embedding model. Default is 150 |
| TOGETHER\_AI\_EMBEDDING\_350\_M | Size parameter for Together AI 350M embedding model. Default is 350 |
| TOOL\_CHOICE\_OBJECT\_TOKEN\_COUNT | Token count for tool choice objects. Default is 4 |
| UI\_LOGO\_PATH | Path to the logo image used in the UI |
| UI\_PASSWORD | Password for accessing the UI |
| UI\_USERNAME | Username for accessing the UI |
| UPSTREAM\_LANGFUSE\_DEBUG | Flag to enable debugging for upstream Langfuse |
| UPSTREAM\_LANGFUSE\_HOST | Host URL for upstream Langfuse service |
| UPSTREAM\_LANGFUSE\_PUBLIC\_KEY | Public key for upstream Langfuse authentication |
| UPSTREAM\_LANGFUSE\_RELEASE | Release version identifier for upstream Langfuse |
| UPSTREAM\_LANGFUSE\_SECRET\_KEY | Secret key for upstream Langfuse authentication |
| USE\_AWS\_KMS | Flag to enable AWS Key Management Service for encryption |
| USE\_PRISMA\_MIGRATE | Flag to use prisma migrate instead of prisma db push. Recommended for production environments. |
| WEBHOOK\_URL | URL for receiving webhooks from external services |
| SPEND\_LOG\_RUN\_LOOPS | Constant for setting how many runs of 1000 batch deletes should spend\_log\_cleanup task run |
| SPEND\_LOG\_CLEANUP\_BATCH\_SIZE | Number of logs deleted per batch during cleanup. Default is 1000 |