#!/usr/bin/env python
"""n8n workflow import/export tool for BelPro.

Usage:
  ./scripts/n8n_workflows.py import   # n8n/workflows/*.json to running n8n
  ./scripts/n8n_workflows.py export   # running n8n to n8n/workflows/*.json
"""

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

REQUEST_TIMEOUT = 10
PLACEHOLDER = "FILL_IN_AFTER_FIRST_N8N_RUN"
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
WORKFLOWS_DIR = PROJECT_DIR / "n8n" / "workflows"
ENV_FILE = PROJECT_DIR / ".env"


def load_env(env_path: pathlib.Path) -> dict:
    """Parse KEY=VALUE lines from a .env file; ignore comments and blanks."""
    env = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("'\"")
    return env


def make_filename(name: str) -> str:
    """Derive a safe filename slug from a workflow name (used by cmd_export)."""
    slug = name.lower().replace(" ", "_")
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    return slug


def api_request(method: str, url: str, api_key: str, payload: dict | None = None) -> tuple[int, dict]:
    """Make an authenticated request to the n8n API.

    Returns (status_code, response_dict).
    Exits with an error message if n8n is unreachable.
    """
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-N8N-API-KEY", api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw.decode(errors="replace")}
        return e.code, body
    except urllib.error.URLError:
        print("ERROR: Cannot reach n8n. Is 'docker compose up' running?")
        sys.exit(1)


def cmd_import(base_url: str, api_key: str) -> None:
    pass


def cmd_export(base_url: str, api_key: str) -> None:
    """Pull all workflows from n8n and write to n8n/workflows/."""
    status, data = api_request("GET", f"{base_url}/api/v1/workflows", api_key)
    if status != 200:
        print(f"ERROR: GET /api/v1/workflows returned HTTP {status}: {data}")
        sys.exit(1)

    workflows = data.get("data", [])
    if not workflows:
        print("No workflows found in n8n.")
        return

    count = 0
    for wf in workflows:
        wf_id = wf["id"]
        name = wf["name"]
        status, full = api_request("GET", f"{base_url}/api/v1/workflows/{wf_id}", api_key)
        if status != 200:
            print(f"  x {wf_id}: GET /{wf_id} returned HTTP {status}")
            continue
        filename = make_filename(name) + ".json"
        out_path = WORKFLOWS_DIR / filename
        out_path.write_text(json.dumps(full, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ok {filename}")
        count += 1

    print(f"\n{count} workflow(s) exported to n8n/workflows/")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("import", "export"):
        print(__doc__)
        sys.exit(1)

    if not ENV_FILE.exists():
        print(f"ERROR: .env not found at {ENV_FILE}")
        sys.exit(1)

    env = load_env(ENV_FILE)
    api_key = env.get("N8N_API_KEY", "")
    if not api_key or api_key == PLACEHOLDER:
        print("ERROR: N8N_API_KEY is not set in .env")
        print("  Go to n8n UI → Settings → API → Create API Key, then add it to .env")
        sys.exit(1)

    base_url = env.get("N8N_WEBHOOK_URL", "http://localhost:5678").rstrip("/")

    if sys.argv[1] == "import":
        cmd_import(base_url, api_key)
    else:
        cmd_export(base_url, api_key)


if __name__ == "__main__":
    main()
