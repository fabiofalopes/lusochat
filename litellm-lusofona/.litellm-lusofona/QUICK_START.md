# Lusochat LiteLLM - Quick Start Guide

## 🚀 One-Command Deployment

```bash
# From litellm-lusofona/ directory
python deploy_litellm.py
```

## 📋 Prerequisites Checklist

- [ ] Python 3.7+
- [ ] Docker & Docker Compose installed
- [ ] Git installed
- [ ] `.env` file created from `env.example`

## ⚡ Setup Steps

1. **Create Environment File**
   ```bash
   cd litellm-lusofona/.litellm-lusofona/
   cp env.example .env
   # Edit .env with your actual values
   ```

2. **Deploy Services**
   ```bash
   cd ../  # Back to litellm-lusofona/
   python deploy_litellm.py
   ```

3. **Verify Deployment**
   ```bash
   docker compose -p lusochat-litellm ps
   ```

## 🌐 Access Points

After successful deployment:

- **🤖 LiteLLM API**: http://localhost:4000
- **📊 Grafana**: http://localhost:3001 (admin/admin)
- **📈 Prometheus**: http://localhost:9090

## 🛠️ Quick Commands

```bash
# Check status
docker compose -p lusochat-litellm ps

# View logs
docker compose -p lusochat-litellm logs -f

# Stop services
docker compose -p lusochat-litellm down

# Update to latest LiteLLM
python deploy_litellm.py  # Choose "y" to remove old clone
```

## 🔧 Test API

```bash
curl -X POST "http://localhost:4000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -d '{
    "model": "DeepSeek-Llama-8B",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Services not starting | Check `docker compose logs -f` |
| License errors | Verify `LITELLM_LICENSE` in `.env` |
| API connection failed | Ensure model servers (192.168.108.x) are running |
| Config errors | Validate `config.yaml` syntax |

---

For detailed documentation, see `README.md` and `NOTE_MODIFICATIONS.md`. 