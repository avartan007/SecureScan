#!/usr/bin/env python3
"""Organize files by security classification."""

import os
import shutil
from pathlib import Path


class FileRouter:
    """Route files to categorized directories based on risk level."""

    def __init__(self, files_dir="./files"):
        self.files_dir = files_dir
        self.clean_dir = os.path.join(files_dir, "approved")
        self.suspicious_dir = os.path.join(files_dir, "suspicious")
        self.quarantine_dir = os.path.join(files_dir, "quarantine")
        self.duplicates_dir = os.path.join(files_dir, "duplicates")

        # Create directories
        for d in [self.clean_dir, self.suspicious_dir, self.quarantine_dir, self.duplicates_dir]:
            os.makedirs(d, exist_ok=True)

    def route_file(self, source_path, filename, risk_level, is_duplicate=False):
        """Route a file to appropriate directory."""
        source_path = str(source_path)

        if not os.path.exists(source_path):
            return False, "Source file not found"

        try:
            if is_duplicate:
                dest = os.path.join(self.duplicates_dir, filename)
            elif risk_level == "CLEAN":
                dest = os.path.join(self.clean_dir, filename)
            elif risk_level == "MALICIOUS":
                dest = os.path.join(self.quarantine_dir, filename)
            else:  # SUSPICIOUS or UNKNOWN
                dest = os.path.join(self.suspicious_dir, filename)

            # Handle filename conflicts
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(os.path.dirname(dest), f"{base}_{counter}{ext}")
                counter += 1

            shutil.copy2(source_path, dest)
            return True, f"Moved to {os.path.basename(os.path.dirname(dest))}"

        except Exception as e:
            return False, str(e)
