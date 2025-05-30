# LiteLLM Proxy Setup Guide for Local llama.cpp Servers
## 1. Docker Compose Configuration (reference: docker-compose.yml startLine: 256-273)

```yaml
version: '3.6'
services:
  litellm:
    image: ghcr.io/berriai/litellm:latest
    ports:
      - "4000:4000"
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./.env:/app/.env
    command: litellm --config /app/config.yaml --port 4000
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: litellm
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

## 2. Environment File (.env)

```env
# Master key for proxy authentication (reference: README.md startLine: 260-267)
LITELLM_MASTER_KEY="sk-1234"
LITELLM_SALT_KEY="your-random-salt-key"
# For local llama.cpp servers (no API key needed)
OPENAI_API_KEY="none"
```

## 3. Model Configuration (config.yaml)

```yaml
model_list:
  - model_name: DeepSeek-Llama-8B
    litellm_params:
      model: openai/deepseek-llama
      api_base: http://192.168.108.161:8080
      api_key: null  # Must be explicit null for no auth
      max_tokens: 4096
  - model_name: DeepSeek-Qwen-32B
    litellm_params:
      model: openai/deepseek-qwen
      api_base: http://192.168.108.164:8080
      api_key: null
      max_tokens: 8192
  - model_name: Mistral-Small-Instruct
    litellm_params:
      model: openai/mistral-instruct
      api_base: http://192.168.108.165:8080
      api_key: null
      temperature: 0.7
  - model_name: Janus-Pro-7B
    litellm_params:
      model: openai/janus-pro
      api_base: http://192.168.108.167:8080
      api_key: null
      top_p: 0.9
```

## Critical Fixes from Error Analysis
1. **Null API Keys**: Explicit `null` values for local endpoints (reference: openai_compatible.md startLine: 59-63)
2. **Docker Volumes**: Uncommented volume mounts for config files
3. **Master Key Setup**: Required for proxy authentication layer
4. **OpenAI Compatibility**: Using `openai/` prefix for local endpoints

## Validation Test

```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="sk-1234"  # Match LITELLM_MASTER_KEY
)
response = client.chat.completions.create(
    model="DeepSeek-Llama-8B",
    messages=[{"role": "user", "content": "Explain LiteLLM proxy setup"}]
)
print(response.choices[0].message.content)
```
