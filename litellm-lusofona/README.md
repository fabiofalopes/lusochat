# Lusochat LiteLLM Deployment

This directory contains a Python deployment script for LiteLLM that follows the same principles as the successful Open WebUI shell script approach.

## 🚀 Quick Start

```bash
# Clone and deploy in one command
python deploy_litellm.py
```

This will automatically:
- ✅ Clone upstream LiteLLM repository
- ✅ Apply your custom configurations  
- ✅ Deploy all services with Docker Compose
- ✅ Provide service URLs and management commands

## 📁 Project Structure

```
litellm-lusofona/
├── .litellm-lusofona/          # Custom configurations (overlay approach)
│   ├── config.yaml             # LiteLLM model configuration
│   ├── docker-compose.yml      # Full stack orchestration
│   ├── .env                    # Environment variables (create from env.example)
│   ├── env.example             # Environment template
│   └── README.md               # Configuration documentation
├── deploy_litellm.py           # 🚀 Main deployment script
├── prometheus.yml              # Monitoring configuration
├── .venv/                      # Python virtual environment
└── README.md                   # This file
```

## 🔧 How It Works (Same Philosophy as Open WebUI)

Our approach mirrors the successful Open WebUI deployment pattern:

1. **Clone Upstream**: Fresh clone of LiteLLM repository (never fork)
2. **Configuration Overlay**: Copy custom configs from `.litellm-lusofona/`
3. **Deploy**: Build and run the complete stack with Docker Compose

This keeps upstream code pristine while applying Lusófona-specific configurations.

## 🌟 Deployed Services

After successful deployment, you'll have:

- **🤖 LiteLLM Proxy**: http://localhost:4000 (main API gateway)
- **📊 Grafana Dashboard**: http://localhost:3001 (admin/admin)
- **📈 Prometheus Monitoring**: http://localhost:9090
- **🗄️ PostgreSQL Database**: Internal (port 5432, not exposed)
- **⚡ Redis Cache**: Internal (port 6379)

## 🛠️ Management Commands

```bash
# Check service status
docker compose -p lusochat-litellm ps

# View real-time logs
docker compose -p lusochat-litellm logs -f

# Stop all services
docker compose -p lusochat-litellm down

# Restart specific service
docker compose -p lusochat-litellm restart litellm
```

## ⚙️ Configuration

1. **Environment Setup**: Copy `.litellm-lusofona/env.example` to `.litellm-lusofona/.env`
2. **Model Configuration**: Edit `.litellm-lusofona/config.yaml` for your model servers
3. **Docker Setup**: Modify `.litellm-lusofona/docker-compose.yml` if needed

## 🔄 Updates & Maintenance

To update to the latest LiteLLM version:
```bash
python deploy_litellm.py  # Will prompt to remove old clone and get fresh upstream
```

Your custom configurations in `.litellm-lusofona/` remain untouched.

## 🎯 Why This Approach?

| Aspect | Our Approach | Alternative (Fork) |
|--------|-------------|-------------------|
| **Upstream Sync** | ✅ Always latest | ❌ Manual merge conflicts |
| **Customization** | ✅ Clean overlay | ❌ Mixed with upstream |
| **Maintenance** | ✅ Low effort | ❌ High maintenance |
| **Upgrades** | ✅ Automatic | ❌ Complex rebasing |

## 🚦 Prerequisites

- Python 3.7+
- Docker & Docker Compose
- Git

The deployment script will verify these automatically.

## 📚 Related Projects

This deployment follows the same successful pattern as:
- **Lusochat Open WebUI**: Shell script approach for UI customization  
- **LiteLLM Proxy**: Python script approach for service configuration

Both maintain the core principle: **Apply customizations at deployment time, never fork upstream.** 