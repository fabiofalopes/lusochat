# Lusochat Open WebUI Custom Deployment

Simple system to fetch the latest Open WebUI, apply your customizations, build a custom image, and deploy.

## Project Structure

```
/
├── .gitignore
├── .env.example                 # Example environment variables template
├── .lusochat-ldap/              # YOUR CUSTOMIZATION FILES
│   ├── .env                     # Environment variables (LDAP, etc.)
│   ├── docker-compose.yaml     # Deployment configuration
│   └── edited-files/            # Custom icons and static files
│       └── app/
│           ├── build/           # Frontend customizations (favicons, themes)
│           └── backend/         # Backend customizations (logos, icons)
├── apply_lusochat_customizations.sh  # One script to rule them all
└── README.md
```

**Generated (ignored by Git):**
- `open-webui/` - Cloned repo with your customizations applied

## Setup Your Customizations

### Environment Variables Setup

1. **Copy the example file**:
   ```bash
   cp .env.example .lusochat-ldap/.env
   ```

2. **Edit your `.env` file** with your actual values:
   - Replace `your-openai-api-key-here` with your actual OpenAI API key
   - Replace `your-groq-api-key-here` with your actual Groq API key
   - Replace `your-very-strong-secret-key-here` with a secure secret key
   - Update LDAP settings with your actual server details:
     - `LDAP_SERVER_HOST` - Your LDAP server hostname/IP
     - `LDAP_APP_PASSWORD` - Your LDAP application password
     - `LDAP_APP_DN` and `LDAP_SEARCH_BASE` - Update domain components

### Customization Files

Place your files in `.lusochat-ldap/`:

- **`.env`** - Your environment variables (LDAP settings, API keys, etc.)
- **`docker-compose.yaml`** - Your deployment configuration
- **`edited-files/`** - Custom icons, logos, and static files for branding
  - Contains favicons, splash screens, and logos that replace the default Open WebUI branding
  - Automatically applied during deployment to customize the appearance

**💡 Tip**: Use `.env.example` as a reference for all available configuration options.

## Usage

### One Command Setup & Deploy
```bash
./apply_lusochat_customizations.sh
```

This comprehensive script will:
- Clone the latest Open WebUI
- Apply targeted customizations:
  - Change app name to "Lusochat"
  - Update favicon to Lusófona image
  - Comment out "Open WebUI" name appending
- Copy your `.env` and `docker-compose.yaml` files
- Build custom Docker image
- Optionally deploy the services
- Handle existing installations with user prompts

### Manual Deployment (if you chose not to auto-deploy)
```bash
cd open-webui
docker compose up -d
```

### Management Commands
```bash
# View logs
cd open-webui
docker compose logs -f open-webui

# Stop services
cd open-webui
docker compose down

# Update (re-run the script)
./apply_lusochat_customizations.sh
```

## Features

- **🔄 Future-proof**: Works with Open WebUI updates via targeted replacements
- **🛡️ Safe**: Backs up files and verifies changes
- **🎯 Targeted**: Only changes specific strings/values, not entire files
- **🔧 Interactive**: Prompts for user decisions
- **⚡ Complete**: Handles everything from clone to deployment

## Simple Workflow

1. **Customize** → Edit files in `.lusochat-ldap/`
2. **Run** → `./apply_lusochat_customizations.sh`
3. **Done!** → Your customized Lusochat is running at http://localhost:3000

Everything happens in the `open-webui/` directory - no scattered files, no complex setup. 