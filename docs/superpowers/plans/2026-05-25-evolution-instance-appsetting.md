# Evolution Instance Name — AppSettings Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the hardcoded Evolution API instance name `belpro` from n8n workflow URLs into AppSettings (DB-first, env-fallback), expose it via a no-auth config endpoint, make it editable in the admin UI, and have n8n fetch it dynamically at workflow execution time.

**Architecture:** Add `evolution_instance_name` as a new AppSettings property seeded by Alembic migration. Expose via `GET /api/config/evolution-instance` (no auth, mirrors `/photo-limit` pattern). Extend `GET/PATCH /api/admin/settings` and the admin UI. Replace hardcoded `belpro` in n8n workflow JSON with an expression that fetches from the config endpoint.

**Tech Stack:** Python/FastAPI, SQLAlchemy/Alembic, Pydantic, vanilla JS, n8n workflow JSON.

---

## Codebase Orientation

Before starting, read these files to understand the patterns you must follow:

- `api/services/app_settings.py` — AppSettings class with `_str()`, `_int()` helpers and DB-tunable properties
- `api/schemas/admin.py` — `AdminSettingsResponse` and `AdminSettingsUpdate` Pydantic models
- `api/routers/admin.py` — GET/PATCH `/api/admin/settings` routes
- `api/routers/log_entries.py:140-145` — the no-auth `/photo-limit` endpoint pattern to replicate
- `api/main.py:21-79` — router registration pattern
- `api/tests/test_app_settings.py` — AppSettings unit test patterns (no DB, pure unit)
- `api/tests/test_admin.py` — admin endpoint integration test patterns (uses `auth_client` fixture)
- `frontend/js/admin.js` — full settings UI: HTML template, load from API, save handler, validation
- `api/db/migrations/versions/014_seed_report_auto_hour.py` — migration seeding pattern
- `n8n/workflows/manager_approval.json` — n8n workflow JSON structure (nodes + connections)
- `n8n/workflows/volunteer_entry.json` — the larger workflow (same pattern)

Key facts:
- Settings DB table is named `settings` with columns `name`, `type`, `value`
- `AppSetting` model attribute is `value_type` but the DB column is `type`
- All tests run inside the API container: `docker compose exec api pytest tests/ -v`
- After n8n JSON edits: run `python scripts/n8n_workflows.py import` to push to running n8n

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `api/db/migrations/versions/015_seed_evolution_instance_name.py` | Seed default DB row |
| Modify | `api/services/app_settings.py` | New `evolution_instance_name` property |
| Modify | `api/schemas/admin.py` | Add field to response + update schemas |
| Modify | `api/routers/admin.py` | Include field in GET/PATCH responses |
| Create | `api/routers/config.py` | No-auth config endpoint for n8n |
| Modify | `api/main.py` | Register config router |
| Modify | `api/tests/test_app_settings.py` | Unit tests for new property + migration smoke |
| Create | `api/tests/test_config.py` | Integration tests for config endpoint |
| Modify | `api/tests/test_admin.py` | Integration tests for GET/PATCH with new field |
| Modify | `frontend/js/admin.js` | Input field + load/save wiring |
| Modify | `n8n/workflows/manager_approval.json` | Fetch Config node + URL expressions |
| Modify | `n8n/workflows/volunteer_entry.json` | Fetch Config node + URL expressions |

---

## Task 1: Alembic migration — seed `evolution_instance_name`

**Files:**
- Create: `api/db/migrations/versions/015_seed_evolution_instance_name.py`
- Modify: `api/tests/test_app_settings.py`

- [ ] **Step 1: Write the failing smoke test**

Add to `api/tests/test_app_settings.py` after the existing `test_settings_table_seeded` test:

```python
async def test_settings_table_seeded_evolution_instance_name(db_session: AsyncSession) -> None:
    """Migration 015 seeds the evolution_instance_name row."""
    from models.app_setting import AppSetting

    rows = (await db_session.execute(select(AppSetting))).scalars().all()
    by_name = {r.name: r for r in rows}
    assert "evolution_instance_name" in by_name
    assert by_name["evolution_instance_name"].value == "belpro"
    assert by_name["evolution_instance_name"].value_type == "str"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
docker compose exec api pytest tests/test_app_settings.py::test_settings_table_seeded_evolution_instance_name -v
```

