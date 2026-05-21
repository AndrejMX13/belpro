#!/usr/bin/env python3
"""Auto monthly report sender — called by crond on the configured day.

Usage: monthly_report_send.py --period {current,previous}
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={
                "service": "ops",
                "operation": "monthly_report_send",
                "message": message,
                "detail": detail,
            },
            timeout=10,
        )
    except Exception:
        pass


def resolve_period(period: str) -> tuple[int, int]:
    """Return (year, month) for the given period label.

    'current'  → today's year and month.
    'previous' → the previous calendar month (handles Jan → Dec year rollover).
    """
    today = datetime.now(timezone.utc)
    if period == "previous":
        ref = today.replace(day=1) - timedelta(days=1)
        return ref.year, ref.month
    return today.year, today.month


def main() -> None:
    """Resolve target month and call the send-monthly API endpoint."""
    parser = argparse.ArgumentParser(description="Send monthly reports via BelPro API.")
    parser.add_argument("--period", choices=["current", "previous"], required=True)
    args = parser.parse_args()

    year, month = resolve_period(args.period)
    print(
        f"[monthly_report_send] Sending reports for {year}-{month:02d}"
        f" (period={args.period})"
    )

    try:
        r = requests.post(
            f"{API_URL}/api/reports/send-monthly",
            params={"year": year, "month": month},
            headers={"X-Internal-Key": API_SECRET_KEY},
            timeout=300,
        )
        r.raise_for_status()
        data = r.json()
        sent_email = len(data.get("sent_via_email", []))
        sent_wa = len(data.get("sent_via_whatsapp", []))
        errors = data.get("errors", [])
        print(
            f"[monthly_report_send] Done: {sent_email} email, {sent_wa} WhatsApp"
            f", {len(errors)} errors"
        )
        if errors:
            for e in errors:
                print(f"[monthly_report_send] ERROR: {e}")
    except Exception as exc:
        report_error("Monthly report send failed", str(exc))
        print(f"[monthly_report_send] FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
