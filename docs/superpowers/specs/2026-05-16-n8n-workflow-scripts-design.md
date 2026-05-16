# Design: n8n Workflow Import/Export Script

**Date:** 2026-05-16
**Status:** Approved

---

## Purpose

A single executable Python script that moves n8n workflows in both directions — from the repository into a running n8n instance (install / dev reset) and from a running n8n instance back into the repository (after editing workflows in the UI).

Useful during fresh installs (saves installers from figuring out n8n's UI import flow) and during development (reduces a multi-step manual process to one command).

---

## File Layout

```
scripts/n8n_workflows.py    ← new executable script
n8n/workflows/              ← existing; source for import, destination for export
```

No other files added or changed by this feature.

---

## Interface

```bash
./scripts/n8n_workflows.py import   # load n8n/workflows/*.json → running n8n
./scripts/n8n_workflows.py export   # pull running n8n → n8n/workflows/*.json
./scripts/n8n_workflows.py          # prints usage and exits
```

The script is executable (`chmod +x`) and uses `#!/usr/bin/env python`.

---

## Configuration

Read from `.env` in the project root, located relative to the script so it works regardless of the caller's working directory. No external dependencies — stdlib only (`urllib`, `json`, `pathlib`, `sys`).

Two values consumed:

| Variable | Used for |
|---|---|
| `N8N_API_KEY` | `X-N8N-API-KEY` header on every request |
| `N8N_WEBHOOK_URL` | Base URL for the n8n instance (e.g. `http://localhost:5678`) |

`N8N_WEBHOOK_URL` already exists in `.env` and `.env.example`; no new variables needed.

---

## Import Flow

For each `.json` file in `n8n/workflows/` (`.gitkeep` skipped):

1. Load the JSON; read its `name` field.
2. GET `/api/v1/workflows` — fetch the full workflow list from n8n.
3. Match by `name`:
   - **Found** → PUT `/api/v1/workflows/{id}` with the file payload merged with the existing `id`.
   - **Not found** → POST `/api/v1/workflows` with the file payload.
4. PATCH `/api/v1/workflows/{id}/activate` — activate regardless of create vs update.
5. Print per-workflow result (ok / error).

Final line: `N/N workflows imported successfully.`

---

## Export Flow

1. GET `/api/v1/workflows` — list all workflows.
2. For each workflow, GET `/api/v1/workflows/{id}` — fetch full definition.
3. Derive filename: `workflow["name"]` → lowercase, spaces to underscores, strip characters that are not alphanumeric or underscore → `{name}.json`.
4. Write to `n8n/workflows/{name}.json` (overwrites if present).
5. Print per-workflow result (filename written / error).

Credentials are never exported (not available via this API endpoint anyway).

Final line: `N workflows exported to n8n/workflows/.`

---

## Error Handling

| Condition | Behaviour |
|---|---|
| `N8N_API_KEY` missing or still placeholder (`FILL_IN_AFTER_FIRST_N8N_RUN`) | Print instructions pointing to n8n Settings → API; exit 1 |
| n8n unreachable (connection refused / timeout) | Tell user to check `docker compose up`; exit 1 |
| Unexpected HTTP status on a single workflow | Print workflow name, status code, response body; continue with remaining workflows |

No silent failures. Every outcome is printed.

---

## README / SPEC Updates

- `README.md` — add a "Workflow management" section covering both import and export, where to get the API key, and when to use each command.
- `SPEC.md` — note that the canonical workflow source is `n8n/workflows/` and the script is how they are loaded on install.
- `OPEN_ISSUES.md` — remove the first issue once implemented.

---

## Out of Scope

- Credential import/export (never committed; documented in `n8n/credentials/README.md`)
- Integration with `setup.sh` (intentionally standalone)
- Workflow validation before import (n8n's API rejects invalid payloads with a clear error)
