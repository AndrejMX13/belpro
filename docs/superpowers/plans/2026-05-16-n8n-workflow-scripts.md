# n8n Workflow Import/Export Script Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `scripts/n8n_workflows.py` — a single executable script that imports workflows from `n8n/workflows/` into a running n8n instance and exports them back, plus update README/SPEC/OPEN_ISSUES.

**Architecture:** Stdlib-only Python script (no pip installs). Reads `N8N_API_KEY` and `N8N_WEBHOOK_URL` from `.env` in the project root. All HTTP via `urllib.request`. Three logical functions: `cmd_import()`, `cmd_export()`, and shared helpers `load_env()`, `make_filename()`, `api_request()`.

**Tech Stack:** Python 3 stdlib (`urllib`, `json`, `pathlib`, `re`, `sys`). n8n REST API v1 (`/api/v1/`). Bash for chmod and manual verification.

---

## File Map

| Action | Path |
|--------|------|
| Create | `scripts/n8n_workflows.py` |
| Modify | `README.md` |
| Modify | `SPEC.md` |
| Modify | `OPEN_ISSUES.md` |

---

### Task 1: Script skeleton — helpers, validation, dispatch

**Files:**
- Create: `scripts/n8n_workflows.py`

- [ ] **Step 1: Create the script with skeleton**

Create `scripts/n8n_workflows.py` with the following content:

```python
#!/usr/bin/env python
"""n8n workflow import/export tool for BelPro.

Usage:
  ./scripts/n8n_workflows.py import   # n8n/workflows/*.json → running n8n
  ./scripts/n8n_workflows.py export   # running n8n → n8n/workflows/*.json
"""

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

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
            env[key.strip()] = value.strip()
    return env


def make_filename(name: str) -> str:
    """Derive a safe filename slug from a workflow name.

    'Volunteer Entry' -> 'volunteer_entry'
    'Manager Approval' -> 'manager_approval'
    """
    slug = name.lower().replace(" ", "_")
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    return slug


def api_request(method: str, url: str, api_key: str, payload: dict | None = None):
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
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {}
        return e.code, body
    except urllib.error.URLError:
        print("ERROR: Cannot reach n8n. Is 'docker compose up' running?")
        sys.exit(1)


def cmd_import(base_url: str, api_key: str) -> None:
    pass  # implemented in Task 3


def cmd_export(base_url: str, api_key: str) -> None:
    pass  # implemented in Task 2


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("import", "export"):
        print(__doc__)
        sys.exit(0)

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
```

- [ ] **Step 2: Make the script executable**

```bash
chmod +x scripts/n8n_workflows.py
```

- [ ] **Step 3: Verify `make_filename()` inline**

```bash
python scripts/n8n_workflows.py
```

Expected: prints usage text and exits 0. Then verify the helper logic manually:

```bash
python -c "
import sys; sys.path.insert(0, 'scripts')
from n8n_workflows import make_filename
assert make_filename('Volunteer Entry') == 'volunteer_entry'
assert make_filename('Manager Approval') == 'manager_approval'
assert make_filename('Monthly Reports') == 'monthly_reports'
assert make_filename('Foo & Bar!') == 'foo__bar'
print('make_filename OK')
"
```

Expected output: `make_filename OK`

- [ ] **Step 4: Verify API key guard**

Temporarily set a bad key and confirm the script exits with the right message:

```bash
N8N_API_KEY=FILL_IN_AFTER_FIRST_N8N_RUN python -c "
import pathlib, sys
# patch ENV_FILE to a tmp file with the placeholder
import tempfile, os
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False)
tmp.write('N8N_API_KEY=FILL_IN_AFTER_FIRST_N8N_RUN\nN8N_WEBHOOK_URL=http://localhost:5678/\n')
tmp.close()
sys.argv = ['n8n_workflows.py', 'import']
import n8n_workflows
n8n_workflows.ENV_FILE = pathlib.Path(tmp.name)
n8n_workflows.main()
" 2>&1 || true
```

Expected: prints `ERROR: N8N_API_KEY is not set in .env` and exits 1.

- [ ] **Step 5: Commit**

```bash
git add scripts/n8n_workflows.py
git commit -m "feat: add n8n_workflows.py skeleton with helpers and dispatch"
```

---

### Task 2: Export command

**Files:**
- Modify: `scripts/n8n_workflows.py` — replace `cmd_export` stub

- [ ] **Step 1: Implement `cmd_export()`**

Replace the `cmd_export` stub with:

```python
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
            print(f"  ✗ {name}: GET /{wf_id} returned HTTP {status}")
            continue
        filename = make_filename(name) + ".json"
        out_path = WORKFLOWS_DIR / filename
        out_path.write_text(json.dumps(full, indent=2, ensure_ascii=False))
        print(f"  ✓ {name} → {filename}")
        count += 1

    print(f"\n{count} workflow(s) exported to n8n/workflows/")
```

- [ ] **Step 2: Run export against the live n8n instance**

```bash
./scripts/n8n_workflows.py export
```

