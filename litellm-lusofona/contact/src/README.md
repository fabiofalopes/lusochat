# Simplified LiteLLM Bulk Email Sender

This is a streamlined version of the bulk email sender, focused specifically on the LiteLLM use case.

## Files

- `litellm_bulk_sender.py` - Main script to run
- `gmail_client.py` - Simple Gmail API wrapper
- `csv_utils.py` - CSV loading and data merging utilities
- `email_logger.py` - Simple result logging
- `.env` - Configuration file
- `requirements.txt` - Python dependencies

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your settings in `.env`

3. Run the script:
   ```bash
   python litellm_bulk_sender.py
   ```

## Configuration

All configuration is done through environment variables in the `.env` file:

- `CSV_PATH` - Path to main CSV file with user data
- `RESULTS_CSV_PATH` - Path to results CSV with credentials (optional)
- `SUBJECT` - Email subject template with {variable} placeholders
- `BODY_FILE` - Path to email body template file
- `SENDER` - Your email address
- `DRY_RUN` - Set to `true` to preview emails without sending
- `CLIENT_SECRETS_PATH` - Path to Google OAuth client secrets
- `TOKEN_PATH` - Path to store OAuth token

## What it does

1. Loads user data from CSV file
2. Optionally merges with results CSV (for credentials/links)
3. Sends personalized emails using Gmail API
4. Logs all results to CSV file
5. Handles rate limiting and duplicate detection

This is much simpler than the original script - no command line arguments, no complex options, just environment variables and straightforward email sending.
