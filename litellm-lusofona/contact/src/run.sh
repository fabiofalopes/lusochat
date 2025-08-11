#!/bin/bash
# Simple runner script for the LiteLLM bulk email sender

cd "$(dirname "$0")"

echo "🚀 LiteLLM Bulk Email Sender"
echo "============================"

# Check if virtual environment exists and is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "../venv" ]; then
        echo "📦 Activating virtual environment..."
        source ../venv/bin/activate
    else
        echo "❌ Virtual environment not found at ../venv"
        echo "Please create one with: python3 -m venv ../venv && source ../venv/bin/activate"
        exit 1
    fi
fi

# Check if dependencies are installed
if ! python3 -c "import google.oauth2.credentials" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Configuration file .env not found"
    echo "Please copy and configure the .env file"
    exit 1
fi

# Show current dry-run setting
DRY_RUN=$(grep "^DRY_RUN=" .env | cut -d'=' -f2)
if [ "$DRY_RUN" = "true" ]; then
    echo "🔍 Running in DRY-RUN mode (no emails will be sent)"
else
    echo "📧 Running in LIVE mode (emails will be sent!)"
fi

echo ""

# Run the script
python3 litellm_bulk_sender.py

echo ""
echo "✅ Done! Check the log file for results."