Expected: FAIL — `evolution_instance_name` not in seeded rows yet.

- [ ] **Step 3: Create the migration file**

```python
# api/db/migrations/versions/015_seed_evolution_instance_name.py
"""Seed evolution_instance_name setting row.

Revision ID: 015
Revises: 014
Create Date: 2026-05-25
"""
from __future__ import annotations
from typing import Sequence, Union
from alembic import op

revision: str = "015"
down_revision: Union[str, None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the evolution_instance_name settings row with default value belpro."""
    op.execute(
        "INSERT INTO settings (name, type, value) "
        "VALUES ('evolution_instance_name', 'str', 'belpro') "
        "ON CONFLICT (name) DO NOTHING"
    )


def downgrade() -> None:
    """Remove the evolution_instance_name settings row."""
    op.execute("DELETE FROM settings WHERE name = 'evolution_instance_name'")
```

- [ ] **Step 4: Apply the migration**

```bash
docker compose exec api alembic upgrade head
```

Expected: `Running upgrade 014 -> 015, Seed evolution_instance_name setting row.`

- [ ] **Step 5: Run the test to verify it passes**

```bash
docker compose exec api pytest tests/test_app_settings.py::test_settings_table_seeded_evolution_instance_name -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/db/migrations/versions/015_seed_evolution_instance_name.py api/tests/test_app_settings.py
git commit -m "feat: migration 015 — seed evolution_instance_name setting"
```

---

## Task 2: AppSettings property

**Files:**
- Modify: `api/services/app_settings.py`
- Modify: `api/tests/test_app_settings.py`

- [ ] **Step 1: Write the failing unit tests**

Add to `api/tests/test_app_settings.py` after `test_appsettings_falls_back_to_env_when_row_missing`:

```python
def test_appsettings_evolution_instance_name_default() -> None:
    """Returns env default when no DB row exists."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {})
    assert settings.evolution_instance_name == env.evolution_instance_name


def test_appsettings_evolution_instance_name_from_db() -> None:
    """Returns DB value when row exists, overriding env default."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {"evolution_instance_name": "myinstance"})
    assert settings.evolution_instance_name == "myinstance"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
docker compose exec api pytest tests/test_app_settings.py::test_appsettings_evolution_instance_name_default tests/test_app_settings.py::test_appsettings_evolution_instance_name_from_db -v
```

Expected: FAIL — `AppSettings` has no `evolution_instance_name` property yet (falls through to `__getattr__` which returns `env.evolution_instance_name`; the second test fails because `"myinstance"` is not returned).

- [ ] **Step 3: Add the property to AppSettings**

In `api/services/app_settings.py`, add after the `backup_retention_days` property (before the `__getattr__` passthrough):

```python
    @property
    def evolution_instance_name(self) -> str:
        """Evolution API WhatsApp instance name. DB-first, env-fallback."""
        return self._str("evolution_instance_name", self._env.evolution_instance_name) or self._env.evolution_instance_name
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
docker compose exec api pytest tests/test_app_settings.py::test_appsettings_evolution_instance_name_default tests/test_app_settings.py::test_appsettings_evolution_instance_name_from_db -v
```

Expected: PASS.

- [ ] **Step 5: Run the full test suite to check for regressions**

```bash
docker compose exec api pytest tests/test_app_settings.py -v
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add api/services/app_settings.py api/tests/test_app_settings.py
git commit -m "feat: add evolution_instance_name AppSettings property"
```

---

## Task 3: Pydantic schemas

**Files:**
- Modify: `api/schemas/admin.py`

- [ ] **Step 1: Add `evolution_instance_name` to both schema classes**

In `api/schemas/admin.py`:

