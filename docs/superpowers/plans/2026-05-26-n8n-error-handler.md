# n8n Error Handler Sub-Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire all three n8n workflows into a single "BelPro - Napake" error-handler sub-workflow that writes to the existing `error_log` table (Dnevnik napak) on both unexpected node exceptions and explicit logic-error branches.

**Architecture:** A new sub-workflow with two triggers (Error Trigger for automatic n8n exceptions, Execute Workflow Trigger for explicit calls) normalises both input shapes and POSTs to `http://api:8000/api/errors`. The three existing workflows gain an `errorWorkflow` setting pointing to it; `volunteer_entry` also gets a parallel explicit Execute Workflow call from its `IF: Manager Error?` true branch.

**Tech Stack:** n8n (self-hosted), FastAPI `/api/errors` endpoint, n8n-mcp tools for workflow creation/validation, `scripts/n8n_workflows.py` for import/export.

---

## File Map

| Action | File | What changes |
|--------|------|-------------|
| Create | `n8n/workflows/error_handler.json` | New sub-workflow |
| Modify | `n8n/workflows/volunteer_entry.json` | `errorWorkflow` setting + new Code + Execute Workflow nodes |
| Modify | `n8n/workflows/manager_approval.json` | `errorWorkflow` setting |
| Modify | `n8n/workflows/monthly_reports.json` | `errorWorkflow` setting |
| Modify | `scripts/n8n_workflows.py` | `errorWorkflow` in allowed_settings, import ordering, name→ID resolution |
| Modify | `n8n/credentials/README.md` | Document new "BelPro API Internal Key" credential |
| Modify | `n8n/credentials/README_SL.md` | Same in Slovenian |
| Create | `tests/test_n8n_import_script.py` | Unit tests for `resolve_workflow_refs` |

---

## Context for Implementer

**Stack:** Docker Compose on Windows. All n8n workflow JSON files live in `n8n/workflows/`. Import/export is done via `python scripts/n8n_workflows.py import|export`. The script authenticates with n8n's REST API using `N8N_API_KEY` from `.env`.

**Existing credential names in n8n:**
- `BelPro Evolution API` — HTTP Header Auth, header `apikey`
- `BelPro API (Basic Auth)` — HTTP Basic Auth for FastAPI

**Exact workflow names (copy-paste, check dashes vs em-dashes):**
- `BelPro - Vnos Prostovoljcev` (regular hyphen)
- `BelPro — Odobritev Upravljalca` (em dash —)
- `BelPro — Mesečna Poročila` (em dash —)
- `BelPro - Napake` (new, regular hyphen)

**`/api/errors` endpoint:** POST to `http://api:8000/api/errors` with header `X-Internal-Key: <API_SECRET_KEY from .env>`. Body is JSON: `{service, operation, message, detail}`. Returns HTTP 201 on success.

**Error Trigger output shape (Shape A):**
```json
{
  "workflow": { "name": "BelPro - Vnos Prostovoljcev" },
  "execution": {
    "lastNodeExecuted": "HTTP: Lookup Volunteer",
    "error": { "message": "...", "stack": "..." }
  }
}
```

**Execute Workflow Trigger input shape (Shape B — explicit calls):**
```json
{
  "workflow_name": "BelPro - Vnos Prostovoljcev",
  "operation": "manager_lookup",
  "detail": "Ni aktivnega vnosa za odobritev."
}
```

**n8n-mcp rule (from CLAUDE.md):** All workflow creation and validation must use n8n-mcp tools. Use `mcp__n8n-mcp__n8n_generate_workflow` to scaffold and `mcp__n8n-mcp__validate_node` to verify individual node parameter structures before writing to disk.

---

## Task 1: Update Import Script

**Files:**
- Modify: `scripts/n8n_workflows.py`
- Create: `tests/test_n8n_import_script.py`

- [ ] **Step 1: Write failing unit tests**

Create `tests/test_n8n_import_script.py`:

