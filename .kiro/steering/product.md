# Product Overview

## Lusochat - AI Chat Platform for Lusófona University

Lusochat is a comprehensive AI chat platform deployment for Lusófona University, consisting of three main components:

### Core Components

1. **LiteLLM Proxy** (`litellm-lusofona/`)
   - Multi-provider LLM API gateway and proxy
   - Handles routing to various AI providers (OpenAI, Groq, SambaNova, etc.)
   - Enterprise features: rate limiting, cost tracking, user management
   - Monitoring with Grafana and Prometheus

2. **Open WebUI Frontend** (`lusochat-openwebui/`)
   - Customized ChatGPT-like web interface
   - Lusófona University branding and theming
   - LDAP/OIDC authentication integration
   - Progressive Web App (PWA) support

3. **Deployment Tools** (`lusochat-deploy/`)
   - Docker Hub image deployment (recommended)
   - Pre-built images with all customizations
   - Production-ready configurations

### Key Features

- **Multi-provider AI access**: OpenAI, Groq, SambaNova, and on-premise models
- **Enterprise authentication**: LDAP integration for university users
- **Custom branding**: Lusófona University visual identity
- **Monitoring & analytics**: Usage tracking and performance monitoring
- **Bulk user management**: Email invitation system for user onboarding
- **Portuguese localization**: Ready for Portuguese-speaking users

### Target Users

- Lusófona University students, faculty, and staff
- IT administrators managing the platform
- Developers maintaining and extending the system