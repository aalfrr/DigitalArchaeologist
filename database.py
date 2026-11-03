import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime


DATABASE_PATH = Path(__file__).parent / "history.db"


def initialize_database():
    """Create the scan history and file tracking tables."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                scan_time TEXT NOT NULL,
                finding_count INTEGER NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS file_state (
                file_path TEXT PRIMARY KEY,
                file_hash TEXT NOT NULL,
                last_scanned TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                finding_data TEXT NOT NULL
            )
        """)


def calculate_file_hash(file_path):
    """Calculate a SHA-256 fingerprint of a file's contents."""

    hasher = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def has_file_changed(file_path):
    """Check whether a file differs from its most recently scanned version."""

    path = str(Path(file_path).resolve())
    current_hash = calculate_file_hash(file_path)

    with sqlite3.connect(DATABASE_PATH) as connection:
        result = connection.execute("""
            SELECT file_hash
            FROM file_state
            WHERE file_path = ?
        """, (path,)).fetchone()

    if result is None:
        return True

    return current_hash != result[0]


def update_file_state(file_path):
    """Save the latest fingerprint after a successful scan."""

    path = str(Path(file_path).resolve())
    file_hash = calculate_file_hash(file_path)
    scan_time = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            INSERT INTO file_state (file_path, file_hash, last_scanned)
            VALUES (?, ?, ?)
            ON CONFLICT(file_path) DO UPDATE SET
                file_hash = excluded.file_hash,
                last_scanned = excluded.last_scanned
        """, (path, file_hash, scan_time))


def record_scan(file_path, finding_count):
    """Save the result of scanning a document."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            INSERT INTO scan_history (
                file_path,
                scan_time,
                finding_count
            )
            VALUES (?, ?, ?)
        """, (
            str(Path(file_path).resolve()),
            datetime.now().isoformat(timespec="seconds"),
            finding_count
        ))


def get_scan_history():
    """Return all recorded scans, newest first."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute("""
            SELECT file_path, scan_time, finding_count
            FROM scan_history
            ORDER BY scan_time DESC
        """)

        return cursor.fetchall()

def save_findings(file_path, findings):
    """Replace the saved findings for a document."""

    path = str(Path(file_path).resolve())

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "DELETE FROM findings WHERE file_path = ?",
            (path,)
        )

        for finding in findings:
            connection.execute("""
                INSERT INTO findings (file_path, finding_data)
                VALUES (?, ?)
            """, (path, json.dumps(finding)))


def get_all_findings():
    """Retrieve all previously saved findings."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            "SELECT finding_data FROM findings"
        ).fetchall()

    return [json.loads(row[0]) for row in rows]