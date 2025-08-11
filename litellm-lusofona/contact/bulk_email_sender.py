"""
Bulk email sender for Google Workspace Gmail using a CSV file and simple string templates.

Features
- Reads recipients and merge fields from a CSV (headers become template variables)
- Subject/body templating with Python format placeholders like {user_email} or {teams}
- Dry-run mode for previews
- Dedupe recipients by email (on by default)
- Simple rate limiting between sends
- CSV log of results

Auth
- Uses Application Default Credentials via google-auth. Provide credentials with Gmail send scope.
- If using a service account with domain-wide delegation, set GMAIL_IMPERSONATE to the user to send as.

Example
python3 bulk_email_sender.py \
  --csv ../docs/bulk_teachers_dsi-teste.csv \
  --subject "Welcome to LusoChat for {teams}" \
  --body-file templates/body_example.txt \
  --dry-run
"""

from __future__ import annotations

import argparse
import base64
import csv
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Iterable, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Google libs are imported lazily so dry-run works without them installed


GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
GMAIL_READ_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GMAIL_SETTINGS_SCOPE = "https://www.googleapis.com/auth/gmail.settings.basic"


class SafeDict(dict):
    """Default missing format keys to empty string to avoid KeyError."""

    def __missing__(self, key):  # type: ignore[override]
        return ""


@dataclass
class SendResult:
    to: str
    subject: str
    status: str
    error: str = ""
    id: str = ""


def str_to_bool(value: str) -> bool:
    """Convert string to boolean, handling common true/false representations."""
    if isinstance(value, bool):
        return value
    return value.lower() in ('true', '1', 'yes', 'on')


def load_text(value: Optional[str], file: Optional[str]) -> str:
    if value and file:
        raise ValueError("Provide either an inline value or a file, not both.")
    if file:
        return Path(file).read_text(encoding="utf-8")
    return value or ""


def build_gmail_service(scopes: Optional[list[str]] = None, *, auth_mode: str = "auto", client_secrets: Optional[str] = None, token_path: Optional[str] = None, impersonate: Optional[str] = None):
    """Build a Gmail API service using either ADC, OAuth (installed app), or SA with impersonation.

    auth_mode: 'auto' (default), 'adc', or 'oauth'
    client_secrets: path to OAuth client_secret.json (for 'oauth' or 'auto')
    token_path: path to store OAuth token.json
    impersonate: user to impersonate when using a service account with DWD
    """
    # Lazy imports so --dry-run doesn't require Google packages
    import google.auth  # type: ignore
    from googleapiclient.discovery import build  # type: ignore
    from google.oauth2 import service_account  # type: ignore
    from google.oauth2.credentials import Credentials as UserCredentials  # type: ignore
    from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
    from google.auth.transport.requests import Request  # type: ignore

    scopes = scopes or [GMAIL_SEND_SCOPE]

    def get_oauth_creds() -> UserCredentials:
        nonlocal client_secrets, token_path
        # Default paths inside current working dir if not provided
        if not client_secrets:
            # Try credentials folder first, then current directory
            creds_dir = Path.cwd() / "credentials"
            if creds_dir.exists():
                # Look for any client_secret_*.json file in credentials/
                secret_files = list(creds_dir.glob("client_secret_*.json"))
                if secret_files:
                    client_secrets = str(secret_files[0])
            
            # Fallback to current directory
            if not client_secrets:
                secret_files = list(Path.cwd().glob("client_secret_*.json"))
                if secret_files:
                    client_secrets = str(secret_files[0])
        if not client_secrets or not Path(client_secrets).exists():
            raise RuntimeError("OAuth selected but client_secret.json was not found; pass --client-secrets")

        if not token_path:
            token_path = str(Path.cwd() / "credentials" / "token.json")

        creds: Optional[UserCredentials] = None
        token_file = Path(token_path)
        if token_file.exists():
            creds = UserCredentials.from_authorized_user_file(token_path, scopes)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets, scopes)
            creds = flow.run_local_server(port=0)
            token_file.write_text(creds.to_json(), encoding="utf-8")
        return creds

    def get_adc_or_sa_creds():
        creds, _ = google.auth.default(scopes=scopes)
        try:
            if isinstance(creds, service_account.Credentials):
                subject_user = impersonate or os.getenv("GMAIL_IMPERSONATE")
                if subject_user:
                    creds = creds.with_subject(subject_user)
        except Exception:
            pass
        return creds

    # Decide mode
    if auth_mode == "oauth":
        creds = get_oauth_creds()
    elif auth_mode == "adc":
        creds = get_adc_or_sa_creds()
    else:  # auto
        # Prefer OAuth if a client secret is present; otherwise ADC/SA
        has_cs = bool(client_secrets and Path(client_secrets).exists()) or (Path.cwd() / "client_secret.json").exists()
        creds = get_oauth_creds() if has_cs else get_adc_or_sa_creds()

    return build("gmail", "v1", credentials=creds)


def get_profile_email(service) -> str:
    """Return the primary email of the authenticated/impersonated user."""
    prof = service.users().getProfile(userId="me").execute()
    return prof.get("emailAddress", "")