```python
"""Unit tests for n8n_workflows.py — resolve_workflow_refs logic."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "scripts"))
from n8n_workflows import resolve_workflow_refs


def test_resolves_error_workflow_setting():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {"errorWorkflow": "BelPro - Napake"},
        "nodes": [],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["settings"]["errorWorkflow"] == "abc123"


def test_resolves_node_workflow_id():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {},
        "nodes": [{"parameters": {"workflowId": "BelPro - Napake"}}],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["nodes"][0]["parameters"]["workflowId"] == "abc123"


def test_no_change_when_already_id():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {"errorWorkflow": "abc123"},
        "nodes": [],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert not changed
    assert payload["settings"]["errorWorkflow"] == "abc123"


def test_no_change_when_setting_absent():
    payload = {"name": "test", "settings": {}, "nodes": []}
    changed = resolve_workflow_refs(payload, {"BelPro - Napake": "abc123"})
    assert not changed


def test_resolves_both_at_once():
    payload = {
        "name": "test",
        "settings": {"errorWorkflow": "BelPro - Napake"},
        "nodes": [{"parameters": {"workflowId": "BelPro - Napake"}}],
    }
    n8n_by_name = {"BelPro - Napake": "xyz999"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["settings"]["errorWorkflow"] == "xyz999"
    assert payload["nodes"][0]["parameters"]["workflowId"] == "xyz999"
```

- [ ] **Step 2: Run tests to confirm they fail**

```powershell
python -m pytest tests/test_n8n_import_script.py -v
```

Expected: `ImportError` or `AttributeError` — `resolve_workflow_refs` does not exist yet.

- [ ] **Step 3: Add `errorWorkflow` to `allowed_settings`**

In `scripts/n8n_workflows.py`, find the `allowed_settings` set (around line 97) and add `"errorWorkflow"`:

```python
    allowed_settings = {
        "executionOrder",
        "errorWorkflow",
        "saveDataErrorExecution",
        "saveDataSuccessExecution",
        "saveManualExecutions",
        "saveExecutionProgress",
        "timezone",
    }
```

- [ ] **Step 4: Sort `error_handler.json` first in the import order**

Find line 64 (the `files = sorted(...)` line in `cmd_import`) and change it to:

```python
    _all = sorted(p for p in WORKFLOWS_DIR.glob("*.json") if p.name != ".gitkeep")
    files = sorted(_all, key=lambda p: (0 if p.name == "error_handler.json" else 1, p.name))
```

- [ ] **Step 5: Update `n8n_by_name` after each upsert**

In `cmd_import`, find the block that sets `wf_id` after a successful POST (new workflow, around line 142). After `wf_id = resp.get("id")`, add:

```python
            n8n_by_name[name] = wf_id
```

Also add after the PUT (updated workflow, around line 136) — after `wf_id = n8n_by_name[name]` — no change needed there since it was already in the map.

- [ ] **Step 6: Add `resolve_workflow_refs` function**

Add this function after the `api_request` function (before `cmd_import`):

```python
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
```

- [ ] **Step 7: Add resolution pass at the end of `cmd_import`**

Append this block just before the final `print(f"\n{ok}/...")` line:

```python
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
```

- [ ] **Step 8: Run tests to confirm they pass**

```powershell
python -m pytest tests/test_n8n_import_script.py -v
```

Expected: 5/5 PASS.

- [ ] **Step 9: Commit**

```powershell
git add scripts/n8n_workflows.py tests/test_n8n_import_script.py
git commit -m "feat: add errorWorkflow support and name-to-ID resolution to import script"
```

---

## Task 2: Document New Credential

**Files:**
- Modify: `n8n/credentials/README.md`
- Modify: `n8n/credentials/README_SL.md`

- [ ] **Step 1: Add row to `n8n/credentials/README.md`**

In the `## Required credentials` table, add a new row:

```markdown
| `BelPro API Internal Key` | HTTP Header Auth | Error handler workflow (`error_handler.json`) |
```

