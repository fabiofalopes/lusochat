# Lusochat LiteLLM Python Deployment

This directory contains a Python-based deployment script for LiteLLM that follows the same principles as the Open WebUI shell script approach.

## What We Have

```
litellm-lusofona/
├── .litellm-lusofona/          # Our custom configurations (like .lusochat-ldap)
│   ├── config.yaml             # LiteLLM model configuration
│   ├── docker-compose.yml      # Docker orchestration
│   ├── Dockerfile              # Custom build
│   └── .env                    # Environment variables
├── deploy_litellm.py           # Simple Python deployment script ⭐
├── .venv/                      # Python virtual environment
└── README.md                   # This file
```

## How It Works (Same as Open WebUI Script)

1. **Clone Upstream**: Clones fresh LiteLLM repository (like shell script clones Open WebUI)
2. **Copy Configs**: Copies our custom files from `.litellm-lusofona/` to the cloned repo
3. **Build & Deploy**: Uses Docker Compose to build and deploy services

## Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run deployment
python deploy_litellm.py
```

The script will:
- ✅ Check for required tools (git, docker)
- ✅ Handle existing directories (ask to remove/reuse)
- ✅ Clone upstream LiteLLM repository
- ✅ Copy your custom configurations
- ✅ Build and deploy with Docker Compose

## Why Python Instead of Shell?

Both approaches work great! We created this Python version to:
- Better handle YAML configuration files
- Provide more structured error handling
- Make it easier to extend with validation
- Show how the same principles work in different languages

## Comparison

| Aspect | Open WebUI (Shell) | LiteLLM (Python) |
|--------|-------------------|------------------|
| **Approach** | Clone → Modify files → Build | Clone → Copy configs → Build |
| **Customization** | Direct file editing | Configuration overlay |
| **Language** | Bash | Python |
| **Best for** | UI customizations | Service configuration |

Both follow the same core principle: **Don't fork upstream, apply customizations at deployment time.**

## Testing

The script has been tested and successfully:
- ✅ Clones LiteLLM repository
- ✅ Copies all custom configuration files
- ✅ Starts Docker build process
- ✅ Handles existing directories properly
- ✅ Provides clear user feedback

## Next Steps

1. Test full deployment when ready
2. Add validation features if needed
3. Extend with health checks
4. Consider CI/CD integration 