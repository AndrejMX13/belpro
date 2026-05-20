#!/usr/bin/env python3
"""Delete photos for approved entries older than PHOTO_RETENTION_DAYS."""
from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
import requests


DATABASE_URL = os.environ["DATABASE_URL"]
API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
RETENTION_DAYS = int(os.environ.get("PHOTO_RETENTION_DAYS", "730"))


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={"service": "ops", "operation": "photo_cleanup", "message": message, "detail": detail},
            timeout=10,
        )
    except Exception:
        pass


def dsn_from_url(url: str) -> str:
    """Convert asyncpg DATABASE_URL to psycopg2 DSN."""
    return url.replace("postgresql+asyncpg://", "postgresql://")


def main() -> None:
    """Query approved entries older than retention cutoff, delete their photos and DB rows."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    print(f"[photo_cleanup] Retention cutoff: {cutoff.date()} ({RETENTION_DAYS} days)")

    try:
        conn = psycopg2.connect(dsn_from_url(DATABASE_URL))
    except Exception as e:
        report_error("DB connection failed", str(e))
        sys.exit(1)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id, p.photo_path
                FROM log_entry_photos p
                JOIN log_entries e ON e.id = p.log_entry_id
                WHERE e.status = 'approved'
                  AND e.created_at < %s
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
            print(f"[photo_cleanup] Found {len(rows)} photos to delete.")

            deleted_files = 0
            ids_to_delete = []

            for photo_id, photo_path in rows:
                path = Path(photo_path)
                if path.exists():
                    path.unlink()
                    deleted_files += 1
                else:
                    print(f"[photo_cleanup] File not found (skipping): {photo_path}")
                ids_to_delete.append(str(photo_id))

            if ids_to_delete:
                cur.execute(
                    "DELETE FROM log_entry_photos WHERE id = ANY(%s::uuid[])",
                    (ids_to_delete,),
                )
                deleted_rows = cur.rowcount
            else:
                deleted_rows = 0

            conn.commit()
            print(f"[photo_cleanup] Deleted {deleted_files} files, {deleted_rows} DB rows.")

    except Exception as e:
        conn.rollback()
        report_error("Photo cleanup failed", str(e))
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
