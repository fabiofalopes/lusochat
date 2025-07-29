# 🗂️ Modular LiteLLM Configuration Guide

This guide explains the new modular configuration structure for the Lusófona LiteLLM deployment, following best practices for organized and maintainable proxy configurations.

## 📁 New Directory Structure

```
.litellm-lusofona/
├── config.yaml                    # 🎯 Main configuration (uses include directive)
├── config-monolithic-backup.yaml  # 📦 Backup of original config
│
├── models/                        # 🤖 Model configurations by provider
│   ├── on-premise.yaml           # Internal Lusófona infrastructure
│   ├── groq.yaml                 # Groq API models
│   └── sambanova.yaml            # SambaNova API models
│
├── settings/                      # ⚙️ LiteLLM settings
│   ├── litellm.yaml              # Core LiteLLM settings
│   ├── router.yaml               # Load balancing & routing
│   └── general.yaml              # General proxy settings
│
└── [other files...]              # Docker, env, docs, etc.
```

## 🚀 Key Benefits

### ✅ **Improved Organization**
- **Provider-based separation**: Each model provider has its own file
- **Settings separation**: Different types of settings in dedicated files
- **Clear responsibility**: Each file has a single, clear purpose

### ✅ **Better Maintainability**
- **Easier to add new models**: Just edit the appropriate provider file
- **Isolated changes**: Modify one provider without affecting others
- **Reduced conflicts**: Multiple team members can work on different providers

### ✅ **Enhanced Readability**
- **Smaller files**: Each file is focused and easier to understand
- **Better documentation**: Each file can have provider-specific comments
- **Logical grouping**: Related configurations are together

## 📝 How to Use

### Adding New Models

#### 1. **On-Premise Models** → Edit `models/on-premise.yaml`
```yaml
model_list:
  - model_name: New-Local-Model-Lusofona-On-Premise
    litellm_params:
      model: openai/new-local-model
      api_base: http://192.168.108.XXX:8080
      api_key: none
      rpm: 100000
    model_info:
      model_alias: new-local-model
      host_node: 192.168.108.XXX
      provider: on-premise
      description: "Description of the new local model"
```

#### 2. **Groq Models** → Edit `models/groq.yaml`
```yaml
model_list:
  - model_name: Groq-New-Model
    litellm_params:
      model: groq/new-model-name
      api_base: https://api.groq.com/openai/v1
      api_key: os.environ/GROQ_API_KEY
      rpm: 100000
    model_info:
      model_alias: Groq-New-Model
      host_node: groq
      provider: groq
      description: "New model via Groq API"
```

#### 3. **SambaNova Models** → Edit `models/sambanova.yaml`
```yaml
model_list:
  - model_name: SambaNova-New-Model
    litellm_params:
      model: sambanova/new-model
      api_base: https://api.sambanova.ai/v1
      api_key: os.environ/SAMBANOVA_API_KEY
      rpm: 100000
      context_window: 32768
      max_tokens: 4096
    model_info:
      model_alias: new-model
      host_node: sambanova
      provider: sambanova
      description: "New model via SambaNova API"
```

#### 4. **New Provider** → Create `models/new-provider.yaml`
```yaml
model_list:
  - model_name: NewProvider-Model
    litellm_params:
      model: newprovider/model-name
      api_base: https://api.newprovider.com/v1
      api_key: os.environ/NEW_PROVIDER_API_KEY
      rpm: 100000
    model_info:
      model_alias: model-name
      host_node: newprovider
      provider: newprovider
      description: "Model via New Provider API"
```

**Then add to `config.yaml`:**
```yaml
include:
  - models/on-premise.yaml
  - models/groq.yaml
  - models/sambanova.yaml
  - models/new-provider.yaml    # 👈 Add this line
  - settings/litellm.yaml
  - settings/router.yaml
  - settings/general.yaml
```

### Modifying Settings

#### **LiteLLM Core Settings** → Edit `settings/litellm.yaml`
```yaml
litellm_settings:
  callbacks: ["prometheus", "langfuse"]  # Add more callbacks
  drop_params: True
  num_retries: 5                         # Increase retries
  request_timeout: 60                    # Increase timeout
```

