#!/usr/bin/env python3
"""Ops HTTP notification server.

Listens on port 9000 for reconfiguration notifications from the API.
ThreadingHTTPServer handles each request in its own thread; the main
loop never blocks.

Endpoints:
    GET  /health      — Docker healthcheck
    POST /reconfigure — Regenerate crontab and reload crond
"""
from __future__ import annotations

import json
import logging
import os
import signal
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg2
import requests

API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
PORT = int(os.environ.get("OPS_SERVER_PORT", "9000"))
CRONTAB_PATH = Path("/etc/crontabs/ops")

logging.basicConfig(
    level=logging.INFO,
    format="[ops_server] %(levelname)s %(message)s",
    stream=__import__("sys").stdout,
)
logger = logging.getLogger(__name__)

# All four cron lines are dynamic; hours/day/period are runtime-tunable.
CRONTAB_TEMPLATE = (
    "# m h dom mon dow command\n"
    "0 {backup_hour} * * * /app/scripts/backup.sh {retention_days} >> /proc/1/fd/1 2>&1\n"
    "0 {cleanup_hour} * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1\n"
    "0 {report_hour} {day} * * /app/scripts/monthly_report_send.py --period {period}"
    " >> /proc/1/fd/1 2>&1\n"
)


def _dsn(url: str) -> str:
    """Convert asyncpg DATABASE_URL to a psycopg2-compatible DSN."""
    return url.replace("postgresql+asyncpg://", "postgresql://")


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log. Best-effort — never raises."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={
                "service": "ops",
                "operation": "ops_server",
                "message": message,
                "detail": detail,
            },
            timeout=10,
        )
    except Exception:
        pass


def reload_crond() -> None:
    """Send SIGHUP to crond so it reloads the crontab file."""
    result = subprocess.run(["pidof", "crond"], capture_output=True, text=True)
    pid_str = result.stdout.strip()
    if not pid_str:
        raise RuntimeError("crond process not found via pidof")
    os.kill(int(pid_str), signal.SIGHUP)


def write_crontab(
    day: int, period: str, backup_hour: int, cleanup_hour: int, retention_days: int,
    report_hour: int = 7,
) -> None:
    """Write a new crontab to CRONTAB_PATH and reload crond."""
    content = CRONTAB_TEMPLATE.format(
        day=day,
        period=period,
        backup_hour=backup_hour,
        cleanup_hour=cleanup_hour,
        retention_days=retention_days,
        report_hour=report_hour,
    )
    CRONTAB_PATH.write_text(content)
    reload_crond()
    logger.info(
        "Crontab updated: day=%d period=%s report_hour=%d backup_hour=%d cleanup_hour=%d retention_days=%d",
        day, period, report_hour, backup_hour, cleanup_hour, retention_days,
    )


def fetch_settings_from_db() -> dict[str, str]:
    """Read report_auto_day and report_auto_period from the settings table.

    Returns an empty dict on any failure (caller falls back to defaults).
    Retries 3 times with 2-second gaps to handle slow DB startup.
    """
    for attempt in range(3):
        try:
            conn = psycopg2.connect(_dsn(DATABASE_URL))
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT name, value FROM settings"
                    " WHERE name IN ('report_auto_day', 'report_auto_period',"
                    " 'report_auto_hour', 'backup_hour', 'photo_cleanup_hour',"
                    " 'backup_retention_days')"
                )
                rows = {name: value for name, value in cur.fetchall()}
            conn.close()
            return rows
        except Exception as exc:
            logger.warning("Settings fetch attempt %d/3 failed: %s", attempt + 1, exc)
            if attempt < 2:
                time.sleep(2)
    return {}


class _Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the ops notification server."""

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        logger.info(fmt, *args)

    def _send(self, status: int, body: bytes = b"", content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, b'{"status":"ok"}')
        else:
            self._send(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/reconfigure":
            self._send(404)
            return

        if self.headers.get("X-Internal-Key", "") != API_SECRET_KEY:
            self._send(403)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")

        # Respond immediately — this thread continues working after the response.
        self._send(202)

        raw_day = int(payload.get("report_auto_day", 28))
        day = max(1, min(raw_day, 28))
        raw_period = str(payload.get("report_auto_period", "current"))
        period = raw_period if raw_period in ("current", "previous") else "current"
        backup_hour = max(0, min(int(payload.get("backup_hour", 2)), 23))
        cleanup_hour = max(0, min(int(payload.get("photo_cleanup_hour", 3)), 23))
        retention_days = max(1, int(payload.get("backup_retention_days", 30)))
        report_hour = max(0, min(int(payload.get("report_auto_hour", 7)), 23))
        try:
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days, report_hour=report_hour)
        except Exception as exc:
            logger.error("Crontab update failed: %s", exc)
            report_error("Crontab update failed", str(exc))


def main() -> None:
    """Sync crontab with DB settings, then start the notification server."""
    logger.info("Fetching settings from DB for startup crontab sync...")
    rows = fetch_settings_from_db()
    if rows:
        day = int(rows.get("report_auto_day", 28))
        period = rows.get("report_auto_period", "current") or "current"
        backup_hour = max(0, min(int(rows.get("backup_hour", 2)), 23))
        cleanup_hour = max(0, min(int(rows.get("photo_cleanup_hour", 3)), 23))
        retention_days = max(1, int(rows.get("backup_retention_days", 30)))
        report_hour = max(0, min(int(rows.get("report_auto_hour", 7)), 23))
        try:
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days, report_hour=report_hour)
            logger.info(
                "Startup crontab sync complete (day=%d, period=%s, report_hour=%d, backup_hour=%d, cleanup_hour=%d, retention_days=%d).",
                day, period, report_hour, backup_hour, cleanup_hour, retention_days,
            )
        except Exception as exc:
            logger.warning("Startup crontab sync failed; baked-in default remains: %s", exc)
    else:
        logger.warning("No settings in DB; baked-in default crontab remains.")

    server = ThreadingHTTPServer(("0.0.0.0", PORT), _Handler)
    logger.info("Ops server listening on port %d.", PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
