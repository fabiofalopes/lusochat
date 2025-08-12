# Project Structure & Organization

## Repository Layout

```
lusochat/
├── litellm-lusofona/           # LiteLLM proxy deployment
├── lusochat-openwebui/         # Open WebUI frontend
├── lusochat-deploy/            # Production deployment tools
└── old/                        # Legacy/backup files
```

## LiteLLM Component (`litellm-lusofona/`)

### Core Structure
```
litellm-lusofona/
├── .litellm-lusofona/          # Custom configuration overlay
│   ├── config.yaml             # Main LiteLLM configuration
│   ├── docker-compose.yml      # Service orchestration
│   ├── .env                    # Environment variables
│   ├── models/                 # Model provider configs
│   ├── settings/               # Modular settings
│   └── grafana/                # Monitoring dashboards
├── litellm-upstream/           # Cloned upstream repository
├── contact/                    # Bulk email invitation system
├── docs/                       # Documentation
└── deploy_litellm.py           # Main deployment script
```

### Configuration Pattern
- **Overlay approach**: Custom configs in `.litellm-lusofona/` are copied over upstream
- **Modular configuration**: Split into `models/`, `settings/` directories
- **Environment-based**: All secrets and variables in `.env` files

## Open WebUI Component (`lusochat-openwebui/`)

### Core Structure
```
lusochat-openwebui/
├── .lusochat-ldap/             # LDAP deployment configuration
│   ├── docker-compose.yaml    # Service definition
│   ├── .env                    # Environment variables
│   └── edited-files/           # Custom branding assets
├── .lusochat-oidc/             # OIDC deployment configuration
├── open-webui/                 # Cloned upstream repository (generated)
├── docs/                       # Customization documentation
└── deploy_and_apply_lusochat_customizations.sh
```

### Customization Pattern
- **Non-fork approach**: Clone upstream, apply targeted customizations
- **Branding overlay**: Custom icons, logos, themes in `edited-files/`
- **Targeted replacements**: Specific string/value changes, not entire file rewrites

## Deployment Tools (`lusochat-deploy/`)

### Structure
```
lusochat-deploy/
└── docker-hub-image/           # Pre-built image deployment
    ├── docker-compose.yml      # Production configuration
    ├── deploy.sh               # Management script
    ├── quick-start.sh          # One-command setup
    └── .env                    # Environment template
```

## Key Architectural Patterns

### 1. Upstream Preservation
- **Never fork upstream repositories**
- Clone fresh copies during deployment
- Apply customizations as overlays/patches
- Enables easy updates to latest upstream versions

### 2. Configuration Management
- **Environment-based configuration**: All deployments use `.env` files
- **Modular settings**: Split complex configs into logical modules
- **Template approach**: `.env.example` files for easy setup

### 3. Docker-First Deployment
- **Containerized everything**: All services run in Docker
- **Compose orchestration**: Multi-service deployments
- **Network isolation**: Services communicate via Docker networks
- **Volume persistence**: Data stored in named volumes

### 4. Monitoring Integration
- **Grafana dashboards**: Pre-configured monitoring
- **Prometheus metrics**: Automatic metric collection
- **Log aggregation**: Centralized logging via Docker

## File Naming Conventions

### Configuration Files
- `.env` - Environment variables (never commit with secrets)
- `.env.example` - Environment template (safe to commit)
- `config.yaml` - Main application configuration
- `docker-compose.yml` - Service orchestration

### Scripts
- `deploy_*.py` - Python deployment scripts
- `*.sh` - Shell scripts for automation
- `quick-start.sh` - One-command setup scripts

### Directories
- `.lusochat-*` - Lusochat-specific configurations
- `*-upstream` - Cloned upstream repositories
- `edited-files/` - Custom branding and assets
- `docs/` - Documentation and guides

## Development Workflow

1. **Configuration**: Edit files in custom config directories (`.litellm-lusofona/`, `.lusochat-ldap/`)
2. **Deployment**: Run deployment scripts (`deploy_litellm.py`, `quick-start.sh`)
3. **Updates**: Re-run deployment scripts to get latest upstream + apply customizations
4. **Monitoring**: Use Grafana dashboards and Docker logs for observability