```python
"""Pydantic schemas for the admin settings endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AdminSettingsResponse(BaseModel):
    """Current values of all runtime-tunable settings."""

    max_photos_per_entry: int
    photo_retention_days: int
    session_duration_hours: int
    report_auto_day: int
    report_auto_period: str
    report_auto_hour: int
    backup_hour: int
    photo_cleanup_hour: int
    backup_retention_days: int
    evolution_instance_name: str


class AdminSettingsUpdate(BaseModel):
    """Partial update for runtime-tunable settings. Only provided fields are written."""

    max_photos_per_entry: int | None = Field(None, ge=1)
    photo_retention_days: int | None = Field(None, ge=1)
    session_duration_hours: int | None = Field(None, ge=1)
    report_auto_day: int | None = Field(None, ge=1, le=28)
    report_auto_period: str | None = Field(None, pattern="^(current|previous)$")
    report_auto_hour: int | None = Field(None, ge=0, le=23)
    backup_hour: int | None = Field(None, ge=0, le=23)
    photo_cleanup_hour: int | None = Field(None, ge=0, le=23)
    backup_retention_days: int | None = Field(None, ge=1)
    evolution_instance_name: str | None = Field(None, min_length=1)
```

- [ ] **Step 2: Verify no import errors**

```bash
docker compose exec api python -c "from schemas.admin import AdminSettingsResponse, AdminSettingsUpdate; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add api/schemas/admin.py
git commit -m "feat: add evolution_instance_name to admin settings schemas"
```

---

## Task 4: Admin router — GET/PATCH + tests

**Files:**
- Modify: `api/routers/admin.py`
- Modify: `api/tests/test_admin.py`

- [ ] **Step 1: Write the failing integration tests**

Open `api/tests/test_admin.py`, check the fixture name used for an authenticated client (look at the existing test function signatures — it may be `auth_client`, `manager_client`, or similar). Use whatever fixture the existing admin tests use. Add these three tests:

```python
async def test_get_admin_settings_includes_evolution_instance_name(
    auth_client: AsyncClient,
) -> None:
    """GET /api/admin/settings includes evolution_instance_name field."""
    r = await auth_client.get("/api/admin/settings")
    assert r.status_code == 200
    data = r.json()
    assert "evolution_instance_name" in data
    assert isinstance(data["evolution_instance_name"], str)
    assert len(data["evolution_instance_name"]) > 0


async def test_patch_admin_settings_updates_evolution_instance_name(
    auth_client: AsyncClient,
) -> None:
    """PATCH /api/admin/settings persists a new evolution_instance_name value."""
    r = await auth_client.patch(
        "/api/admin/settings",
        json={"evolution_instance_name": "testinstance"},
    )
    assert r.status_code == 200
    assert r.json()["evolution_instance_name"] == "testinstance"


async def test_patch_admin_settings_evolution_instance_name_rejects_empty(
    auth_client: AsyncClient,
) -> None:
    """PATCH /api/admin/settings rejects empty evolution_instance_name."""
    r = await auth_client.patch(
        "/api/admin/settings",
        json={"evolution_instance_name": ""},
    )
    assert r.status_code == 422
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
docker compose exec api pytest tests/test_admin.py::test_get_admin_settings_includes_evolution_instance_name tests/test_admin.py::test_patch_admin_settings_updates_evolution_instance_name tests/test_admin.py::test_patch_admin_settings_evolution_instance_name_rejects_empty -v
```

Expected: first test FAIL (field missing from response), others may also fail.

- [ ] **Step 3: Update admin router GET response**

In `api/routers/admin.py`, in the `get_admin_settings` function, add `evolution_instance_name=s.evolution_instance_name` to the `AdminSettingsResponse(...)` constructor:

```python
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
        report_auto_hour=s.report_auto_hour,
        backup_hour=s.backup_hour,
        photo_cleanup_hour=s.photo_cleanup_hour,
        backup_retention_days=s.backup_retention_days,
        evolution_instance_name=s.evolution_instance_name,
    )
```

- [ ] **Step 4: Update admin router PATCH response**

In `api/routers/admin.py`, in the `update_admin_settings` function, add the same field to the second `AdminSettingsResponse(...)` constructor:

```python
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
        report_auto_hour=s.report_auto_hour,
        backup_hour=s.backup_hour,
        photo_cleanup_hour=s.photo_cleanup_hour,
        backup_retention_days=s.backup_retention_days,
        evolution_instance_name=s.evolution_instance_name,
    )
```

- [ ] **Step 5: Run the three new tests**

