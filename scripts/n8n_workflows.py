#!/usr/bin/env python
"""n8n workflow import/export tool for BelPro.

Usage:
  ./scripts/n8n_workflows.py import   # n8n/workflows/*.json to running n8n
  ./scripts/n8n_workflows.py export   # running n8n to n8n/workflows/*.json
"""

import json
import pathlib
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


def resolve_workflow_refs(payload: dict, n8n_by_name: dict[str, str]) -> bool:
    """Replace name-based workflow references with live n8n IDs.

    Handles settings.errorWorkflow and nodes[*].parameters.workflowId.
    Returns True if any substitution was made.
    """
    changed = False
    settings = payload.get("settings", {})
    ref = settings.get("errorWorkflow")
    if isinstance(ref, str) and ref in n8n_by_name:
        settings["errorWorkflow"] = n8n_by_name[ref]
        changed = True
    for node in payload.get("nodes", []):
        params = node.get("parameters", {})
        wf_id = params.get("workflowId")
        if isinstance(wf_id, str) and wf_id in n8n_by_name:
            params["workflowId"] = n8n_by_name[wf_id]
            changed = True
    return changed


def cmd_import(base_url: str, api_key: str) -> None:
    """Load each repo workflow file into n8n (upsert + activate)."""
    _all = sorted(p for p in WORKFLOWS_DIR.glob("*.json") if p.name != ".gitkeep")
    files = sorted(_all, key=lambda p: (0 if p.name == "error_handler.json" else 1, p.name))
    if not files:
        print("No workflow JSON files found in n8n/workflows/")
        return

    n8n_by_name: dict[str, str] = {}
    cursor = None
    while True:
        url = f"{base_url}/api/v1/workflows"
        if cursor:
            url += f"?cursor={cursor}"
        list_status, data = api_request("GET", url, api_key)
        if list_status != 200:
            print(f"ERROR: GET /api/v1/workflows returned HTTP {list_status}: {data}")
            sys.exit(1)
        for wf in data.get("data", []):
            n8n_by_name[wf["name"]] = wf["id"]
        cursor = data.get("nextCursor")
        if not cursor:
            break

    ok = 0
    # Fields to preserve when upserting (read-only fields are excluded)
    allowed_top_level = {
        "name",
        "nodes",
        "connections",
        "settings",
        "description",
        "staticData",
        "pinData",
    }
    # Valid settings keys (others are API-internal, read-only, or not accepted by the API)
    allowed_settings = {
        "executionOrder",
        "errorWorkflow",
        "saveDataErrorExecution",
        "saveDataSuccessExecution",
        "saveManualExecutions",
        "saveExecutionProgress",
        "timezone",
    }

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  x {path.name}: could not parse JSON ({exc})")
            continue

        name = payload.get("name", "")
        if not name:
            print(f"  ! {path.name}: missing or empty 'name' field - skipping")
            continue

        # Filter to only allowed fields
        filtered_payload = {k: v for k, v in payload.items() if k in allowed_top_level}

        # Clean up description: convert None to empty string
        if "description" in filtered_payload and filtered_payload["description"] is None:
            filtered_payload["description"] = ""

        # Filter settings to only allowed keys
        if "settings" in filtered_payload and isinstance(filtered_payload["settings"], dict):
            filtered_payload["settings"] = {
                k: v
                for k, v in filtered_payload["settings"].items()
                if k in allowed_settings
            }

        if name in n8n_by_name:
            wf_id = n8n_by_name[name]
            upsert_status, resp = api_request(
                "PUT", f"{base_url}/api/v1/workflows/{wf_id}", api_key, filtered_payload
            )
            action = "updated"
        else:
            upsert_status, resp = api_request(
                "POST", f"{base_url}/api/v1/workflows", api_key, filtered_payload
            )
            wf_id = resp.get("id")
            if not wf_id:
                print(f"  x {name}: created but response missing 'id' field")
                continue
            n8n_by_name[name] = wf_id
            action = "created"

        if upsert_status not in (200, 201):
            print(f"  x {name}: HTTP {upsert_status} - {resp}")
            continue

        act_status, _ = api_request(
            "POST", f"{base_url}/api/v1/workflows/{wf_id}/activate", api_key
        )
        if act_status not in (200, 201):
            print(f"  ! {name}: {action} but activation failed (HTTP {act_status})")
        else:
            print(f"  ok {name}: {action} and activated")
            ok += 1

    # Second pass: resolve name-based workflow references to live n8n IDs.
    ref_ok = 0
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        name = payload.get("name", "")
        if not name or name not in n8n_by_name:
            continue
        filtered = {k: v for k, v in payload.items() if k in allowed_top_level}
        if "description" in filtered and filtered["description"] is None:
            filtered["description"] = ""
        if "settings" in filtered and isinstance(filtered["settings"], dict):
            filtered["settings"] = {
                k: v for k, v in filtered["settings"].items() if k in allowed_settings
            }
        if resolve_workflow_refs(filtered, n8n_by_name):
            wf_id = n8n_by_name[name]
            patch_status, _ = api_request(
                "PUT", f"{base_url}/api/v1/workflows/{wf_id}", api_key, filtered
            )
            if patch_status == 200:
                print(f"  ref {name}: workflow references resolved")
                ref_ok += 1
            else:
                print(f"  ! {name}: failed to resolve workflow references (HTTP {patch_status})")

    print(f"\n{ok}/{len(files)} workflow(s) imported and activated successfully.")


def cmd_export(base_url: str, api_key: str) -> None:
    """Overwrite each repo workflow file with its current definition from n8n."""
    files = sorted(p for p in WORKFLOWS_DIR.glob("*.json") if p.name != ".gitkeep")
    if not files:
        print("No workflow JSON files found in n8n/workflows/")
        return

    n8n_by_name: dict[str, str] = {}
    cursor = None
    while True:
        url = f"{base_url}/api/v1/workflows"
        if cursor:
            url += f"?cursor={cursor}"
        list_status, data = api_request("GET", url, api_key)
        if list_status != 200:
            print(f"ERROR: GET /api/v1/workflows returned HTTP {list_status}: {data}")
            sys.exit(1)
        for wf in data.get("data", []):
            n8n_by_name[wf["name"]] = wf["id"]
        cursor = data.get("nextCursor")
        if not cursor:
            break
    repo_names = set()
    count = 0

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  x {path.name}: could not parse JSON ({exc})")
            continue
        name = payload.get("name", "")
        if not name:
            print(f"  ! {path.name}: missing or empty 'name' field - skipping")
            continue
        repo_names.add(name)

        if name not in n8n_by_name:
            print(f"  ! {path.name}: workflow '{name}' not found in n8n - skipping")
            continue

        wf_id = n8n_by_name[name]
        fetch_status, full = api_request("GET", f"{base_url}/api/v1/workflows/{wf_id}", api_key)
        if fetch_status != 200:
            print(f"  x {path.name}: GET /{wf_id} returned HTTP {fetch_status}")
            continue

        path.write_text(json.dumps(full, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ok {path.name} <- '{name}'")
        count += 1

    extras = [name for name in n8n_by_name if name not in repo_names]
    if extras:
        print("\nWorkflows in n8n with no repo file (not exported):")
        for name in extras:
            print(f"  - {name}")

    print(f"\n{count}/{len(files)} workflow(s) exported to n8n/workflows/")


def main() -> None:
    # Ensure stdout/stderr can emit UTF-8 on Windows consoles that default to cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

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
