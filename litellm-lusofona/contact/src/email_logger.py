"""
Simple logging utility for email sending results.
"""

import csv
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


@dataclass
class EmailResult:
    """Result of sending an email."""
    to: str
    subject: str
    status: str  # SENT, ERROR, SKIPPED, DRY_RUN
    error: str = ""
    message_id: str = ""


class EmailLogger:
    """Simple CSV logger for email results."""
    
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Create log file with headers if it doesn't exist."""
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "to", "subject", "status", "message_id", "error"])
    
    def log_result(self, result: EmailResult):
        """Log an email result."""
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        
        with self.log_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                result.to,
                result.subject,
                result.status,
                result.message_id,
                result.error
            ])