```bash
docker compose exec api pytest tests/test_admin.py::test_get_admin_settings_includes_evolution_instance_name tests/test_admin.py::test_patch_admin_settings_updates_evolution_instance_name tests/test_admin.py::test_patch_admin_settings_evolution_instance_name_rejects_empty -v
```

Expected: all PASS.

- [ ] **Step 6: Run full admin test suite for regressions**

```bash
docker compose exec api pytest tests/test_admin.py -v
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add api/routers/admin.py api/tests/test_admin.py
git commit -m "feat: expose evolution_instance_name in admin settings GET/PATCH"
```

---

## Task 5: Config router — no-auth endpoint for n8n

**Files:**
- Create: `api/routers/config.py`
- Modify: `api/main.py`
- Create: `api/tests/test_config.py`

- [ ] **Step 1: Write the failing integration tests**

Create `api/tests/test_config.py`:

```python
"""Tests for the public config endpoint consumed by n8n workflows."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


async def test_get_evolution_instance_no_auth_required(client: AsyncClient) -> None:
    """GET /api/config/evolution-instance is publicly accessible."""
    r = await client.get("/api/config/evolution-instance")
    assert r.status_code == 200


async def test_get_evolution_instance_returns_instance_name(client: AsyncClient) -> None:
    """Response contains a non-empty instance_name string."""
    r = await client.get("/api/config/evolution-instance")
    data = r.json()
    assert "instance_name" in data
    assert isinstance(data["instance_name"], str)
    assert len(data["instance_name"]) > 0


async def test_get_evolution_instance_reflects_db_value(
    client: AsyncClient,
    auth_client: AsyncClient,
) -> None:
    """Config endpoint reflects value updated via PATCH /api/admin/settings."""
    await auth_client.patch(
        "/api/admin/settings",
        json={"evolution_instance_name": "reflected"},
    )
    r = await client.get("/api/config/evolution-instance")
    assert r.json()["instance_name"] == "reflected"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
docker compose exec api pytest tests/test_config.py -v
```

Expected: FAIL — 404 (route does not exist yet).

- [ ] **Step 3: Create the config router**

Create `api/routers/config.py`:

```python
"""Config router — public read-only settings for n8n workflow consumption."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from services.app_settings import AppSettings, get_app_settings

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/evolution-instance")
async def get_evolution_instance(
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> dict:
    """Return the Evolution API instance name. No auth required. Used by n8n workflows."""
    return {"instance_name": settings.evolution_instance_name}
```

- [ ] **Step 4: Register the router in main.py**

In `api/main.py`, add the import alongside the other router imports:

```python
from routers.config import router as config_router
```

And add the router registration after the existing `app.include_router` calls:

```python
app.include_router(config_router, prefix="/api")
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
docker compose exec api pytest tests/test_config.py -v
```

Expected: all PASS.

- [ ] **Step 6: Run the full test suite**

```bash
docker compose exec api pytest tests/ -v
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add api/routers/config.py api/main.py api/tests/test_config.py
git commit -m "feat: add /api/config/evolution-instance endpoint for n8n"
```

---

## Task 6: Admin UI — settings field

**Files:**
- Modify: `frontend/js/admin.js`

The admin UI is in `frontend/js/admin.js`. The page has a settings form with inputs for each setting. You need to add `evolution_instance_name` as a text input, wire it into the load, save, and validation logic.

- [ ] **Step 1: Add the HTML input field**

In the `setHtml(...)` template inside `renderAdmin()`, add the new field inside the `<div id="admin-settings-form">` block, after the `a-backup-retention` field and before the error div:

```html
        <div class="field">
          <label for="a-evolution-instance">Ime instance (WhatsApp)</label>
          <input id="a-evolution-instance" type="text" style="width:100%;max-width:24rem" />
        </div>
```

- [ ] **Step 2: Load the value from the API response**

In the `// Load current settings` block, after the existing `$('a-backup-retention').value = data.backup_retention_days;` line, add:

```js
    $('a-evolution-instance').value = data.evolution_instance_name;
```

- [ ] **Step 3: Include the value in the save handler's `current` object**

In the save handler, add `evolution_instance_name` to the `current` object:

