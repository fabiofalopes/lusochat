# Lusochat LiteLLM Configuration Layer

This directory contains all custom configuration files for the **Lusochat LiteLLM** deployment. Our approach uses a "deployment-time overlay" strategy that keeps upstream code untouched while applying Lusófona-specific configurations.

## 🎯 Strategy: Configuration Overlay (Not Fork)

**We use a clean overlay approach:**
- ✅ Clone fresh upstream LiteLLM repository via `deploy_litellm.py`
- ✅ Copy our custom configs from `.litellm-lusofona/` to the cloned repo
- ✅ Deploy using Docker Compose with the upstream image
- ✅ Keep all customizations separate and trackable

**This is NOT a fork approach** - we never modify upstream code, just overlay configurations.

## 📁 Configuration Files

| File | Purpose | Required |
|------|---------|----------|
| `config.yaml` | LiteLLM model servers configuration | ✅ Yes |
| `docker-compose.yml` | Full stack orchestration | ✅ Yes |
| `.env` | Environment variables & secrets | ✅ Yes (copy from env.example) |
| `env.example` | Template for environment setup | ℹ️ Reference |
| `NOTE_MODIFICATIONS.md` | Change tracking & documentation | ℹ️ Documentation |

## 🚀 How to Deploy

### Method 1: Python Deployment Script (Recommended)
```bash
# From litellm-lusofona/ directory
python deploy_litellm.py
```

This automatically:
1. Clones upstream LiteLLM to `litellm-upstream/`
2. Copies all configs from `.litellm-lusofona/`
3. Deploys full stack with `docker compose -p lusochat-litellm up -d`

### Method 2: Manual Deployment
```bash
# 1. Clone upstream
git clone --depth 1 https://github.com/BerriAI/litellm.git litellm-upstream

# 2. Copy our configurations
cp .litellm-lusofona/config.yaml litellm-upstream/
cp .litellm-lusofona/docker-compose.yml litellm-upstream/
cp .litellm-lusofona/.env litellm-upstream/

# 3. Deploy the stack
cd litellm-upstream
docker compose -p lusochat-litellm up -d --build
```

## 🌐 Deployed Services

After deployment you'll have:

- **🤖 LiteLLM Proxy**: http://localhost:4000 
- **📊 Grafana**: http://localhost:3001 (admin/admin)
- **📈 Prometheus**: http://localhost:9090
- **🗄️ PostgreSQL**: Internal database (not exposed to host)
- **⚡ Redis**: Internal cache

## ⚙️ Configuration Details

### Environment Variables (`.env`)
**Important**: Copy `env.example` to `.env` and configure:
```bash
cp env.example .env
# Edit .env with your actual values
```

Key variables:
- `LITELLM_LICENSE`: Your LiteLLM license key
- `POSTGRES_PASSWORD`: Database password
- `REDIS_PASSWORD`: Cache password
- `GRAFANA_ADMIN_PASSWORD`: Dashboard password

### Model Configuration (`config.yaml`)
Defines available LLM models and routing:
- Model endpoints (192.168.108.161-166)
- Authentication tokens
- Rate limiting
- Load balancing

### Docker Orchestration (`docker-compose.yml`)
Configured for Lusófona infrastructure:
- **Security**: Database not exposed to host network
- **Persistence**: Named volumes for data
- **Monitoring**: Prometheus + Grafana integration
- **Dependencies**: Proper service startup order

## 🔧 Management & Troubleshooting

### Service Management
```bash
# Check all services
docker compose -p lusochat-litellm ps

# View logs
docker compose -p lusochat-litellm logs -f litellm

# Restart specific service
docker compose -p lusochat-litellm restart litellm

# Stop everything
docker compose -p lusochat-litellm down
```

### Common Issues & Solutions

#### 🔑 License Issues
- **Problem**: LiteLLM license verification fails
- **Solution**: Verify `LITELLM_LICENSE` in `.env` file
- **Check**: `docker compose exec litellm env | grep LITELLM_LICENSE`

#### 📊 Prometheus Metrics
- **Note**: Requires valid LiteLLM Enterprise license
- **Without license**: Service runs with warnings (normal)
- **With license**: Full metrics available in Grafana

#### 🐛 YAML Configuration Errors
- **Problem**: Service crashes with YAML parser errors
- **Solution**: Validate `config.yaml` syntax (indentation, dashes)
- **Tool**: Use `yamllint config.yaml` or online validator

#### 🔌 Connection Issues
- **Problem**: Services can't reach each other
- **Solution**: Check all services are in same Docker network (`litellm-network`)
- **Debug**: `docker network inspect lusochat-litellm_litellm-network`

## 🔄 Updates & Maintenance

### Updating to Latest LiteLLM
```bash
python deploy_litellm.py  # Will ask to remove old clone and get fresh upstream
```

### Modifying Configuration
1. Edit files in `.litellm-lusofona/`
2. Re-run deployment script or manually copy files
3. Restart affected services

### Backing Up Data
```bash
# Export volumes (databases, dashboards)
docker volume ls | grep lusochat-litellm
```

## 🔒 Security Notes

- **Database**: PostgreSQL port NOT exposed to host (security improvement)
- **Passwords**: All passwords via environment variables, not hardcoded
- **Secrets**: Keep `.env` file secure and out of version control
- **Network**: Services communicate via internal Docker network

## 📋 Best Practices for Maintainers

1. **Keep ALL customizations in `.litellm-lusofona/`** for easy tracking
2. **Test changes with deployment script** before production
3. **Update `.env` from `env.example`** when new variables added
4. **Document configuration changes** in `NOTE_MODIFICATIONS.md`
5. **When syncing upstream**, verify our overlay still works

## 💡 Why This Approach Works

- ✅ **No upstream conflicts**: Never merge conflicts on updates
- ✅ **Clean customizations**: All changes tracked in one place  
- ✅ **Easy rollback**: Just re-deploy with different configs
- ✅ **Team friendly**: Clear separation of custom vs. upstream
- ✅ **Always current**: Latest upstream features automatically available

---

This approach has been **successfully tested and deployed**. All services are running and accessible as documented above. 