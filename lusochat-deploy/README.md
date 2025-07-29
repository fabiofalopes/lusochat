# 🚀 Lusochat Deployment Options

This folder contains different deployment approaches for Lusochat, a customized Open WebUI instance for Lusófona University.

## 📁 Available Deployments

### 🐳 Docker Hub Image Deployment (Recommended)
**Location**: `docker-hub-image/`

**Best for**: Production deployments, quick setup, consistent environments

✅ **Advantages**:
- ⚡ **Zero build time** - Pull and run directly
- 🔄 **Easy updates** - One command to update
- 📦 **All customizations included** - Branding, icons, themes pre-built
- 🏭 **Production ready** - Optimized and tested configuration
- 🛠️ **Complete management** - Full lifecycle management scripts

**Quick Start**:
```bash
cd docker-hub-image/
./quick-start.sh
```

Uses the pre-built image: `fabiolx/lusochat-openwebui:latest`

---

## 🎯 Which Deployment Should I Use?

### Use Docker Hub Image If:
- ✅ You want the **fastest deployment** (no build time)
- ✅ You prefer **consistent, tested environments**
- ✅ You need **easy updates and management**
- ✅ You're deploying to **production or multiple servers**
- ✅ You don't need to modify the Lusochat customizations

### Use Local Build If:
- ✅ You want to **customize the branding further**
- ✅ You need to **modify the Open WebUI code**
- ✅ You want to **control the entire build process**
- ✅ You have specific **custom requirements**

## 🏗️ What's Included in All Deployments

All Lusochat deployments include:

- 🎨 **Custom Branding**: Lusochat logos and styling
- 🏛️ **Lusófona University Theme**: Institutional colors and design
- 🌍 **Portuguese Localization**: Ready for Portuguese users
- 🔐 **LDAP Integration**: Enterprise authentication support
- 📱 **PWA Support**: Progressive Web App functionality
- 🛡️ **Security Hardening**: Production security configurations

## 🚀 Quick Deployment Guide

### Option 1: Docker Hub (Fastest - Recommended)
```bash
# Navigate to Docker Hub deployment
cd docker-hub-image/

# Run quick setup
./quick-start.sh

# Or manual setup:
cp env.example .env
nano .env  # Configure your settings
./deploy.sh
```

**Time to deploy**: ~2-3 minutes

### Option 2: Local Build (Most Flexible)
```bash
# Navigate to build deployment (if available)
cd local-build/

# Build and deploy
./build-and-deploy.sh
```

**Time to deploy**: ~15-20 minutes (includes build)

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] **Docker installed** and running
- [ ] **Docker Compose** available (v2.0+)
- [ ] **Required API keys** (OpenAI, Groq, etc.)
- [ ] **LDAP credentials** (if using LDAP authentication)
- [ ] **Network ports available** (default: 3000)

## ⚙️ Environment Configuration

All deployments use similar environment configuration:

```bash
# Basic Configuration
OPEN_WEBUI_PORT=3000
WEBUI_NAME=Lusochat
WEBUI_SECRET_KEY=your-secure-secret-key

# API Keys
OPENAI_API_KEY=your-openai-api-key
GROQ_API_KEY=your-groq-api-key

# LDAP (Optional)
ENABLE_LDAP=true
LDAP_SERVER_HOST=ldap.lusofona.pt
LDAP_APP_DN=CN=lusochat-app,OU=Applications,DC=domain,DC=com
```

## 🛠️ Management Commands

All deployments provide similar management capabilities:

```bash
# Status and monitoring
./deploy.sh status    # Check service status
./deploy.sh logs      # View logs

# Control
./deploy.sh start     # Start services
./deploy.sh stop      # Stop services
./deploy.sh restart   # Restart services

# Updates and maintenance
./deploy.sh update    # Update to latest version
./deploy.sh backup    # Create data backup
./deploy.sh clean     # Complete cleanup
```

## 🌐 Access After Deployment

After successful deployment:

- **Local Access**: http://localhost:3000
- **Network Access**: http://YOUR_SERVER_IP:3000
- **Custom Port**: Edit `OPEN_WEBUI_PORT` in `.env`

### First Login Steps:
1. Open the web interface
2. Create your admin account
3. Configure available models
4. Set up authentication (if using LDAP)
5. Start using Lusochat!

## 🔍 Troubleshooting

### Common Issues:

**Docker not running**:
```bash
sudo systemctl start docker
```

**Port conflicts**:
```bash
# Change port in .env file
OPEN_WEBUI_PORT=3001
./deploy.sh restart
```

**Permission issues**:
```bash
chmod +x deploy.sh
```

**View detailed logs**:
```bash
./deploy.sh logs
```

## 📞 Support

### For Deployment Issues:
- Check the specific deployment folder's README
- Review logs: `./deploy.sh logs`
- Verify environment configuration

### For Open WebUI Issues:
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)

### For Lusochat Customizations:
- Docker Hub image contains all customizations
- Source customizations available in the build folder
- Contact Lusófona IT support for institutional issues

---

## 🎉 Ready to Deploy?

**Recommended for most users**:
```bash
cd docker-hub-image/
./quick-start.sh
```

**For advanced users or custom requirements**:
```bash
cd local-build/
./build-and-deploy.sh
```

Choose your deployment method and get Lusochat running in minutes! 🚀