def list_send_as(service) -> list[str]:
    """Return the list of allowed send-as addresses for the user."""
    try:
        sendas_list = (
            service.users().settings().sendAs().list(userId="me").execute()
        )
        return [item.get("sendAsEmail", "") for item in sendas_list.get("sendAs", [])]
    except Exception:
        return []


def compose_email(
    to_addr: str,
    subject_tpl: str,
    body_tpl: str,
    row: Dict[str, str],
    sender: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
) -> EmailMessage:
    ctx = SafeDict(row)
    subject = subject_tpl.format_map(ctx)
    body = body_tpl.format_map(ctx)

    msg = EmailMessage()
    msg.set_content(body)
    msg["To"] = to_addr
    if sender:
        msg["From"] = sender
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    if reply_to:
        msg["Reply-To"] = reply_to
    msg["Subject"] = subject
    return msg


def send_via_gmail(service, message: EmailMessage) -> str:
    # Lazy import so dry-run doesn't require base packages beyond stdlib
    # (base64 is stdlib; only discovery is needed in build)
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded}
    sent = (
        service.users().messages().send(userId="me", body=create_message).execute()
    )
    return sent.get("id", "")


def iter_rows(csv_path: Path, results_csv: Optional[Path] = None) -> Iterable[Dict[str, str]]:
    """
    Iterate over CSV rows, optionally merging with results CSV data.
    
    If results_csv is provided, it will merge data based on user_email field.
    This allows combining original CSV data with generated credentials/links.
    """
    # Load results data if provided
    results_data = {}
    if results_csv and results_csv.exists():
        with results_csv.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("user_email", "").strip().lower()
                if email:
                    # Normalize keys and store
                    results_data[email] = {k.strip(): (v or "").strip() for k, v in row.items()}
    
    # Iterate main CSV and merge with results
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize main row
            normalized_row = {k.strip(): (v or "").strip() for k, v in row.items()}
            
            # Merge with results data if available
            email = normalized_row.get("user_email", "").strip().lower()
            if email in results_data:
                # Merge results data, with results taking precedence for conflicts
                normalized_row.update(results_data[email])
            
            yield normalized_row


def write_log_header(log_path: Path):
    if not log_path.exists():
        # Ensure the parent directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "to", "subject", "status", "id", "error"])


def append_log(log_path: Path, res: SendResult):
    with log_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                datetime.utcnow().isoformat(timespec="seconds") + "Z",
                res.to,
                res.subject,
                res.status,
                res.id,
                res.error,
            ]
        )


