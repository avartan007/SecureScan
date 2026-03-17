#!/usr/bin/env python3
"""File security scanner with VirusTotal API integration."""

import hashlib
import os
import requests
from pathlib import Path

# Configuration
MAX_FILE_SIZE_MB = 32
SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".dll", ".scr"}
SAFE_EXTENSIONS = {".pdf", ".txt", ".jpg", ".jpeg", ".png", ".gif", ".zip", ".doc", ".docx"}


class FileScanner:
    """Scan files using VirusTotal API with local extension-based fallback."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.vt_base_url = "https://www.virustotal.com/api/v3"
        self.vt_headers = (
            {"x-apikey": api_key}
            if api_key
            else {}
        )

    def get_file_hash(self, file_path):
        """Compute SHA-256 hash of a file."""
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except OSError:
            return None

    def _check_virustotal_api(self, file_hash):
        """Query VirusTotal for file hash. Returns (risk_level, reason, stats)."""
        if not self.api_key:
            return None, None, None

        try:
            url = f"{self.vt_base_url}/files/{file_hash}"
            response = requests.get(url, headers=self.vt_headers, timeout=10)

            if response.status_code == 200:
                data = response.json().get("data", {})
                attrs = data.get("attributes", {})
                stats = attrs.get("last_analysis_stats", {})

                harmless = stats.get("harmless", 0)
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                undetected = stats.get("undetected", 0)
                total = harmless + malicious + suspicious + undetected

                # Threat decision logic
                if malicious >= 5:
                    risk = "MALICIOUS"
                    reason = f"{malicious} vendors flagged as malicious"
                elif malicious > 0:
                    risk = "SUSPICIOUS"
                    reason = f"{malicious} vendor(s) detected threat"
                elif suspicious > 0:
                    risk = "SUSPICIOUS"
                    reason = f"{suspicious} vendor(s) flagged as suspicious"
                elif harmless > 0:
                    risk = "CLEAN"
                    reason = "Verified safe by security vendors"
                else:
                    risk = "UNKNOWN"
                    reason = "No analysis available"

                stats_data = {"malicious": malicious, "suspicious": suspicious, "harmless": harmless, "total": total}
                return risk, reason, stats_data

            return None, None, None

        except Exception as e:
            return None, str(e), None

    def check_extension(self, file_path):
        """Heuristic-based risk classification from file extension."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in SUSPICIOUS_EXTENSIONS:
            return "SUSPICIOUS", f"Executable extension: {ext} (heuristic-based classification)"
        if ext in SAFE_EXTENSIONS:
            return "CLEAN", f"Known safe extension: {ext}"
        return "UNKNOWN", "Unknown extension (inconclusive)"

    def analyze_file(self, file_path):
        """Analyze a file and return detailed result."""
        file_path = str(file_path)
        filename = os.path.basename(file_path)

        # Check file size
        try:
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
        except OSError:
            return {
                "filename": filename,
                "status": "ERROR",
                "risk_level": "UNKNOWN",
                "reason": "Cannot read file"
            }

        if size_mb > MAX_FILE_SIZE_MB:
            return {
                "filename": filename,
                "status": "SKIPPED",
                "risk_level": "UNKNOWN",
                "reason": f"File too large ({size_mb:.1f} MB)"
            }

        # Compute hash
        file_hash = self.get_file_hash(file_path)
        if not file_hash:
            return {
                "filename": filename,
                "status": "ERROR",
                "hash": None,
                "risk_level": "UNKNOWN",
                "reason": "Cannot compute hash"
            }

        # Try VirusTotal first
        vt_risk, vt_reason, vt_stats = self._check_virustotal_api(file_hash)
        if vt_risk:
            return {
                "filename": filename,
                "hash": file_hash,
                "size_bytes": size_bytes,
                "status": "SCANNED",
                "risk_level": vt_risk,
                "reason": vt_reason,
                "source": "VirusTotal API",
                "stats": vt_stats
            }

        # Fall back to heuristic-based extension classification
        ext_risk, ext_reason = self.check_extension(file_path)
        return {
            "filename": filename,
            "hash": file_hash,
            "size_bytes": size_bytes,
            "status": "SCANNED",
            "risk_level": ext_risk,
            "reason": ext_reason,
            "source": "Heuristic Analysis",
            "stats": None
        }