In the `## Setup` section, add:

```markdown
- **BelPro API Internal Key:** Header name `X-Internal-Key`, value = `API_SECRET_KEY` from `.env`.
```

- [ ] **Step 2: Add row to `n8n/credentials/README_SL.md`**

In the `## Zahtevani prijavni podatki` table, add:

```markdown
| `BelPro API Internal Key` | HTTP Header Auth | Potek dela za napake (`error_handler.json`) |
```

In the `## Nastavitev` section, add:

```markdown
- **BelPro API Internal Key:** Ime glave `X-Internal-Key`, vrednost = `API_SECRET_KEY` iz datoteke `.env`.
```

- [ ] **Step 3: Create the credential in n8n UI (manual step)**

Open n8n at http://localhost:5678 → Settings → Credentials → New Credential → HTTP Header Auth.

- Name: `BelPro API Internal Key`
- Name (header field): `X-Internal-Key`
- Value: paste the value of `API_SECRET_KEY` from `.env`

Save. The credential ID will be auto-assigned; it is referenced by name in the workflow JSON.

- [ ] **Step 4: Commit**

```powershell
git add n8n/credentials/README.md n8n/credentials/README_SL.md
git commit -m "docs: document BelPro API Internal Key n8n credential"
```

---

## Task 3: Create "BelPro - Napake" Sub-Workflow

**Files:**
- Create: `n8n/workflows/error_handler.json`

- [ ] **Step 1: Validate the HTTP Request node parameter structure**

Use n8n-mcp to confirm the correct parameter names for an HTTP Request v4.2 node that POSTs JSON with `genericCredentialType` / `httpHeaderAuth`:

```
mcp__n8n-mcp__validate_node with type="n8n-nodes-base.httpRequest", typeVersion=4.2,
parameters={
  "method": "POST",
  "url": "http://api:8000/api/errors",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "sendBody": true,
  "contentType": "json",
  "body": "={{ JSON.stringify({service: $json.service, operation: $json.operation, message: $json.message, detail: $json.detail || null}) }}"
}
```

If validation returns errors, adjust parameter names to match. The goal: POST JSON body `{service, operation, message, detail}` using the `BelPro API Internal Key` HTTP Header Auth credential.

- [ ] **Step 2: Generate the sub-workflow via n8n-mcp**

Use `mcp__n8n-mcp__n8n_generate_workflow` with this description:

```
Create an n8n workflow named "BelPro - Napake" that handles errors from other workflows.
It has two triggers:
1. Error Trigger (n8n-nodes-base.errorTrigger typeVersion 1) — fires automatically when set as errorWorkflow
2. When Called By Another Workflow (n8n-nodes-base.executeWorkflowTrigger typeVersion 1) — fires on explicit Execute Workflow calls

Both triggers connect to a single Code node named "Code: Normalize Input" (n8n-nodes-base.code typeVersion 2).

The Code node runs this JavaScript:
  const LABEL_MAP = {
    'BelPro - Vnos Prostovoljcev': 'Napaka pri vnosu prostovoljca',
    'BelPro — Odobritev Upravljalca': 'Napaka pri odobritvi vnosa',
    'BelPro — Mesečna Poročila': 'Napaka pri mesečnih poročilih',
  };
  let workflowName, operation, detail;
  if ($json.workflow_name !== undefined) {
    workflowName = $json.workflow_name;
    operation = $json.operation || workflowName;
    detail = String($json.detail || '');
  } else {
    workflowName = ($json.workflow || {}).name || 'neznano';
    operation = ($json.execution || {}).lastNodeExecuted || workflowName;
    const err = ($json.execution || {}).error || {};
    detail = [err.message, err.stack].filter(Boolean).join('\n');
  }
  const message = LABEL_MAP[workflowName] || 'Neznana napaka n8n';
  return [{ json: { service: 'n8n', operation, message, detail } }];

The Code node connects to an HTTP Request node named "HTTP: POST /api/errors" that POSTs JSON to http://api:8000/api/errors using the credential "BelPro API Internal Key" (httpHeaderAuth).

The HTTP node connects to an IF node named "IF: POST Failed?" that checks whether the HTTP response status code is not 201. The true branch (failure) is a no-op (workflow ends). The false branch (success) is also a no-op.

Workflow settings: executionOrder v1, timezone Europe/Ljubljana, saveDataErrorExecution all, saveDataSuccessExecution all, saveManualExecutions true.
```

