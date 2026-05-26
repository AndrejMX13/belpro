# n8n Error Handler Sub-Workflow Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add consistent operational error reporting to all three n8n workflows by routing both unexpected node exceptions and explicit logic errors into the existing `error_log` table (Dnevnik napak) via a single shared sub-workflow.

**Background:** The `/api/errors` endpoint and `error_log` table already exist. The manager dashboard already displays and acknowledges these entries. Nothing new is needed on the API side.

**Future extensions:** This design intentionally leaves room for WhatsApp manager notifications and AppSettings-based filtering (e.g. suppress certain error types). Both would be added inside the sub-workflow between normalization and the HTTP POST — no changes to callers needed. A note should be added to `SPEC.md` linking to this document once implemented, and an open issue should be created for the AppSettings-based notification settings UI.

---

## Architecture

One new n8n workflow — **"BelPro - Napake"** (`n8n/workflows/error_handler.json`) — acts as the single error destination. All three existing workflows connect to it via two mechanisms:

1. **`errorWorkflow` setting** — n8n fires this automatically when any node throws an unhandled exception. Provides workflow name, failing node name, error message, and stack trace via injected n8n variables.
2. **Execute Workflow node** — called explicitly from logical error branches (controlled flows that are not exceptions). Caller passes a normalized JSON payload.

No changes to the FastAPI backend are required.

---

## Sub-Workflow: BelPro - Napake

File: `n8n/workflows/error_handler.json`

### Node sequence

**1. Error Trigger** (`n8n-nodes-base.errorTrigger`)
- n8n's built-in trigger; fires when called as `errorWorkflow`
- Injects: `$workflow.name`, `$node.name`, `$execution.error.message`, `$execution.error.stack`
- Also serves as the entry point when called via Execute Workflow (n8n routes both through the same trigger)

**2. Code: Normalize Input** (`n8n-nodes-base.code`)
- Detects input shape and normalizes to one internal object
- **Shape A** (from Error Trigger / errorWorkflow): reads n8n injected variables
- **Shape B** (from Execute Workflow): reads `$json.workflow_name`, `$json.operation`, `$json.detail`
- Selects Slovenian `message` label by `workflow_name`:

| workflow_name | message |
|---|---|
| `BelPro - Vnos Prostovoljcev` | `Napaka pri vnosu prostovoljca` |
| `BelPro - Odobritev Upravljalca` | `Napaka pri odobritvi vnosa` |
| `BelPro - Mesečna Poročila` | `Napaka pri mesečnih poročilih` |
| *(unknown)* | `Neznana napaka n8n` |

- Output object:
  ```json
  {
    "service": "n8n",
    "operation": "<workflow_name or caller-supplied operation>",
    "message": "<Slovenian label>",
    "detail": "<raw error text — any language>"
  }
  ```

**3. HTTP: POST /api/errors** (`n8n-nodes-base.httpRequest`)
- URL: `http://api:8000/api/errors`
- Method: POST
- Header: `X-Internal-Key: {{ $credential.apiSecretKey }}` (n8n Header Auth credential, same pattern as other HTTP nodes in the project)
- Body: normalized object from step 2

**4. IF: POST Failed?** (`n8n-nodes-base.if`)
- Checks HTTP response status code
- **True branch** (failure): no-op — the error is visible in n8n execution history, which is the fallback when the error log itself is unreachable
- **False branch** (success): workflow ends cleanly

### Future extension point
WhatsApp notification and AppSettings-based filtering insert between nodes 2 and 3. Callers need no changes.

---

## Wiring Existing Workflows

### All three workflows
Add to `settings`:
```json
"errorWorkflow": "BelPro - Napake"
```
Stored as the workflow **name** in repo JSON. The import script resolves this to the live n8n ID at import time (see Import Script Changes below).

Affected files:
- `n8n/workflows/volunteer_entry.json`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/monthly_reports.json`

### volunteer_entry.json — explicit error branch
The existing `IF: Manager Error?` true branch currently routes only to "HTTP: WA Ni Aktivnega Vnosa (Mgr)". A parallel **Execute Workflow: Napake** node is added to the same branch, firing alongside the WhatsApp message.

Payload passed to the sub-workflow:
```json
{
  "workflow_name": "BelPro - Vnos Prostovoljcev",
  "operation": "manager_lookup",
  "detail": "{{ $json.error_detail }}"
}
```

The WhatsApp node is kept — it is user-facing and intentional. The Execute Workflow node is additional, for the error log.

---

## Import Script Changes (`scripts/n8n_workflows.py`)

### 1. Add `errorWorkflow` to `allowed_settings`
The current filter (line 97–104) strips `errorWorkflow` before sending to n8n. Add it to the set:
```python
allowed_settings = {
    "executionOrder",
    "errorWorkflow",          # <-- add this
    "saveDataErrorExecution",
    ...
}
```

### 2. Import order
"BelPro - Napake" must be imported before the three caller workflows so its n8n ID exists when we need to reference it. Sort the file list so `error_handler.json` comes first.

### 3. Name → ID resolution
Repo JSON files store `settings.errorWorkflow` as a workflow **name** string (e.g. `"BelPro - Napake"`). During import, after all workflows have been upserted, do a resolution pass:

- Build `n8n_by_name` (already built in `cmd_import`)
- For each workflow whose `settings.errorWorkflow` is a string that matches a known workflow name, PATCH `settings.errorWorkflow` with the resolved n8n ID via `PUT /api/v1/workflows/{id}`

This ensures fresh installs wire the error handler correctly regardless of what IDs n8n assigns.

### Export
No changes needed. n8n writes the live ID into `errorWorkflow` on export, which is correct for reading back into a running instance. The name→ID substitution is import-only.

---

## Testing

1. Trigger a deliberate node failure in volunteer_entry (e.g. temporarily point the Whisper HTTP node at a bad URL) → confirm an entry appears in Dnevnik napak with Slovenian message and English/raw detail.
2. Trigger the `IF: Manager Error?` true branch (send a WhatsApp message that produces a manager lookup error) → confirm both the WhatsApp message and the Dnevnik napak entry appear.
3. Confirm manager_approval and monthly_reports also produce entries on forced failure.
4. Run `python scripts/n8n_workflows.py import` on a fresh n8n instance → confirm `errorWorkflow` is wired correctly on all three workflows.
