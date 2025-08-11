# Bulk Email Sender for Google Workspace Gmail

A Python tool for sending personalized bulk emails via Gmail API, designed for distributing user credentials and access information for the modelos.ai.ulusofona.pt platform.

## Features

- 📧 **Bulk email sending** with Gmail API
- 🎯 **CSV-based templating** with merge fields
- 🔐 **Credentials distribution** by merging original CSV with results CSV
- 🛡️ **Dry-run mode** for safe testing
- 🚫 **Duplicate prevention** by email address
- ⏱️ **Rate limiting** between sends
- 📊 **CSV logging** of all send results
- ⚙️ **Environment-based configuration** (no command-line flags needed)
- 🌍 **Multi-language templates** (Portuguese PT and English)

## Prerequisites

- Python 3.8+
- Google Workspace account with Gmail
- Google Cloud Project with Gmail API enabled

## Complete Setup Guide

### 1. Google Cloud Project Setup

#### Step 1.1: Create or Select a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your **Project ID** for later

#### Step 1.2: Enable Gmail API
1. In Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Gmail API"
3. Click on Gmail API and click **Enable**
4. Wait for the API to be enabled (may take a few minutes)

#### Step 1.3: Configure OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**
2. Choose **Internal** (for Google Workspace) or **External** (for personal Gmail)
3. Fill in the required fields:
   - **App name**: `Bulk Email Sender` (or your preferred name)
   - **User support email**: Your email
   - **Developer contact email**: Your email
