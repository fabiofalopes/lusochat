# LiteLLM Bulk Email Sender

A simple tool for sending personalized bulk emails to LiteLLM users via Gmail API.

## Quick Start

1. **Setup Google OAuth credentials** (see Google Setup section below)
2. **Configure settings** in `src/.env`
3. **Run the script:**
   ```bash
   cd src/
   ./run.sh
   ```

## Files Structure

```
contact/
├── src/                    # ← Main application code
│   ├── litellm_bulk_sender.py  # Main script
│   ├── gmail_client.py         # Gmail API wrapper  
│   ├── csv_utils.py           # CSV handling
│   ├── email_logger.py        # Result logging
│   ├── .env                   # Configuration
│   └── run.sh                 # Convenience runner
├── credentials/            # OAuth credentials
├── templates/             # Email templates
├── files/                # CSV data files
└── logs/                 # Email sending logs
```

## Configuration

Edit `src/.env` to configure:

```bash
# Required
CSV_PATH=../files/your_users.csv
RESULTS_CSV_PATH=../files/your_results.csv  
SUBJECT=Your access to modelos.ai.ulusofona.pt
BODY_FILE=../templates/welcome.txt
SENDER=your-email@domain.com

# Optional
DRY_RUN=true                    # Set to false to actually send
SLEEP_BETWEEN_SENDS=0.5         # Rate limiting
LOG_PATH=../logs/email_log.csv
```

## Email Templates

Templates support variable substitution using `{variable_name}` syntax:
- `{user_email}` - Recipient email
- `{teams}` - Team name  
- `{key}` - Access key
- `{invitation_link}` - Invitation URL

## Google OAuth Setup

**This is required before first use.**

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing one
3. Enable Gmail API: APIs & Services → Library → Gmail API → Enable

### 2. Create OAuth Credentials  
1. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client IDs
2. Application type: Desktop application
3. Download the JSON file
4. Save as `credentials/client_secret_*.json`

### 3. OAuth Consent Screen
1. APIs & Services → OAuth consent screen
2. User Type: Internal (for organization) or External
3. Add your email to test users if External
4. Scopes: Add `https://www.googleapis.com/auth/gmail.send`

### 4. First Run
The first time you run the script, it will:
1. Open a browser for Google authentication
2. Save the token for future use
3. You only need to do this once

## Troubleshooting

**"Client secrets file not found"**
- Ensure your `client_secret_*.json` is in the `credentials/` folder

**"Authentication failed"**  
- Delete `credentials/token.json` and re-authenticate
- Check OAuth consent screen configuration

**"Permission denied"**
- Verify Gmail API is enabled
- Check OAuth scopes include Gmail send permission

## Usage Examples

**Test with dry-run:**
```bash
cd src/
# Set DRY_RUN=true in .env
./run.sh
```

**Send actual emails:**
```bash
cd src/ 
# Set DRY_RUN=false in .env
./run.sh
```

**Check results:**
```bash
tail -f logs/bulk_email_log.csv
```