```js
    const current = {
      max_photos_per_entry:   parseInt($('a-max-photos').value, 10),
      photo_retention_days:   parseInt($('a-photo-retention').value, 10),
      session_duration_hours: parseInt($('a-session-duration').value, 10),
      report_auto_day:        parseInt($('a-report-day').value, 10),
      report_auto_period:     $('a-report-period').value,
      report_auto_hour:       parseInt($('a-report-hour').value, 10),
      backup_hour:            parseInt($('a-backup-hour').value, 10),
      photo_cleanup_hour:     parseInt($('a-cleanup-hour').value, 10),
      backup_retention_days:  parseInt($('a-backup-retention').value, 10),
      evolution_instance_name: $('a-evolution-instance').value.trim(),
    };
```

- [ ] **Step 4: Add validation for the string field**

In the validation `for` loop, add a skip for `evolution_instance_name` so the integer validation doesn't reject it, then add a separate string validation after the loop:

```js
    // Validate
    for (const [key, val] of Object.entries(current)) {
      if (key === 'report_auto_period') continue;
      if (key === 'evolution_instance_name') continue;   // ← add this line
      if (key === 'backup_hour' || key === 'photo_cleanup_hour' || key === 'report_auto_hour') {
        // ... existing hour validation unchanged ...
      }
      // ... rest of existing loop unchanged ...
    }

    if (!current.evolution_instance_name) {
      errEl.textContent = 'Ime instance ne sme biti prazno.';
      errEl.style.display = 'block';
      return;
    }
```

- [ ] **Step 5: Manual test in the browser**

Start the stack if not running:

```bash
docker compose up -d
```

Open http://localhost:80, navigate to Administracija. Verify:
- The "Ime instance (WhatsApp)" field loads with `belpro` (or current DB value)
- Changing the value and clicking Shrani shows the success toast
- Reloading the page shows the saved value

- [ ] **Step 6: Commit**

```bash
git add frontend/js/admin.js
git commit -m "feat: add evolution_instance_name field to admin settings UI"
```

---

## Task 7: n8n — manager_approval workflow

**Files:**
- Modify: `n8n/workflows/manager_approval.json`

**Context:** This workflow handles manager WhatsApp approval responses. It currently has hardcoded `belpro` in all `http://evolution-api:8080/message/sendText/belpro` and similar URLs. You will add a `Fetch Config` HTTP Request node that fetches the instance name from the API, then rewrite all Evolution API URLs as n8n expressions.

- [ ] **Step 1: Find all Evolution API URL occurrences in manager_approval.json**

```bash
grep -n "evolution-api.*belpro" n8n/workflows/manager_approval.json
```

Note the line numbers — you need to update every occurrence.

- [ ] **Step 2: Find the trigger node and its first connected node**

In `n8n/workflows/manager_approval.json`, find the `connections` section (near the end of the file). Find what node(s) `Execute Workflow Trigger` and `Manual Trigger` connect to — this is the node you will insert `Fetch Config` before.

- [ ] **Step 3: Add the Fetch Config node to the nodes array**

In the `"nodes"` array, add the following node. Position it just to the right of the trigger node(s) — use `x = trigger_x + 260, y = trigger_y` as a starting point:

```json
{
  "parameters": {
    "url": "http://api:8000/api/config/evolution-instance",
    "options": {}
  },
  "id": "fetch_config",
  "name": "Fetch Config",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4,
  "position": [
    500,
    304
  ]
}
```

Adjust `position` so it fits between the trigger(s) and the next node in the visual layout.

- [ ] **Step 4: Rewire connections**

In the `connections` section:

1. Find the connection(s) from `Execute Workflow Trigger` (and `Manual Trigger`) to their current first target node.
2. Change those connections to point to `Fetch Config` instead.
3. Add a new connection from `Fetch Config` to the original first target node:

