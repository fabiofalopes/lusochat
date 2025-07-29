#!/bin/bash

# ===============================================
# LUSOCHAT DOCKER HUB - ONE-LINER QUICK START
# ===============================================

echo "🚀 Lusochat Quick Start - Docker Hub Deployment"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ] || [ ! -f "deploy.sh" ]; then
    echo "❌ Error: This script must be run from the docker-hub-image directory"
    echo "   Please navigate to the correct directory first:"
    echo "   cd lusochat-deploy/docker-hub-image/"
    exit 1
fi

echo "📋 Setting up Lusochat deployment..."

# Make deploy script executable
chmod +x deploy.sh
echo "✅ Made deploy script executable"

# Copy environment template if .env doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from template"
    else
        echo "❌ Error: env.example file not found"
        exit 1
    fi
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "🎯 Setup Complete! Next steps:"
echo ""
echo "1. Edit your configuration:"
echo "   nano .env  # (or use your preferred editor)"
echo ""
echo "2. Configure these REQUIRED settings in .env:"
echo "   • WEBUI_SECRET_KEY - Generate with: openssl rand -base64 32"
echo "   • OPENAI_API_KEY - Your OpenAI API key"
echo "   • GROQ_API_KEY - Your Groq API key (optional)"
echo ""
echo "3. Deploy Lusochat:"
echo "   ./deploy.sh"
echo ""
echo "📖 For detailed help, see README.md or run: ./deploy.sh help"
echo ""

# Offer to open .env for editing
if command -v nano >/dev/null 2>&1; then
    echo -n "Would you like to edit .env now? [y/N]: "
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            echo "Opening .env for editing..."
            nano .env
            echo ""
            echo "✅ Configuration saved!"
            echo ""
            echo -n "Ready to deploy Lusochat now? [y/N]: "
            read -r deploy_response
            case "$deploy_response" in
                [yY][eE][sS]|[yY]) 
                    echo "🚀 Starting deployment..."
                    ./deploy.sh
                    ;;
                *)
                    echo "ℹ️  Run './deploy.sh' when ready to deploy"
                    ;;
            esac
            ;;
        *)
            echo "ℹ️  Don't forget to edit .env before deploying!"
            echo "   Then run: ./deploy.sh"
            ;;
    esac
else
    echo "ℹ️  Edit .env with your preferred editor, then run: ./deploy.sh"
fi