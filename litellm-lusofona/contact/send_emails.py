#!/usr/bin/env python3
"""Simple wrapper to run bulk_email_sender.py with .env configuration."""

import subprocess
import sys
from pathlib import Path

# Change to the script directory so .env is found
script_dir = Path(__file__).parent
script_path = script_dir / "bulk_email_sender.py"

# Run the main script
result = subprocess.run([sys.executable, str(script_path)] + sys.argv[1:], cwd=script_dir)
sys.exit(result.returncode)
