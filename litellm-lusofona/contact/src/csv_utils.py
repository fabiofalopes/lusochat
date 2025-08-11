"""
CSV utilities for bulk email processing.
Handles loading and merging CSV data.
"""

import csv
from pathlib import Path
from typing import Dict, Iterator, Optional


def load_csv_data(csv_path: Path) -> Iterator[Dict[str, str]]:
    """Load and normalize CSV data."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize: strip whitespace from keys and values
            yield {k.strip(): (v or "").strip() for k, v in row.items()}


def merge_csv_data(main_csv: Path, results_csv: Optional[Path] = None) -> Iterator[Dict[str, str]]:
    """
    Load main CSV data and optionally merge with results CSV.
    Merging is done based on 'user_email' field.
    """
    # Load results data if provided
    results_data = {}
    if results_csv and results_csv.exists():
        for row in load_csv_data(results_csv):
            email = row.get("user_email", "").strip().lower()
            if email:
                results_data[email] = row
    
    # Iterate main CSV and merge with results
    for row in load_csv_data(main_csv):
        email = row.get("user_email", "").strip().lower()
        
        # Merge with results data if available
        if email in results_data:
            # Results data takes precedence for conflicting fields
            merged_row = row.copy()
            merged_row.update(results_data[email])
            yield merged_row
        else:
            yield row


class SafeFormatter:
    """Template formatter that handles missing keys gracefully."""
    
    def __init__(self, data: Dict[str, str]):
        self.data = data
    
    def format(self, template: str) -> str:
        """Format template, replacing missing keys with empty strings."""
        try:
            return template.format(**self.data)
        except KeyError as e:
            # Handle missing keys by replacing them with empty strings
            safe_data = {k: v for k, v in self.data.items()}
            # Add any missing keys as empty strings
            import re
            missing_keys = re.findall(r'{(\w+)}', template)
            for key in missing_keys:
                if key not in safe_data:
                    safe_data[key] = ""
            return template.format(**safe_data)