```json
"Fetch Config": {
  "main": [
    [
      {
        "node": "<original first target node name>",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

- [ ] **Step 5: Replace all hardcoded Evolution API URLs with expressions**

For every occurrence of `"http://evolution-api:8080/message/sendText/belpro"`, replace with:

```json
"={{ 'http://evolution-api:8080/message/sendText/' + $('Fetch Config').first().json.instance_name }}"
```

For every occurrence of `"http://evolution-api:8080/chat/getBase64FromMediaMessage/belpro"`, replace with:

```json
"={{ 'http://evolution-api:8080/chat/getBase64FromMediaMessage/' + $('Fetch Config').first().json.instance_name }}"
```

The key change is: plain string URLs become expression strings (prefixed with `=`).

- [ ] **Step 6: Import the workflow into n8n**

```bash
python scripts/n8n_workflows.py import
```

Expected: imports without errors.

- [ ] **Step 7: Verify in n8n UI**

Open http://localhost:5678, find "BelPro — Odobritev Upravljalca". Verify:
- `Fetch Config` node appears in the canvas connected between the trigger(s) and the next node
- One of the `sendText` HTTP Request nodes shows the expression URL (click the node, check the URL field — it should show the expression, not `belpro`)

- [ ] **Step 8: Commit**

```bash
git add n8n/workflows/manager_approval.json
git commit -m "feat: fetch evolution instance name dynamically in manager_approval workflow"
```

---

## Task 8: n8n — volunteer_entry workflow

**Files:**
- Modify: `n8n/workflows/volunteer_entry.json`

**Context:** Same pattern as Task 7 but for the larger volunteer_entry workflow. This workflow is triggered by an incoming WhatsApp webhook (not an Execute Workflow trigger). It has many more Evolution API URL occurrences (~20 HTTP Request nodes).

- [ ] **Step 1: Find all Evolution API URL occurrences**

```bash
grep -n "evolution-api.*belpro" n8n/workflows/volunteer_entry.json
```

Note all line numbers.

- [ ] **Step 2: Find the webhook trigger node and its first connected node**

In `n8n/workflows/volunteer_entry.json`, find the webhook trigger node in `"nodes"` (type will be `n8n-nodes-base.webhook`). Then find its connection in `"connections"` to identify the first target node.

- [ ] **Step 3: Add the Fetch Config node**

Add the same `Fetch Config` node as in Task 7 to the `"nodes"` array. Position it between the webhook trigger and the next node.

```json
{
  "parameters": {
    "url": "http://api:8000/api/config/evolution-instance",
    "options": {}
  },
  "id": "fetch_config",
  "name": "Fetch Config",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4,
  "position": [
    <webhook_x + 260>,
    <webhook_y>
  ]
}
```

- [ ] **Step 4: Rewire connections**

Same as Task 7 Step 4:
1. Change the webhook trigger's outgoing connection(s) to point to `Fetch Config`
2. Add connection from `Fetch Config` to the original first target node

- [ ] **Step 5: Replace all hardcoded Evolution API URLs**

Apply the same replacements as Task 7 Step 5 to every occurrence in this file. There are more occurrences — be thorough. After editing, verify the count:

```bash
grep -c "evolution-api.*belpro" n8n/workflows/volunteer_entry.json
```

Expected: `0`

And verify the expressions are in place:

```bash
grep -c "Fetch Config.*instance_name\|instance_name.*Fetch Config" n8n/workflows/volunteer_entry.json
```

Expected: matches equal to the number of Evolution API nodes you updated.

- [ ] **Step 6: Import and verify**

```bash
python scripts/n8n_workflows.py import
```

Open http://localhost:5678, find "BelPro — Vnos Prostovoljcev". Verify `Fetch Config` appears and URL expressions are set.

- [ ] **Step 7: Run the full API test suite one final time**

```bash
docker compose exec api pytest tests/ -v
```

Expected: all pass.

- [ ] **Step 8: Final commit**

```bash
git add n8n/workflows/volunteer_entry.json
git commit -m "feat: fetch evolution instance name dynamically in volunteer_entry workflow"
```

---

## Done

After all 8 tasks:

- `evolution_instance_name` is seeded in the DB from `.env` on migration
- It is a runtime-tunable AppSettings property (DB-first, env-fallback)
- `GET /api/admin/settings` and `PATCH /api/admin/settings` include the field
- The admin UI shows it as an editable text input
- `GET /api/config/evolution-instance` exposes it publicly for n8n
- Both `manager_approval` and `volunteer_entry` workflows fetch it dynamically
- No hardcoded `belpro` remains in n8n workflow URLs
- All API tests pass