Expected output (one line per workflow):
```
  ✓ Volunteer Entry → volunteer_entry.json
  ✓ Manager Approval → manager_approval.json
  ✓ Monthly Reports → monthly_reports.json

3 workflow(s) exported to n8n/workflows/
```

Verify files were written (or overwritten) in `n8n/workflows/`:

```bash
ls -la n8n/workflows/*.json
```

- [ ] **Step 3: Commit**

```bash
git add scripts/n8n_workflows.py
git commit -m "feat: implement export command in n8n_workflows.py"
```

---

### Task 3: Import command

**Files:**
- Modify: `scripts/n8n_workflows.py` — replace `cmd_import` stub

- [ ] **Step 1: Implement `cmd_import()`**

Replace the `cmd_import` stub with:

```python
def cmd_import(base_url: str, api_key: str) -> None:
    """Load all *.json workflows from n8n/workflows/ into n8n (upsert + activate)."""
    files = sorted(p for p in WORKFLOWS_DIR.glob("*.json") if p.name != ".gitkeep")
    if not files:
        print("No workflow JSON files found in n8n/workflows/")
        return

    # Fetch existing workflows to match by name
    status, data = api_request("GET", f"{base_url}/api/v1/workflows", api_key)
    if status != 200:
        print(f"ERROR: GET /api/v1/workflows returned HTTP {status}: {data}")
        sys.exit(1)
    existing = {wf["name"]: wf["id"] for wf in data.get("data", [])}

    ok = 0
    for path in files:
        payload = json.loads(path.read_text())
        name = payload.get("name", path.stem)

        if name in existing:
            wf_id = existing[name]
            payload["id"] = wf_id
            status, resp = api_request(
                "PUT", f"{base_url}/api/v1/workflows/{wf_id}", api_key, payload
            )
            action = "updated"
        else:
            status, resp = api_request(
                "POST", f"{base_url}/api/v1/workflows", api_key, payload
            )
            wf_id = resp.get("id")
            action = "created"

        if status not in (200, 201):
            print(f"  ✗ {name}: HTTP {status} — {resp}")
            continue

        # Activate
        act_status, _ = api_request(
            "POST", f"{base_url}/api/v1/workflows/{wf_id}/activate", api_key
        )
        if act_status not in (200, 201):
            print(f"  ! {name}: {action} but activation failed (HTTP {act_status})")
        else:
            print(f"  ✓ {name}: {action} and activated")
        ok += 1

    print(f"\n{ok}/{len(files)} workflow(s) imported successfully.")
```

- [ ] **Step 2: Run import against the live n8n instance**

```bash
./scripts/n8n_workflows.py import
```

Expected output:
```
  ✓ Volunteer Entry: updated and activated
  ✓ Manager Approval: updated and activated
  ✓ Monthly Reports: updated and activated

3/3 workflow(s) imported successfully.
```

- [ ] **Step 3: Verify in n8n**

Open `http://localhost:5678` → Workflows. Confirm all three workflows are present and active (green toggle).

- [ ] **Step 4: Test the fresh-install path**

To simulate a clean install, temporarily deactivate and delete one workflow via the n8n UI (or API), then re-run import and confirm it's recreated and activated.

- [ ] **Step 5: Commit**

```bash
git add scripts/n8n_workflows.py
git commit -m "feat: implement import command in n8n_workflows.py"
```

---

### Task 4: README, SPEC, and OPEN_ISSUES updates

**Files:**
- Modify: `README.md`
- Modify: `SPEC.md`
- Modify: `OPEN_ISSUES.md`

- [ ] **Step 1: Add a "Workflow management" section to README.md**

Find the existing n8n-related section in `README.md` and add below it (or create a new subsection):

```markdown
### Workflow management

The three n8n workflows (`volunteer_entry`, `manager_approval`, `monthly_reports`) are stored as JSON in `n8n/workflows/` and managed with `scripts/n8n_workflows.py`.

**Prerequisites:** Generate an API key in n8n UI → Settings → API and add it to `.env`:
```
N8N_API_KEY=<your-key>
```

**Load workflows into n8n (fresh install or after pulling updates):**
```bash
./scripts/n8n_workflows.py import
```

**Export workflows from n8n to the repository (after editing in the n8n UI):**
```bash
./scripts/n8n_workflows.py export
git add n8n/workflows/
git commit -m "chore: update n8n workflow exports"
```
```

- [ ] **Step 2: Update SPEC.md**

Find the section in `SPEC.md` that describes n8n workflows and add a note:

```
The canonical source of truth for workflow definitions is `n8n/workflows/`.
On a fresh install, load them with `./scripts/n8n_workflows.py import`.
After editing a workflow in the n8n UI, export with `./scripts/n8n_workflows.py export` and commit the result.
```

- [ ] **Step 3: Remove the first item from OPEN_ISSUES.md**

The first bullet under "Planned Features / Enhancements" reads:
> Check for possibility of a script to load n8n workflows into n8n server...

Remove it. The remaining content stays.

- [ ] **Step 4: Commit all doc changes**

```bash
git add README.md SPEC.md OPEN_ISSUES.md
git commit -m "docs: document n8n workflow import/export script in README and SPEC"
```