#### **Load Balancing** → Edit `settings/router.yaml`
```yaml
router_settings:
  routing_strategy: "usage-based-routing"  # Change strategy
  redis_host: redis
  redis_port: 6379
  timeout: 45                             # Increase timeout
```

#### **General Settings** → Edit `settings/general.yaml`
```yaml
general_settings:
  user_header_name: X-OpenWebUI-User-Id
  master_key: sk-your-secret-key         # Add authentication
```

## 🔄 Migration from Monolithic Config

Your original configuration has been preserved as `config-monolithic-backup.yaml`. The new modular structure is functionally equivalent but better organized.

### **What Changed:**
- ✅ **Same models**: All your existing models are preserved
- ✅ **Same settings**: All your settings are preserved
- ✅ **Same functionality**: Everything works exactly the same
- ✅ **Better organization**: Models grouped by provider, settings separated

### **What to Update:**
- 🔄 **Your deployment process**: Uses the same `config.yaml` file
- 🔄 **Your model management**: Now easier with separate provider files
- 🔄 **Your team workflow**: Multiple people can edit different providers

## 🛠️ Deployment

The deployment process remains exactly the same:

```bash
# Deploy (same as before)
python deploy_litellm.py

# Update configuration (same as before)
python deploy_litellm.py --update-config
```

The `deploy_litellm.py` script automatically handles the new structure because it still uses `config.yaml` as the main file.

## 🔍 Validation

To verify your configuration is working correctly:

1. **Check file structure:**
   ```bash
   ls -la models/ settings/
   ```

2. **Test configuration:**
   ```bash
   # In the upstream LiteLLM directory
   litellm --config config.yaml --dry-run
   ```

3. **Check logs after deployment:**
   ```bash
   docker compose -p lusochat-litellm logs litellm
   ```

Look for: `LiteLLM: Proxy initialized with Config, Set models:` in the logs.

## 📊 Current Model Inventory

### **🏢 On-Premise Models** (4 models)
- `gemma-3n-E4B-Lusofona-On-Premise` → 192.168.108.161:8080
- `Mistral-Small-3.2-24B-Lusofona-On-Premise` → 192.168.108.162:8080
- `Magistral-Small-2506-Lusofona-On-Premise` → 192.168.108.164:8080
- `Qwen2.5-VL-7B-Lusofona-On-Premise` → 192.168.108.166:11434

### **⚡ Groq Models** (10 models)
- Llama 3.3 70B, Llama 3.1 8B, Llama 4 variants
- Mistral Saba 24B, DeepSeek Llama 70B
- Moonshot Kimi K2, Qwen3 32B
- Compound Beta variants

### **🚀 SambaNova Models** (10 models)
- DeepSeek R1, DeepSeek V3, DeepSeek R1 Distill
- Meta Llama 3.3 70B, Meta Llama 3.1 8B
- Llama 4 Maverick, Whisper Large v3
- Qwen3 32B, Llama 3.3 Swallow, E5 Mistral

**Total: 24 models across 3 providers**

## 🆘 Troubleshooting

### **Include Files Not Found**
```
ERROR: Could not find include file: models/provider.yaml
```
**Solution:** Check file paths relative to main `config.yaml`

### **Models Not Loading**
```
ERROR: No models found in configuration
```
**Solution:** Verify each included file has proper `model_list:` structure

### **Syntax Errors**
```
ERROR: Invalid YAML syntax
```
**Solution:** Validate YAML syntax in each file:
```bash
python -c "import yaml; yaml.safe_load(open('models/provider.yaml'))"
```

## 📚 References

- [LiteLLM Include Documentation](https://docs.litellm.ai/docs/proxy/configs#include-config-files)
- [LiteLLM Model Configuration](https://docs.litellm.ai/docs/proxy/configs)
- [YAML Best Practices](https://yaml.org/spec/1.2.2/)

---

**Next Steps:**
1. ✅ Test the new configuration
2. ✅ Update team documentation
3. ✅ Train team on new structure
4. 🔄 Consider implementing CI/CD validation for config files 