def run(args) -> int:
    # Identity check mode
    if args.whoami:
        try:
            service = build_gmail_service(
                scopes=[GMAIL_SEND_SCOPE, GMAIL_READ_SCOPE, GMAIL_SETTINGS_SCOPE],
                auth_mode=args.auth,
                client_secrets=args.client_secrets,
                token_path=args.token,
                impersonate=args.impersonate,
            )
            me = get_profile_email(service)
            aliases = list_send_as(service)
            print(f"Authenticated as: {me}")
            if aliases:
                print("Send-as addresses:")
                for a in aliases:
                    print(f" - {a}")
            else:
                print("No additional send-as aliases configured.")
            return 0
        except Exception as e:
            print(f"Failed to resolve identity: {e}", file=sys.stderr)
            return 2

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        return 2

    subject_tpl = load_text(args.subject, args.subject_file)
    body_tpl = load_text(args.body, args.body_file)
    if not subject_tpl:
        print("Missing --subject or --subject-file", file=sys.stderr)
        return 2
    if not body_tpl:
        print("Missing --body or --body-file", file=sys.stderr)
        return 2

    to_field = args.to_field
    log_path = Path(args.log)
    write_log_header(log_path)

    sent_emails = set()
    processed = 0

    service = None if args.dry_run else build_gmail_service(
        scopes=[GMAIL_SEND_SCOPE],
        auth_mode=args.auth,
        client_secrets=args.client_secrets,
        token_path=args.token,
        impersonate=args.impersonate,
    )

    # Parse results CSV path if provided
    results_csv_path = None
    if args.results_csv:
        results_csv_path = Path(args.results_csv)
        if not results_csv_path.exists():
            print(f"Results CSV not found: {results_csv_path}", file=sys.stderr)
            return 2

    for row in iter_rows(csv_path, results_csv_path):
        if args.limit and processed >= args.limit:
            break

        to_addr = row.get(to_field, "").strip()
        subject_rendered = ""
        if not to_addr:
            append_log(log_path, SendResult(to="", subject="", status="SKIPPED", error=f"Missing {to_field}"))
            continue

        normalized = to_addr.lower()
        if args.dedupe and normalized in sent_emails:
            append_log(log_path, SendResult(to=to_addr, subject="", status="SKIPPED", error="duplicate"))
            continue

        try:
            msg = compose_email(
                to_addr=to_addr,
                subject_tpl=subject_tpl,
                body_tpl=body_tpl,
                row=row,
                sender=args.sender,
                cc=args.cc,
                bcc=args.bcc,
                reply_to=args.reply_to,
            )

            subject_rendered = msg.get("Subject", "")

            if args.dry_run:
                print("--- DRY RUN ---")
                print("To:", to_addr)
                if args.sender:
                    print("From:", args.sender)
                print("Subject:", subject_rendered)
                print("Body:\n" + msg.get_content())
                append_log(log_path, SendResult(to=to_addr, subject=subject_rendered, status="DRY_RUN"))
            else:
                message_id = send_via_gmail(service, msg)
                append_log(
                    log_path,
                    SendResult(to=to_addr, subject=subject_rendered, status="SENT", id=message_id),
                )
                if args.sleep > 0:
                    time.sleep(args.sleep)

            sent_emails.add(normalized)
            processed += 1

        except Exception as e:  # Keep going while logging errors
            append_log(log_path, SendResult(to=to_addr, subject=subject_rendered, status="ERROR", error=str(e)))

    print(f"Done. Processed {processed} row(s). Log: {log_path}")
    return 0


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Bulk Gmail sender from CSV with templating")
    
    # Override defaults with environment variables
    def env_default(env_key: str, default_value=None, type_func=str):
        env_val = os.getenv(env_key)
        if env_val is None:
            return default_value
        if type_func == bool:
            return str_to_bool(env_val)
        return type_func(env_val) if env_val else default_value

    p.add_argument("--whoami", action="store_true", 
                   default=env_default("WHOAMI", False, bool),
                   help="Print Gmail identity and send-as aliases, then exit")
    p.add_argument("--auth", choices=["auto", "adc", "oauth"], 
                   default=env_default("AUTH_MODE", "auto"), 
                   help="Auth mode: Application Default Credentials (adc), OAuth installed app (oauth), or auto-detect (default: auto)")
    p.add_argument("--client-secrets", 
                   default=env_default("CLIENT_SECRETS_PATH"),
                   help="Path to OAuth client_secret.json (for --auth oauth or auto)")
    p.add_argument("--token", 
                   default=env_default("TOKEN_PATH"),
                   help="Path to OAuth token cache file (default: ./token.json if OAuth is used)")
    p.add_argument("--impersonate", 
                   default=env_default("GMAIL_IMPERSONATE"),
                   help="User to impersonate when using a service account with domain-wide delegation (or set GMAIL_IMPERSONATE)")
    p.add_argument("--csv", 
                   default=env_default("CSV_PATH"),
                   help="Path to CSV input file")
    p.add_argument("--results-csv",
                   default=env_default("RESULTS_CSV_PATH"),
                   help="Path to results CSV with credentials and links (optional)")
    p.add_argument("--to-field",
                   default=env_default("TO_FIELD", "user_email"),
                   help="CSV column name for recipient email (default: user_email)")
    p.add_argument("--sender", 
                   default=env_default("SENDER"),
                   help="Optional From header value")
    p.add_argument("--cc", 
                   default=env_default("CC"),
                   help="Optional static CC addresses (comma-separated)")
    p.add_argument("--bcc", 
                   default=env_default("BCC"),
                   help="Optional static BCC addresses (comma-separated)")
    p.add_argument("--reply-to", 
                   default=env_default("REPLY_TO"),
                   help="Optional Reply-To address")

    # Subject and body - check env vars first, then require one or the other
    subject_env = env_default("SUBJECT")
    subject_file_env = env_default("SUBJECT_FILE")
    body_env = env_default("BODY")
    body_file_env = env_default("BODY_FILE")
    
    # Make subject/body optional if provided via env
    gsubj = p.add_mutually_exclusive_group(required=not (subject_env or subject_file_env))
    gsubj.add_argument("--subject", default=subject_env, help="Inline subject template string")
    gsubj.add_argument("--subject-file", default=subject_file_env, help="Path to subject template file")

    gbody = p.add_mutually_exclusive_group(required=not (body_env or body_file_env))
    gbody.add_argument("--body", default=body_env, help="Inline body template string")
    gbody.add_argument("--body-file", default=body_file_env, help="Path to body template file")

    p.add_argument("--log", 
                   default=env_default("LOG_PATH", "logs/bulk_email_log.csv"), 
                   help="Path to CSV log (default: logs/bulk_email_log.csv)")
    p.add_argument("--dedupe", action="store_true", 
                   default=env_default("DEDUPE", True, bool),
                   help="Dedupe by recipient email (default: on)")
    p.add_argument("--no-dedupe", dest="dedupe", action="store_false", help="Disable dedupe")
    p.add_argument("--sleep", type=float, 
                   default=env_default("SLEEP_BETWEEN_SENDS", 0.0, float), 
                   help="Seconds to sleep between sends (default: 0)")
    p.add_argument("--limit", type=int, 
                   default=env_default("LIMIT", None, lambda x: int(x) if x else None),
                   help="Optional maximum number of rows to process")
    p.add_argument("--dry-run", action="store_true", 
                   default=env_default("DRY_RUN", False, bool),
                   help="Preview messages without sending")
    
    args = p.parse_args(argv)
    
    # Validate required args after env defaults
    if not args.csv:
        p.error("CSV path is required (set CSV_PATH in .env or use --csv)")
    
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