- [ ] **Step 3: Validate the generated workflow**

Use `mcp__n8n-mcp__n8n_validate_workflow` on the generated JSON. Fix any reported issues.

- [ ] **Step 4: Create the workflow in n8n**

Use `mcp__n8n-mcp__n8n_create_workflow` with the validated JSON. Note the returned workflow ID.

- [ ] **Step 5: Export to disk**

Run the export script to write the workflow to disk:

```powershell
python scripts/n8n_workflows.py export
```

Verify `n8n/workflows/error_handler.json` was created and contains `"name": "BelPro - Napake"`.

- [ ] **Step 6: Replace the live credential ID with the credential name**

Open `n8n/workflows/error_handler.json`. Find the HTTP node's `credentials` block. It will look like:

```json
"credentials": {
  "httpHeaderAuth": {
    "id": "<some-id>",
    "name": "BelPro API Internal Key"
  }
}
```

This is correct — keep it as-is. The name is what matters for portability.

Also check `settings.errorWorkflow` — it should be absent (this workflow IS the error handler, it doesn't call another). If present and set to something unexpected, remove it.

- [ ] **Step 7: Verify the Code node label map uses correct workflow names**

Open `n8n/workflows/error_handler.json` and find the `jsCode` parameter of `Code: Normalize Input`. Confirm the LABEL_MAP keys exactly match:

- `BelPro - Vnos Prostovoljcev` (regular hyphen)
- `BelPro — Odobritev Upravljalca` (em dash U+2014)
- `BelPro — Mesečna Poročila` (em dash U+2014, č, č)

If the generator escaped them differently, edit the jsCode in the JSON directly to use the exact strings above.

- [ ] **Step 8: Commit**

```powershell
git add n8n/workflows/error_handler.json
git commit -m "feat: add BelPro - Napake error handler sub-workflow"
```

---

## Task 4: Wire `errorWorkflow` in Existing Workflow Settings

**Files:**
- Modify: `n8n/workflows/volunteer_entry.json` (settings only, nodes in Task 5)
- Modify: `n8n/workflows/manager_approval.json`
- Modify: `n8n/workflows/monthly_reports.json`

- [ ] **Step 1: Add `errorWorkflow` to `volunteer_entry.json`**

Open `n8n/workflows/volunteer_entry.json`. Find the `"settings"` block and add `"errorWorkflow"`:

```json
"settings": {
  "executionOrder": "v1",
  "timezone": "Europe/Ljubljana",
  "errorWorkflow": "BelPro - Napake",
  "saveDataErrorExecution": "all",
  "saveDataSuccessExecution": "all",
  "saveManualExecutions": true,
  "binaryMode": "separate",
  "timeSavedMode": "fixed",
  "callerPolicy": "workflowsFromSameOwner",
  "availableInMCP": false
}
```

- [ ] **Step 2: Add `errorWorkflow` to `manager_approval.json`**

Open `n8n/workflows/manager_approval.json`. Find `"settings"` and add:

```json
"errorWorkflow": "BelPro — Odobritev Upravljalca"
```

Wait — that's the wrong value. Add:

```json
"errorWorkflow": "BelPro - Napake"
```

Full settings block result:

```json
"settings": {
  "executionOrder": "v1",
  "errorWorkflow": "BelPro - Napake",
  "saveDataErrorExecution": "all",
  "saveDataSuccessExecution": "all",
  "saveManualExecutions": true,
  "saveExecutionProgress": true,
  "binaryMode": "separate"
}
```

- [ ] **Step 3: Add `errorWorkflow` to `monthly_reports.json`**

Full settings block result:

```json
"settings": {
  "executionOrder": "v1",
  "timezone": "Europe/Ljubljana",
  "errorWorkflow": "BelPro - Napake",
  "saveDataErrorExecution": "all",
  "saveDataSuccessExecution": "none",
  "saveManualExecutions": true,
  "binaryMode": "separate"
}
```

- [ ] **Step 4: Import all workflows**

```powershell
python scripts/n8n_workflows.py import
```

Expected output includes lines like:
```
  ok BelPro - Napake: created and activated
  ref BelPro - Vnos Prostovoljcev: workflow references resolved
  ref BelPro — Odobritev Upravljalca: workflow references resolved
  ref BelPro — Mesečna Poročila: workflow references resolved
```

- [ ] **Step 5: Verify in n8n UI**

Open n8n → each of the three workflows → Settings tab. Confirm "Error workflow" shows "BelPro - Napake".

- [ ] **Step 6: Commit**

```powershell
git add n8n/workflows/volunteer_entry.json n8n/workflows/manager_approval.json n8n/workflows/monthly_reports.json
git commit -m "feat: wire errorWorkflow setting to BelPro - Napake in all three workflows"
```

---

## Task 5: Add Explicit Error Path to `volunteer_entry`

**Files:**
- Modify: `n8n/workflows/volunteer_entry.json`

Context: `IF: Manager Error?` is at position `[1040, 832]`. Its true branch (index 0) currently goes only to `HTTP: WA Ni Aktivnega Vnosa (Mgr)` at `[1216, 816]`. We add a Code node and Execute Workflow node below it.

- [ ] **Step 1: Add `Code: Pripravi Napako` node to the `nodes` array**

In `n8n/workflows/volunteer_entry.json`, in the `"nodes"` array, append:

```json
{
  "parameters": {
    "jsCode": "return [{ json: { workflow_name: 'BelPro - Vnos Prostovoljcev', operation: 'manager_lookup', detail: $json.message || 'Ni aktivnega vnosa za odobritev.' } }];"
  },
  "id": "code_pripravi_napako",
  "name": "Code: Pripravi Napako",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [1216, 960]
}
```

- [ ] **Step 2: Add `Execute Workflow: Napake` node to the `nodes` array**

Append to `"nodes"`:

```json
{
  "parameters": {
    "workflowId": "BelPro - Napake",
    "mode": "each",
    "options": {}
  },
  "id": "exec_wf_napake",
  "name": "Execute Workflow: Napake",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1,
  "position": [1456, 960]
}
```

The `workflowId` value `"BelPro - Napake"` is a name placeholder; the import script's resolution pass (Task 1) will replace it with the live n8n ID.

- [ ] **Step 3: Update `connections` to wire from `IF: Manager Error?` true branch**

Find the `"IF: Manager Error?"` key in `"connections"`. It currently reads:

```json
"IF: Manager Error?": {
  "main": [
    [
      {"node": "HTTP: WA Ni Aktivnega Vnosa (Mgr)", "type": "main", "index": 0}
    ],
    [
      {"node": "Execute Workflow: Manager Approval", "type": "main", "index": 0}
    ]
  ]
}
```

Change the true-branch (index 0) inner array to include the new Code node:

```json
"IF: Manager Error?": {
  "main": [
    [
      {"node": "HTTP: WA Ni Aktivnega Vnosa (Mgr)", "type": "main", "index": 0},
      {"node": "Code: Pripravi Napako", "type": "main", "index": 0}
    ],
    [
      {"node": "Execute Workflow: Manager Approval", "type": "main", "index": 0}
    ]
  ]
}
```

- [ ] **Step 4: Add connection from `Code: Pripravi Napako` to `Execute Workflow: Napake`**

In `"connections"`, add:

```json
"Code: Pripravi Napako": {
  "main": [
    [{"node": "Execute Workflow: Napake", "type": "main", "index": 0}]
  ]
}
```

- [ ] **Step 5: Validate the updated workflow**

Use `mcp__n8n-mcp__n8n_validate_workflow` on the modified `volunteer_entry.json` content to catch any structural errors before import.

- [ ] **Step 6: Import and verify**

```powershell
python scripts/n8n_workflows.py import
```

Open n8n → BelPro - Vnos Prostovoljcev. Confirm two new nodes appear below `IF: Manager Error?` on the true branch. Confirm `Execute Workflow: Napake` shows `workflowId` pointing to `BelPro - Napake` (the live ID, not the name string).

- [ ] **Step 7: Export to capture the live workflow ID in the JSON**

```powershell
python scripts/n8n_workflows.py export
```

This overwrites `volunteer_entry.json` with the live n8n version, which now has the real n8n ID in `Execute Workflow: Napake`'s `workflowId` and the resolved `errorWorkflow` ID in settings. Commit this canonical version.

- [ ] **Step 8: Commit**

```powershell
git add n8n/workflows/volunteer_entry.json
git commit -m "feat: add explicit error reporting to volunteer_entry IF: Manager Error? branch"
```

---

## Task 6: End-to-End Tests

No automated tests exist for n8n workflow logic — these are manual acceptance tests. Run with the full stack up (`docker compose up -d`).

- [ ] **Test 1: Automatic error catch in `volunteer_entry`**

Temporarily break the Whisper HTTP node:

1. In n8n UI, open `BelPro - Vnos Prostovoljcev`.
2. Edit `HTTP: Transcribe Audio` → change URL to `http://whisper:9099/asr` (wrong port, guaranteed 502).
3. Send a WhatsApp voice note to the bot.
4. Wait for execution to fail.
5. Open `http://localhost:80` → Dnevnik napak.

Expected: one new entry with `service=n8n`, `message=Napaka pri vnosu prostovoljca`, `detail` containing the 502 error text.

6. Restore the correct Whisper URL. Re-import.

- [ ] **Test 2: Explicit error branch in `volunteer_entry`**

Trigger the manager-lookup error branch:

1. Send a WhatsApp text entry from a registered volunteer.
2. Immediately approve/reject it in the dashboard so no `pending_manager` entry exists.
3. Send another WhatsApp message containing a number (e.g. "1") — this hits the manager-approval sub-flow lookup with nothing to find.
4. Check Dnevnik napak.

Expected: one entry with `service=n8n`, `operation=manager_lookup`, `message=Napaka pri vnosu prostovoljca`, `detail=Ni aktivnega vnosa za odobritev.` AND a WhatsApp message "Ni aktivnega vnosa" sent to the manager.

- [ ] **Test 3: Automatic error catch in `manager_approval`**

1. Temporarily change `HTTP: Approve/Reject Entry` URL to a broken path.
2. Trigger a manager approval via WhatsApp.
3. Check Dnevnik napak.

Expected: entry with `message=Napaka pri odobritvi vnosa`.

4. Restore the URL. Re-import.

- [ ] **Test 4: Automatic error catch in `monthly_reports`**

1. Temporarily break `HTTP: Generate PDF` or similar.
2. Trigger the monthly reports workflow manually in n8n.
3. Check Dnevnik napak.

Expected: entry with `message=Napaka pri mesečnih poročilih`.

4. Restore. Re-import.

- [ ] **Test 5: Import script ID resolution on re-import**

```powershell
python scripts/n8n_workflows.py import
```

Expected: script runs cleanly, `ref` lines appear for workflows with `errorWorkflow` set, no HTTP errors in resolution pass. Verify in n8n UI that errorWorkflow is still correctly wired after re-import.

- [ ] **Final commit (if any files changed during testing)**

```powershell
git add n8n/workflows/
git commit -m "chore: export n8n workflows after error handler end-to-end tests"
```
