#!/usr/bin/env python3
"""SQLite-based threat intelligence database."""

import sqlite3
from datetime import datetime


class ThreatDatabase:
    """Store and query file threat history."""

    def __init__(self, db_path="threat_intelligence.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        """Create database tables."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    file_hash TEXT UNIQUE,
                    filename TEXT,
                    file_size INTEGER,
                    risk_level TEXT,
                    scan_source TEXT,
                    reason TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create scan history table for audit trail
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY,
                    file_hash TEXT,
                    filename TEXT,
                    file_size INTEGER,
                    risk_level TEXT,
                    scan_source TEXT,
                    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_file(self, file_hash, filename, file_size, risk_level, source, reason=None):
        """Record a scanned file."""
        try:
            with self.conn:
                self.conn.execute(
                    """INSERT INTO files 
                       (file_hash, filename, file_size, risk_level, scan_source, reason)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (file_hash, filename, file_size, risk_level, source, reason)
                )
        except sqlite3.IntegrityError:
            # File already exists, update last_updated
            with self.conn:
                self.conn.execute(
                    """UPDATE files SET last_updated = ?, scan_source = ?, reason = ? 
                       WHERE file_hash = ?""",
                    (datetime.now().isoformat(), source, reason, file_hash)
                )
        
        # Always add to history for audit trail
        try:
            with self.conn:
                self.conn.execute(
                    """INSERT INTO scan_history
                       (file_hash, filename, file_size, risk_level, scan_source)
                       VALUES (?, ?, ?, ?, ?)""",
                    (file_hash, filename, file_size, risk_level, source)
                )
        except:
            pass

    def get_file(self, file_hash):
        """Look up a file by hash."""
        cursor = self.conn.execute(
            "SELECT * FROM files WHERE file_hash = ?",
            (file_hash,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "hash": row[1],
                "filename": row[2],
                "size": row[3],
                "risk_level": row[4],
                "source": row[5],
                "first_seen": row[6],
                "last_updated": row[7]
            }
        return None

    def is_known_malicious(self, file_hash):
        """Check if hash is in database and is malicious."""
        file_info = self.get_file(file_hash)
        return file_info and file_info.get("risk_level") == "MALICIOUS"

    def get_recent_scans(self, limit=10):
        """Get recent scan history."""
        try:
            cursor = self.conn.execute(
                """SELECT file_hash, filename, risk_level, scanned_at 
                   FROM scan_history 
                   ORDER BY scanned_at DESC LIMIT ?""",
                (limit,)
            )
            scans = []
            for row in cursor.fetchall():
                scans.append({
                    "hash": row[0][:16] + "..." if row[0] else None,
                    "filename": row[1],
                    "risk_level": row[2],
                    "timestamp": row[3]
                })
            return scans
        except Exception as e:
            return []

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