4. Click **Save and Continue**
5. On **Scopes** page, click **Save and Continue** (we'll add scopes programmatically)
6. Review and click **Back to Dashboard**

#### Step 1.4: Create OAuth Credentials
1. Go to **APIs & Services > Credentials**
2. Click **+ Create Credentials > OAuth 2.0 Client IDs**
3. Choose **Desktop application**
4. Name it: `Gmail Bulk Sender`
5. Click **Create**
6. **Download the JSON file** - it will have a name like `client_secret_XXXXX.json`
7. Save this file in the `contact/credentials/` folder

### 2. Alternative Authentication Methods

#### Option A: OAuth (Recommended - What we set up above)
- ✅ Easy setup with browser consent flow
- ✅ Works with personal and workspace accounts
- ✅ Automatic token refresh
- ❌ Requires manual consent on first run

#### Option B: Service Account with Domain-Wide Delegation
- ✅ Fully automated (no browser interaction)
- ✅ Can impersonate any user in the domain
- ✅ Perfect for production automation
- ❌ Requires Google Workspace admin privileges
- ❌ More complex setup

<details>
<summary>Click to expand Service Account setup instructions</summary>

##### Service Account Setup:
1. **Create Service Account:**
   - Go to **APIs & Services > Credentials**
   - Click **+ Create Credentials > Service Account**
   - Name: `gmail-bulk-sender`
   - Click **Create and Continue**
   - Skip role assignment, click **Done**

2. **Create Key:**
   - Click on the created service account
   - Go to **Keys** tab
   - Click **Add Key > Create New Key**
   - Choose **JSON** and download

3. **Enable Domain-Wide Delegation:**
   - In the service account details, check **Enable Google Workspace Domain-wide Delegation**
   - Note the **Client ID** (long number)

4. **Configure in Google Admin Console:**
   - Go to [admin.google.com](https://admin.google.com)
   - Navigate to **Security > Access and data control > API controls**
   - Click **Domain-wide delegation**
   - Click **Add new** and enter:
     - **Client ID**: The service account client ID
     - **OAuth Scopes**: 
       ```
       https://www.googleapis.com/auth/gmail.send,
       https://www.googleapis.com/auth/gmail.readonly,
       https://www.googleapis.com/auth/gmail.settings.basic
       ```
   - Click **Authorize**

5. **Set Environment Variables:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   export GMAIL_IMPERSONATE=your-email@yourdomain.com
   ```
</details>

#### Option C: Application Default Credentials (gcloud)
```bash
gcloud auth application-default login
```
Choose your Google Workspace account when prompted.

##### Credentials Example

```json

{
    "installed": {
        "client_id": "<client_id>.apps.googleusercontent.com",
        "project_id": "<project_id>",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "client_secret",
        "redirect_uris": [
            "http://localhost"
        ]
    }
}

```


### 3. Installation

#### Step 3.1: Clone and Setup
```bash
# Navigate to your project directory
cd /path/to/your/project/contact/

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3.2: Configure Environment
```bash
# Copy the example configuration
cp .env.example .env

# Create credentials folder and move your client secret there
mkdir -p credentials
mv client_secret_*.json credentials/

# Edit the configuration file
nano .env  # or use your preferred editor
```

### 4. Required Folders (Not in Git)

⚠️ **Important**: The following folders are excluded from git (via .gitignore) but are essential for the system to work:

#### 4.1 credentials/ folder
- **Purpose**: Stores all authentication files
- **Contents**: 
  - `client_secret_*.json` - Your OAuth credentials from Google Cloud
  - `token.json` - Auto-generated OAuth token cache (created on first auth)
- **Setup**: `mkdir -p credentials` and move your client_secret file there
- **Security**: Never commit these files - they contain sensitive authentication data

#### 4.2 logs/ folder  
- **Purpose**: Stores all email send logs and results
- **Contents**:
  - `bulk_email_log.csv` - Detailed log of all email sends (success/failure/errors)
  - Additional log files if you customize LOG_PATH
- **Setup**: Created automatically by the script when first run
- **Monitoring**: Check `logs/bulk_email_log.csv` to track email delivery status

#### 4.3 .env file
- **Purpose**: Your personal configuration with paths, credentials, and settings
- **Setup**: Copy from `.env.example` and customize
- **Security**: Contains paths to sensitive files - excluded from git

```bash
# Quick setup commands:
mkdir -p credentials logs
cp .env.example .env
mv client_secret_*.json credentials/
# Edit .env with your settings
```

### 5. Configuration (.env file)

The `.env` file contains all configuration. Here's what each setting does:

```bash
# Authentication (choose one approach)
AUTH_MODE=oauth                    # oauth, adc, or auto
CLIENT_SECRETS_PATH=./credentials/client_secret_XXXXX.json  # Path to your OAuth credentials
TOKEN_PATH=./credentials/token.json           # Where to store the OAuth token
# GMAIL_IMPERSONATE=shared@domain.com  # For service accounts only

# Email Content and Data Sources
CSV_PATH=../docs/bulk_test.csv    # Main CSV with user data
RESULTS_CSV_PATH=../docs/bulk_users__bulk_test_results.csv  # CSV with credentials
TO_FIELD=user_email               # Column name for recipient emails

# Email Template
SUBJECT=Acesso à plataforma modelos.ai.ulusofona.pt - Equipa {teams}
BODY_FILE=./templates/welcome_with_credentials.txt
# BODY=Inline message here     # Alternative to BODY_FILE

# Email Headers
SENDER=your.email@domain.com      # From address
# CC=admin@domain.com            # Optional CC
# BCC=logs@domain.com            # Optional BCC
# REPLY_TO=support@domain.com    # Optional Reply-To

# Sending Options
DRY_RUN=true                      # Set to false when ready to send
DEDUPE=true                       # Remove duplicate recipients
SLEEP_BETWEEN_SENDS=0.5          # Seconds between emails (rate limiting)
LIMIT=                           # Max emails to send (empty = no limit)
LOG_PATH=logs/bulk_email_log.csv      # Results log file
```

### 6. CSV File Format

#### 6.1 Main CSV (user data)
```csv
user_email,user_role,teams,max_budget,budget_duration,models
user1@domain.com,internal_user,"team-alpha",,,
user2@domain.com,internal_user,"team-beta",,,
```

#### 6.2 Results CSV (credentials from LiteLLM)
```csv
user_email,user_role,status,key,invitation_link,error
user1@domain.com,internal_user,success,abc123,https://modelos.ai.ulusofona.pt/ui?invitation_id=xyz,
user2@domain.com,internal_user,success,def456,https://modelos.ai.ulusofona.pt/ui?invitation_id=uvw,
```

The script automatically merges these CSVs by `user_email`, so each recipient gets their personalized credentials.

### 7. Email Templates

#### 7.1 Available Templates
- `templates/welcome_with_credentials.txt` - Portuguese (default)
- `templates/welcome_with_credentials_en.txt` - English
- `templates/body_example.txt` - Simple Portuguese template

#### 7.2 Template Variables
Templates use Python string formatting. Available variables include:
- `{user_email}` - Recipient email
- `{teams}` - Team assignment
- `{user_role}` - User role
- `{key}` - Access key (from results CSV)
- `{invitation_link}` - Login link (from results CSV)
- `{status}` - Account creation status
- Any other column from your CSV files

#### 7.3 Example Template
```text
Olá {user_email},

A sua conta na plataforma modelos.ai.ulusofona.pt foi criada com sucesso.

**Credenciais de Acesso:**
- Chave de acesso: {key}
- Link direto: {invitation_link}
- Equipa: {teams}

**Como aceder:**
1. Clique no link acima
2. Use a chave de acesso quando solicitado
3. Comece a explorar os modelos de IA disponíveis

Para questões técnicas, responda a este email.

Cumprimentos,
Equipa modelos.ai.ulusofona.pt
```

### 8. Usage

#### 8.1 First Time Setup (OAuth Authentication)
```bash
# Activate virtual environment
source venv/bin/activate

# Check authentication (will trigger OAuth flow)
python3 bulk_email_sender.py --whoami --csv ../docs/any.csv --subject test --body test --limit 0 --dry-run
```
This will:
1. Open your browser for Google OAuth consent
2. Save `token.json` for future use
3. Display your authenticated email and any send-as aliases

#### 8.2 Test with Dry Run
```bash
# Preview emails without sending
python3 bulk_email_sender.py
```
This reads all settings from `.env` and shows you exactly what will be sent.

#### 8.3 Send Real Emails
Edit `.env` and set:
```bash
DRY_RUN=false
```
Then run:
```bash
python3 bulk_email_sender.py
```

#### 8.4 Check Results
View the log file:
```bash
cat logs/bulk_email_log.csv
```

### 9. Workflow Examples

#### 8.1 Complete User Onboarding Workflow
1. **Prepare user list**: Create CSV with user emails and team assignments
2. **Import to LiteLLM**: Use your existing bulk import script
3. **Get credentials**: Export results CSV with keys and invitation links
4. **Configure email**: Update `.env` with correct CSV paths and template
5. **Test**: Run with `DRY_RUN=true` to preview
6. **Send**: Set `DRY_RUN=false` and run the script
7. **Monitor**: Check `logs/bulk_email_log.csv` for delivery status

#### 9.2 Different Email Languages
For English emails:
```bash
# In .env file:
SUBJECT=Access to modelos.ai.ulusofona.pt platform - Team {teams}
BODY_FILE=./templates/welcome_with_credentials_en.txt
```

#### 9.3 Rate Limiting for Large Lists
For 100+ recipients:
```bash
# In .env file:
SLEEP_BETWEEN_SENDS=1.0  # 1 second between emails
LIMIT=50                 # Send only 50 at a time
```

### 10. Troubleshooting

#### 10.1 Common Issues

**"Default credentials not found"**
- Ensure you've completed Google Cloud setup
- Check that `CLIENT_SECRETS_PATH` points to your downloaded JSON file
- Try running `--whoami` command first

**"OAuth selected but client_secret.json was not found"**
- Verify the path in `CLIENT_SECRETS_PATH`
- Ensure the file was downloaded from Google Cloud Console

**"HttpError 403: Insufficient Permission"**
- Verify Gmail API is enabled in your Google Cloud project
- Check OAuth consent screen is configured
- Ensure your account has necessary permissions

**"The user does not have permission to send as..."**
- The `SENDER` email must be either your authenticated account or a verified "Send mail as" alias
- Add send-as aliases in Gmail Settings > Accounts and Import

#### 10.2 Gmail API Quotas
- **Daily send limit**: 1 billion (for most accounts)
- **Rate limit**: 250 quota units per user per 100 seconds
- Our script includes rate limiting with `SLEEP_BETWEEN_SENDS`

#### 10.3 Debugging
```bash
# Test authentication only
python3 bulk_email_sender.py --whoami --csv ../docs/any.csv --subject test --body test --limit 0 --dry-run

# Test with minimal data
python3 bulk_email_sender.py --limit 1 --dry-run

# Check CSV merging
python3 -c "
from bulk_email_sender import iter_rows
from pathlib import Path
for row in iter_rows(Path('../docs/bulk_test.csv'), Path('../docs/bulk_users__bulk_test_results.csv')):
    print(row)
    break
"
```

### 11. Security Notes

- **Never commit credentials**: `.env` and `token.json` are in `.gitignore`
- **Rotate tokens**: OAuth tokens expire and refresh automatically
- **Limit permissions**: Only enable necessary Gmail API scopes
- **Audit logs**: Check `bulk_email_log.csv` for all send activity
- **Test thoroughly**: Always use `DRY_RUN=true` before real sends

### 12. Advanced Configuration

#### 12.1 Custom Send-As Addresses
To send from a shared mailbox or group email:

1. **Add Send-As Alias** in Gmail:
   - Go to Gmail Settings > Accounts and Import
   - Click "Add another email address"
   - Add the shared email and verify it

2. **Set in .env**:
   ```bash
   SENDER=shared-mailbox@yourdomain.com
   ```

#### 12.2 Service Account with Impersonation
```bash
# In .env file:
AUTH_MODE=adc
GMAIL_IMPERSONATE=shared-account@yourdomain.com
```

#### 12.3 Command Line Overrides
You can still override any .env setting:
```bash
python3 bulk_email_sender.py --sender different@email.com --dry-run
```

### 13. File Structure
```
contact/
├── .env                          # Your configuration (not in git)
├── .env.example                  # Configuration template
├── .gitignore                    # Excludes credentials and logs from git
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── bulk_email_sender.py          # Main script
├── credentials/                  # All authentication files (not in git)
│   ├── client_secret_*.json     # OAuth credentials
│   └── token.json               # OAuth token cache
├── logs/                         # All log files (not in git)
│   └── bulk_email_log.csv       # Send results log
└── templates/
    ├── welcome_with_credentials.txt     # Portuguese template
    ├── welcome_with_credentials_en.txt  # English template
    └── body_example.txt                 # Simple template
```

---

## Quick Reference

**Setup**: `mkdir credentials` → Move client_secret to credentials/ → `cp .env.example .env` → Edit .env → `python3 bulk_email_sender.py`

**Test**: Set `DRY_RUN=true` in .env

**Send**: Set `DRY_RUN=false` in .env

**Check results**: `cat logs/bulk_email_log.csv`

For support, check the troubleshooting section or review the Google Cloud Console setup steps.
