"""
Simple Gmail API wrapper for sending emails.
Handles OAuth authentication and email sending.
"""

import os
import base64
from pathlib import Path
from email.message import EmailMessage
from typing import Optional

import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials as UserCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"


class GmailSender:
    """Simple Gmail API client for sending emails."""
    
    def __init__(self, client_secrets_path: str, token_path: str):
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.service = None
        
    def authenticate(self):
        """Authenticate with Gmail API using OAuth."""
        creds = None
        token_file = Path(self.token_path)
        
        # Load existing token if available
        if token_file.exists():
            creds = UserCredentials.from_authorized_user_file(
                self.token_path, [GMAIL_SEND_SCOPE]
            )
        
        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # Get new token if needed
        if not creds or not creds.valid:
            if not Path(self.client_secrets_path).exists():
                raise FileNotFoundError(f"Client secrets file not found: {self.client_secrets_path}")
                
            flow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_path, [GMAIL_SEND_SCOPE]
            )
            creds = flow.run_local_server(port=0)
            
            # Save token for future use
            token_file.parent.mkdir(parents=True, exist_ok=True)
            token_file.write_text(creds.to_json(), encoding="utf-8")
        
        self.service = build("gmail", "v1", credentials=creds)
        
    def create_email(self, to: str, subject: str, body: str, sender: Optional[str] = None) -> EmailMessage:
        """Create an email message."""
        msg = EmailMessage()
        msg.set_content(body)
        msg["To"] = to
        msg["Subject"] = subject
        
        if sender:
            msg["From"] = sender
            
        return msg
    
    def send_email(self, message: EmailMessage) -> str:
        """Send an email and return the message ID."""
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
            
        encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded}
        
        sent = self.service.users().messages().send(
            userId="me", body=create_message
        ).execute()
        
        return sent.get("id", "")
