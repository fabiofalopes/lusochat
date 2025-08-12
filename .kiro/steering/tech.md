# Technology Stack & Build System

## Core Technologies

### Backend
- **Python 3.8+**: Primary backend language
- **LiteLLM**: Multi-provider LLM proxy framework
- **FastAPI**: Web framework (via LiteLLM)
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage

### Frontend
- **SvelteKit**: Frontend framework (Open WebUI)
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Build tool and dev server
- **Node.js 18+**: JavaScript runtime

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Grafana**: Monitoring dashboards
- **Prometheus**: Metrics collection
- **Nginx**: Reverse proxy (in production)

### Authentication
- **LDAP**: Enterprise directory integration
- **OIDC**: OpenID Connect support
- **JWT**: Token-based authentication

## Build & Development Commands

### LiteLLM Deployment
```bash
# Deploy entire stack
python deploy_litellm.py

# Update configuration only
python deploy_litellm.py --update-config

# Check service status
docker compose -p lusochat-litellm ps

# View logs
docker compose -p lusochat-litellm logs -f

# Stop services
docker compose -p lusochat-litellm down
```

### Open WebUI Development
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Type checking
npm run check

# Linting
npm run lint

# Format code
npm run format
```

### Docker Operations
```bash
# Build custom image
docker build -t lusochat-openwebui .

# Run with compose
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Contact System (Bulk Email)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run bulk email sender
python litellm_bulk_sender.py
```

## Package Managers
- **Poetry**: Python dependency management (LiteLLM)
- **npm**: Node.js package management (Open WebUI)
- **pip**: Python package installation (contact system)

## Development Tools
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Black**: Python code formatting
- **Pylint**: Python linting
- **Svelte Check**: Svelte type checking

## Environment Configuration
All components use `.env` files for configuration:
- Database connections
- API keys (OpenAI, Groq, etc.)
- LDAP credentials
- Service URLs and ports
- Feature flags