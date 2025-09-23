# Modifications & Customization Tracking for `.litellm-lusofona`

## Pu### G### Known Limitations
- **Groq Whisper Audio Transcription**: Groq Whisper models (`groq/whisper-large-v3`) are configured in our model list but currently don't work properly through the LiteLLM proxy due to internal parameter handling issues. Use other providers (OpenAI, Deepgram, etc.) for audio transcription, or configure OpenWebUI to use Groq directly for STT.

---per Fix – Details
- Context: Groq provides OpenAI-compatible `/v1/audio/transcriptions`, but LiteLLM must apply provider-specific configuration for audio transcription to enforce safe defaults (notably `response_format=verbose_json` for duration/cost handling).
- Change 1: We ensure `ProviderConfigManager.get_provider_audio_transcription_config()` returns `OpenAIWhisperAudioTranscriptionConfig()` for `LlmProviders.GROQ`.
- Change 2: Fixed incorrect function call in `get_optional_params_transcription()` where `add_provider_specific_params_to_optional_params` was called with non-existent parameters `model_params_json` and `model_params_class_name` instead of the correct `openai_params` and `additional_drop_params`.
- Where: `litellm-upstream/litellm/utils.py` (patched automatically by our `deploy_litellm.py`).
- Automation: The deployment script runs `apply_groq_whisper_fix()` after cloning/pulling upstream. It's idempotent and skips if upstream already contains the fixes.
- Removal: When upstream includes these fixes, the patch will no-op and can be removed from the script/notes.This folder contains all custom configuration files for the `litellm-lusofona` deployment. The goal is to keep upstream (main repo) code untouched, making it easy to sync with the main project while maintaining your own customizations.

---

## Current Strategy: Configuration Overlay
**We use a "deployment-time overlay" approach:**
- Clone fresh upstream LiteLLM repository 
- Copy our custom configs from `.litellm-lusofona/` over the defaults
- Deploy using Docker Compose with the upstream image

**This differs from a fork approach** - we don't modify upstream code, just overlay configurations.

---

## What Has Been Changed
- **docker-compose.yml**: Custom Compose file with PostgreSQL, Redis, Grafana, and Prometheus integration
- **config.yaml**: LiteLLM model configuration for Lusófona's model servers (192.168.108.161-166)
- **.env**: Environment variables for passwords, settings, and customization
- **env.example**: Template for required environment variables
- **Groq Whisper Fix (utils.py)**: Until upstream includes it, we add a provider mapping so Groq Whisper uses the OpenAI Whisper audio transcription config. This ensures correct parameter defaults (like `response_format=verbose_json`) and compatibility with Groq's OpenAI-style endpoints.

---

## How to Deploy

### Using the Python Deployment Script (Recommended)
```bash
python deploy_litellm.py
```

This will:
1. Clone upstream LiteLLM repository to `litellm-upstream/`
2. Copy custom configs from `.litellm-lusofona/`
 3. Apply local patches (including Groq Whisper audio transcription mapping)
3. Deploy the full stack with Docker Compose

### Manual Deployment
```bash
# 1. Clone upstream
git clone --depth 1 https://github.com/BerriAI/litellm.git litellm-upstream

# 2. Copy configs
cp .litellm-lusofona/config.yaml litellm-upstream/
cp .litellm-lusofona/docker-compose.yml litellm-upstream/
cp .litellm-lusofona/.env litellm-upstream/

# 3. Deploy
cd litellm-upstream
docker compose -p lusochat-litellm up -d --build
```

---

## Security Notes
- **Database**: PostgreSQL port is NOT exposed to host network (security improvement)
- **Passwords**: Use environment variables from `.env` file, not hardcoded values
- **Required**: Copy `env.example` to `.env` and configure before deployment

---

## Files in this Directory
- `config.yaml` - LiteLLM model configuration
- `docker-compose.yml` - Full stack orchestration
- `.env` - Environment variables (create from env.example)
- `env.example` - Template for environment variables  
- `README.md` - Usage documentation
- `NOTE_MODIFICATIONS.md` - This file

### Groq Whisper Fix – Details
- Context: Groq provides OpenAI-compatible `/v1/audio/transcriptions`, but LiteLLM must apply provider-specific configuration for audio transcription to enforce safe defaults (notably `response_format=verbose_json` for duration/cost handling).
- Change: We ensure `ProviderConfigManager.get_provider_audio_transcription_config()` returns `OpenAIWhisperAudioTranscriptionConfig()` for `LlmProviders.GROQ`.
- Where: `litellm-upstream/litellm/utils.py` (patched automatically by our `deploy_litellm.py`).
- Automation: The deployment script runs `apply_groq_whisper_fix()` after cloning/pulling upstream. It’s idempotent and skips if upstream already contains the fix.
- Removal: When upstream includes this mapping, the patch will no-op and can be removed from the script/notes.

---

## Best Practices for Future Maintainers
- **Keep all customizations in `.litellm-lusofona/`** for easy tracking
- **Test changes with the deployment script** before production
- **Update `.env` from `env.example`** when new variables are added
- **Document any new configuration files** in this note
- **When syncing with upstream**, test that our config overlay still works

---

## Contact
For questions about this deployment setup, refer to the deployment script and commit history. 