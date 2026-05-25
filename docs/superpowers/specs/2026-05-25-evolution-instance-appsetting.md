# Evolution Instance Name — AppSettings Migration Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the Evolution API instance name from a hardcoded string in n8n workflow URLs into the AppSettings system, expose it via a no-auth config endpoint, and have n8n fetch it dynamically.

**Architecture:** `evolution_instance_name` becomes an AppSettings property (DB-first, env-fallback, seeded on first boot). A new no-auth `GET /api/config/evolution-instance` endpoint returns it. All n8n HTTP Request nodes that call Evolution API replace the hardcoded `belpro` instance name with a sub-workflow fetch of this endpoint.

**Tech Stack:** Python/FastAPI, SQLAlchemy/Alembic, Pydantic, n8n workflow JSON.

---

## Context

Three n8n workflow files contain hardcoded `belpro` in all Evolution API URLs:

- `n8n/workflows/volunteer_entry.json` — ~20 unique HTTP Request nodes
- `n8n/workflows/manager_approval.json` — ~5 unique HTTP Request nodes
- `n8n/workflows/monthly_reports.json` — 0 Evolution API calls (no change needed)

Evolution API URL pattern used:
- `http://evolution-api:8080/message/sendText/belpro`
- `http://evolution-api:8080/chat/getBase64FromMediaMessage/belpro`

The instance name `belpro` must become dynamic. The correct source of truth is AppSettings — the same DB-first, env-fallback system used for `max_photos_per_entry`, `photo_retention_days`, `report_auto_hour`, and `session_duration_hours`.

Precedent for the n8n endpoint pattern: `GET /api/log-entries/photo-limit` (no auth, returns a single AppSettings value, used by n8n workflows).

---

## Files

| Action | File |
|--------|------|
| Modify | `api/services/app_settings.py` |
| Modify | `api/schemas/admin.py` |
| Modify | `api/routers/admin.py` |
| Create | `api/routers/config.py` |
| Modify | `api/main.py` |
| Create | `db/versions/<timestamp>_add_evolution_instance_name_setting.py` |
| Modify | `api/tests/test_app_settings.py` |
| Create | `api/tests/test_config.py` |
| Modify | `n8n/workflows/volunteer_entry.json` |
| Modify | `n8n/workflows/manager_approval.json` |

---

## Design

### AppSettings extension

Add `evolution_instance_name` property to `AppSettings` in `api/services/app_settings.py`:

```python
@property
def evolution_instance_name(self) -> str:
    """Evolution API WhatsApp instance name. DB-first, env-fallback."""
    return self._str("evolution_instance_name", self._env.evolution_instance_name)
```

The env fallback reads from `Settings.evolution_instance_name` which already reads `EVOLUTION_INSTANCE_NAME` from `.env` (default `"belpro"`).

### Schema

Add field to `AdminSettingsResponse` in `api/schemas/admin.py`:

```python
evolution_instance_name: str
```

### Admin router

Include `evolution_instance_name` in both `GET /api/admin/settings` and `PATCH /api/admin/settings` responses. No PATCH support for this field — it is read-only from the admin settings endpoint (runtime changes go via the DB directly or future UI).

### New config router

New file `api/routers/config.py` — no auth required, single endpoint:

```python
GET /api/config/evolution-instance
→ {"instance_name": "<value>"}
```

This follows the same no-auth pattern as `GET /api/log-entries/photo-limit`.

### Alembic migration

Seed the `app_settings` table with the new key on migration:

```python
op.execute(
    "INSERT INTO app_settings (name, value) "
    "VALUES ('evolution_instance_name', 'belpro') "
    "ON CONFLICT (name) DO NOTHING"
)
```

The hardcoded `'belpro'` seed is the safe default. Deployments with a different instance name set `EVOLUTION_INSTANCE_NAME` in `.env` — the env-fallback in AppSettings picks it up if no DB row exists, and the DB row can be updated at runtime without restart.

### n8n workflow changes

Each HTTP Request node that calls Evolution API currently has a plain string URL. It must become an n8n expression that injects the fetched instance name.

**Fetch pattern** — add a single `GET /api/config/evolution-instance` HTTP Request node immediately after the webhook trigger in each workflow (before any branching), store the result, then reference `{{ $('Fetch Config').first().json.instance_name }}` in all Evolution API URL expressions. Node name must be exactly `Fetch Config` so the reference is consistent across all nodes in the workflow.

URL transformation example:
```
Before: "http://evolution-api:8080/message/sendText/belpro"
After:  "={{ 'http://evolution-api:8080/message/sendText/' + $('Fetch Config').first().json.instance_name }}"
```

Both `volunteer_entry.json` and `manager_approval.json` need this change. `monthly_reports.json` has no Evolution API calls — no change.

**Important:** n8n workflow JSON edits must be followed by running `python scripts/n8n_workflows.py import` to push changes into the running n8n instance.

### Tests

**`api/tests/test_app_settings.py`** — add:
- `test_appsettings_evolution_instance_name_default()` — returns `"belpro"` when no DB row
- `test_appsettings_evolution_instance_name_from_db()` — returns DB value when row exists

**`api/tests/test_config.py`** — new file:
- `test_get_evolution_instance_requires_no_auth()` — endpoint is public
- `test_get_evolution_instance_returns_default()` — returns `"belpro"` from seeded default

---

## Out of Scope

- Making `evolution_instance_name` editable via the admin dashboard UI (OPEN_ISSUES: ISS-NNN — n8n variable passing system rework)
- Parameterising `evolution-api:8080` base URL (YAGNI — Docker service name is stable)
- Changing `monthly_reports.json` (no Evolution API calls)
