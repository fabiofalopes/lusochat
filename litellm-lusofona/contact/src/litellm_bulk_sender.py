#!/usr/bin/env python3
"""
Simple bulk email sender for LiteLLM user notifications.

This script reads configuration from environment variables,
loads CSV data, merges it with results, and sends personalized emails.

Usage:
    python litellm_bulk_sender.py
    
Configuration is read from .env file.
"""

import os
import sys
import time
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from gmail_client import GmailSender
from csv_utils import merge_csv_data, SafeFormatter
from email_logger import EmailLogger, EmailResult


class LiteLLMBulkSender:
    """Simple bulk email sender for LiteLLM notifications."""
    
    def __init__(self):
        self.load_config()
        self.gmail = GmailSender(self.client_secrets_path, self.token_path)
        self.logger = EmailLogger(Path(self.log_path))
        
    def load_config(self):
        """Load configuration from environment variables."""
        # Required settings
        self.csv_path = self._get_env_required("CSV_PATH")
        self.subject_template = self._get_env_required("SUBJECT")
        self.sender = self._get_env_required("SENDER")
        self.client_secrets_path = self._get_env_required("CLIENT_SECRETS_PATH")
        
        # Optional settings with defaults
        self.results_csv_path = os.getenv("RESULTS_CSV_PATH")
        self.body_file = os.getenv("BODY_FILE")
        self.body_template = os.getenv("BODY")
        self.token_path = os.getenv("TOKEN_PATH", "./credentials/token.json")
        self.to_field = os.getenv("TO_FIELD", "user_email")
        self.log_path = os.getenv("LOG_PATH", "logs/bulk_email_log.csv")
        self.dry_run = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")
        self.sleep_between = float(os.getenv("SLEEP_BETWEEN_SENDS", "0.5"))
        self.dedupe = os.getenv("DEDUPE", "true").lower() in ("true", "1", "yes")
        
        # Load body template
        if self.body_file:
            body_path = Path(self.body_file)
            if not body_path.exists():
                raise FileNotFoundError(f"Body template file not found: {self.body_file}")
            self.body_template = body_path.read_text(encoding="utf-8")
        elif not self.body_template:
            raise ValueError("Either BODY_FILE or BODY must be specified")
    
    def _get_env_required(self, key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def authenticate(self):
        """Authenticate with Gmail API."""
        print("Authenticating with Gmail...")
        self.gmail.authenticate()
        print("✓ Authentication successful")
    
    def send_emails(self):
        """Send bulk emails."""
        csv_path = Path(self.csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        results_csv_path = Path(self.results_csv_path) if self.results_csv_path else None
        if results_csv_path and not results_csv_path.exists():
            print(f"Warning: Results CSV not found: {self.results_csv_path}")
            results_csv_path = None
        
        print(f"Processing CSV: {csv_path}")
        if results_csv_path:
            print(f"Merging with results: {results_csv_path}")
        
        sent_emails = set()
        processed_count = 0
        
        for row_data in merge_csv_data(csv_path, results_csv_path):
            try:
                # Get recipient email
                to_email = row_data.get(self.to_field, "").strip()
                if not to_email:
                    self.logger.log_result(EmailResult(
                        to="", subject="", status="SKIPPED", 
                        error=f"Missing {self.to_field} field"
                    ))
                    continue
                
                # Check for duplicates
                if self.dedupe and to_email.lower() in sent_emails:
                    self.logger.log_result(EmailResult(
                        to=to_email, subject="", status="SKIPPED",
                        error="Duplicate email address"
                    ))
                    continue
                
                # Format subject and body
                formatter = SafeFormatter(row_data)
                subject = formatter.format(self.subject_template)
                body = formatter.format(self.body_template)
                
                if self.dry_run:
                    print(f"\\n--- DRY RUN ---")
                    print(f"To: {to_email}")
                    print(f"Subject: {subject}")
                    print(f"Body:\\n{body}")
                    print(f"--- END DRY RUN ---")
                    
                    self.logger.log_result(EmailResult(
                        to=to_email, subject=subject, status="DRY_RUN"
                    ))
                else:
                    # Send actual email
                    message = self.gmail.create_email(
                        to=to_email,
                        subject=subject,
                        body=body,
                        sender=self.sender
                    )
                    
                    message_id = self.gmail.send_email(message)
                    print(f"✓ Sent to {to_email}")
                    
                    self.logger.log_result(EmailResult(
                        to=to_email, subject=subject, status="SENT", 
                        message_id=message_id
                    ))
                    
                    # Rate limiting
                    if self.sleep_between > 0:
                        time.sleep(self.sleep_between)
                
                sent_emails.add(to_email.lower())
                processed_count += 1
                
            except Exception as e:
                error_msg = str(e)
                print(f"✗ Error sending to {to_email}: {error_msg}")
                self.logger.log_result(EmailResult(
                    to=to_email, subject=subject if 'subject' in locals() else "",
                    status="ERROR", error=error_msg
                ))
        
        mode = "DRY RUN" if self.dry_run else "ACTUAL"
        print(f"\\n{mode} completed. Processed {processed_count} emails.")
        print(f"Log saved to: {self.log_path}")


def main():
    """Main entry point."""
    try:
        sender = LiteLLMBulkSender()
        sender.authenticate()
        sender.send_emails()
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
