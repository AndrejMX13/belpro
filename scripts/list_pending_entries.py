"""Print pending_manager entries as JSON for the manual trigger node.

Usage:
  python scripts/list_pending_entries.py          # from repo root
  python scripts/list_pending_entries.py --all    # include already-notified entries

Output is one JSON object per line — ready to copy into the n8n manual trigger.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

API_BASE = os.getenv("BELPRO_API_URL", "http://localhost:8100/api")


def _auth() -> tuple[str, str]:
    password = os.getenv("MANAGER_PASSWORD", "")
    if not password:
        sys.exit("MANAGER_PASSWORD not set — source .env first or set env var")
    return ("manager", password)


def _get(url: str) -> dict:
    r = requests.get(url, auth=_auth(), timeout=10)
    r.raise_for_status()
    return r.json()


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="List pending log entries for n8n manual trigger")
    parser.add_argument("--all", action="store_true", help="Include entries already notified to manager")
    args = parser.parse_args()

    entries_resp = _get(f"{API_BASE}/log-entries?status=pending_manager")
    items = entries_resp.get("items", [])

    if not args.all:
        items = [e for e in items if not e.get("manager_notified_at")]

    if not items:
        print("No pending entries found.", file=sys.stderr)
        return

    manager_resp = _get(f"{API_BASE}/managers/me")
    manager_phone = manager_resp.get("phone", "")

    for entry in items:
        volunteer = _get(f"{API_BASE}/volunteers/{entry['volunteer_id']}")
        manual_json = {
            "entry_id": entry["id"],
            "hours": float(entry["hours"]),
            "activity_description": entry["activity_description"],
            "location": entry.get("location") or "",
            "volunteer_name": f"{volunteer['first_name']} {volunteer['last_name']}",
            "entry_date": entry["entry_date"],
            "manager_phone": manager_phone,
        }
        print(json.dumps(manual_json, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()
