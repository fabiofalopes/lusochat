# 🚀 Lusochat Docker Hub Deployment

Deploy Lusochat instantly using the pre-built Docker image from Docker Hub - **no building required!**

## 📋 What's This?

This folder provides a **deployment-only** solution for Lusochat using the pre-customized Docker image:
- **Docker Hub Image**: `fabiolx/lusochat-openwebui:latest`
- **Zero Build Time**: Pull and run directly
- **All Customizations Included**: Branding, icons, Lusófona University theme
- **Production Ready**: Optimized for quick deployment

## 🎯 Quick Start

### 1. Setup Environment
```bash
# Copy environment template and configure
cp env.example .env
nano .env  # Edit with your actual values
```

### 2. Deploy
```bash
# Make script executable and deploy
chmod +x deploy.sh
./deploy.sh
```

That's it! 🎉 Lusochat is now running at **http://localhost:3000**

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Docker Compose configuration using Docker Hub image |
| `env.example` | Environment variables template |
| `deploy.sh` | Complete deployment and management script |
| `README.md` | This documentation |

## ⚙️ Configuration

### Required Environment Variables

Edit `.env` file with your actual values:

```bash
# Essential Configuration
WEBUI_SECRET_KEY=your-secure-secret-key
OPENAI_API_KEY=your-openai-api-key-here
GROQ_API_KEY=your-groq-api-key-here

# Optional: LDAP Authentication
ENABLE_LDAP=true
LDAP_SERVER_HOST=ldap.your-domain.com
LDAP_APP_DN=CN=lusochat-app,OU=Applications,DC=domain,DC=com
LDAP_APP_PASSWORD=your-ldap-password
```

### Generate Secure Secret Key
```bash
# Generate strong secret key
openssl rand -base64 32
```

## 🛠️ Management Commands

The `deploy.sh` script provides comprehensive management:

### Basic Operations
```bash
./deploy.sh deploy    # Deploy Lusochat
./deploy.sh update    # Update to latest version
./deploy.sh stop      # Stop services
./deploy.sh restart   # Restart services
./deploy.sh status    # Show detailed status
```

### Monitoring & Troubleshooting
```bash
./deploy.sh logs      # View real-time logs
./deploy.sh shell     # Open container shell
./deploy.sh status    # Check health & resources
```

### Data Management
```bash
./deploy.sh backup    # Create data backup
./deploy.sh restore backup.tar.gz  # Restore from backup
./deploy.sh clean     # Complete cleanup
```

### Help
```bash
./deploy.sh help      # Show all commands
```

## 🔧 Advanced Features

### Automatic Setup
- ✅ **Environment Detection**: Checks for required tools
- ✅ **Secret Key Generation**: Auto-generates secure keys
- ✅ **Health Monitoring**: Validates service status
- ✅ **Smart Updates**: Handles version updates gracefully

### Production Features
- ✅ **Volume Persistence**: Data survives container restarts
- ✅ **Health Checks**: Built-in container health monitoring
- ✅ **Backup System**: Complete data backup/restore
- ✅ **Resource Monitoring**: CPU, memory, and network stats

### LDAP Integration
- ✅ **Enterprise Authentication**: Full LDAP support
- ✅ **Lusófona University Ready**: Pre-configured for institutional use
- ✅ **Secure Binding**: Proper LDAP application authentication

## 📊 Service Status

Check your deployment status:

```bash
# Quick status check
./deploy.sh status

# Monitor resources
docker stats lusochat-openwebui

# View detailed logs
./deploy.sh logs
```

## 🔄 Updates

Keep Lusochat up-to-date with the latest features:

```bash
# Update to latest Docker Hub image
./deploy.sh update
```

This will:
1. Pull the latest `fabiolx/lusochat-openwebui:latest` image
2. Stop current services
3. Start with new image
4. Preserve all your data and configuration

## 🌐 Access Information

After deployment, access Lusochat at:

- **Local**: http://localhost:3000
- **Network**: http://YOUR_SERVER_IP:3000
- **Custom Port**: Edit `OPEN_WEBUI_PORT` in `.env`

### First Login
1. Open the web interface
2. Create your admin account
3. Configure models and settings
4. Start chatting!

## 🔍 Troubleshooting

### Common Issues

**Services won't start:**
```bash
./deploy.sh logs  # Check error messages
```

**Permission issues:**
```bash
chmod +x deploy.sh  # Make script executable
```

**Port conflicts:**
```bash
# Edit .env file and change OPEN_WEBUI_PORT
nano .env
./deploy.sh restart
```

**Docker issues:**
```bash
docker info        # Check Docker daemon
docker version     # Verify Docker installation
```

### Reset Everything
```bash
./deploy.sh clean   # Remove everything
./deploy.sh deploy  # Fresh deployment
```

## 🎨 What's Included in the Docker Image

The `fabiolx/lusochat-openwebui:latest` image includes:

- ✅ **Lusochat Branding**: Custom logos and styling
- ✅ **Lusófona University Theme**: Institutional colors and design
- ✅ **Custom Favicons**: Branded browser icons
- ✅ **Portuguese Localization**: Ready for Lusófona users
- ✅ **PWA Configuration**: Progressive Web App support
- ✅ **LDAP Integration**: Enterprise authentication ready
- ✅ **Security Hardening**: Production security settings

## 📞 Support & Documentation

### For Deployment Issues
- Check this README
- Run `./deploy.sh help`
- Review logs with `./deploy.sh logs`

### For Open WebUI Issues
- Visit [Open WebUI Documentation](https://docs.openwebui.com/)
- Check [Open WebUI GitHub](https://github.com/open-webui/open-webui)

### For Lusochat Customizations
- This deployment uses the pre-built custom image
- All customizations are already included
- No additional configuration needed

## 🚀 Benefits of This Deployment

✅ **No Build Time**: Skip the 10-15 minute build process  
✅ **Consistent Environment**: Same image across all deployments  
✅ **Easy Updates**: Simple one-command updates  
✅ **Production Ready**: Optimized and tested configuration  
✅ **Complete Management**: Full lifecycle management scripts  
✅ **Enterprise Features**: LDAP, backup, monitoring included  
✅ **Zero Dependencies**: Just Docker required  

---

**Ready to deploy?** Just run `./deploy.sh` and you're live! 🎉