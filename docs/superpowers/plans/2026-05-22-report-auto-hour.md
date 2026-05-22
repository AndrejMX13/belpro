# Report Auto-Hour Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the hour at which monthly reports are automatically sent configurable (default 7), and fill in missing test coverage for existing hour-type settings.

**Architecture:** `report_auto_hour` follows the identical pattern as `backup_hour` and `photo_cleanup_hour` — AppSettings property → schema fields → admin router payload → ops server crontab template. The frontend form field and validation mirror the existing `backup_hour` field exactly. Tests are written first (TDD) for each layer.

**Tech Stack:** Python/FastAPI (AppSettings, schemas, router), plain Python HTTP server (ops/scripts/ops_server.py), Alembic data-seed migration, vanilla JS (frontend/js/admin.js).

---

## File Map

| File | Change |
|------|--------|
| `api/services/app_settings.py` | Add `report_auto_hour` property after `photo_cleanup_hour` |
| `api/schemas/admin.py` | Add field to `AdminSettingsResponse` and `AdminSettingsUpdate` |
| `api/routers/admin.py` | Add `report_auto_hour` in `_notify_ops` payload and both `AdminSettingsResponse` constructions |
| `ops/scripts/ops_server.py` | Replace hardcoded `7` in `CRONTAB_TEMPLATE`; add param to `write_crontab`, `fetch_settings_from_db`, `do_POST`, `main` |
| `api/db/migrations/versions/014_seed_report_auto_hour.py` | Data-seed migration: INSERT one row into `settings` |
| `frontend/js/admin.js` | Add `a-report-hour` field in HTML template, populate in load, read+validate in save handler |
| `api/tests/test_app_settings.py` | Add unit tests for `report_auto_hour` (default, DB override, clamping) |
| `api/tests/test_admin.py` | Add GET-default, PATCH-persist, boundary, and ops-payload tests for `report_auto_hour`; add missing coverage for `backup_hour` and `photo_cleanup_hour` |

---

## Task 1: AppSettings unit tests + property

**Files:**
- Modify: `api/services/app_settings.py` (after line 91)
- Modify: `api/tests/test_app_settings.py` (append)

- [ ] **Step 1: Append failing tests to `api/tests/test_app_settings.py`**

```python
def test_appsettings_report_auto_hour_default() -> None:
    """report_auto_hour defaults to 7 when no DB row exists."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {})
    assert s.report_auto_hour == 7


def test_appsettings_report_auto_hour_from_db() -> None:
    """report_auto_hour reads the DB value when present."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {"report_auto_hour": "9"})
    assert s.report_auto_hour == 9


def test_appsettings_report_auto_hour_clamped_high() -> None:
    """report_auto_hour clamps values above 23 to 23."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {"report_auto_hour": "99"})
    assert s.report_auto_hour == 23


def test_appsettings_report_auto_hour_clamped_low() -> None:
    """report_auto_hour clamps negative values to 0."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {"report_auto_hour": "-5"})
    assert s.report_auto_hour == 0
```

- [ ] **Step 2: Run tests to verify they fail**

```
docker compose exec api pytest tests/test_app_settings.py::test_appsettings_report_auto_hour_default tests/test_app_settings.py::test_appsettings_report_auto_hour_from_db tests/test_app_settings.py::test_appsettings_report_auto_hour_clamped_high tests/test_app_settings.py::test_appsettings_report_auto_hour_clamped_low -v
```

Expected: FAIL — `AttributeError: 'AppSettings' object has no attribute 'report_auto_hour'`

- [ ] **Step 3: Add the `report_auto_hour` property to `api/services/app_settings.py`**

After the `photo_cleanup_hour` property (after line 91), insert:

```python
    @property
    def report_auto_hour(self) -> int:
        """Hour of day (0–23) at which the monthly report cron fires."""
        return max(0, min(self._int("report_auto_hour", 7), 23))
```

- [ ] **Step 4: Run tests to verify they pass**

```
docker compose exec api pytest tests/test_app_settings.py::test_appsettings_report_auto_hour_default tests/test_app_settings.py::test_appsettings_report_auto_hour_from_db tests/test_app_settings.py::test_appsettings_report_auto_hour_clamped_high tests/test_app_settings.py::test_appsettings_report_auto_hour_clamped_low -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```
git add api/services/app_settings.py api/tests/test_app_settings.py
git commit -m "feat(settings): add report_auto_hour AppSettings property with unit tests"
```

---

## Task 2: Schema and router

**Files:**
- Modify: `api/schemas/admin.py`
- Modify: `api/routers/admin.py`
- Modify: `api/tests/test_admin.py` (append)

- [ ] **Step 1: Append failing tests to `api/tests/test_admin.py`**

```python
async def test_get_settings_returns_report_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns report_auto_hour default of 7."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["report_auto_hour"] == 7


async def test_patch_settings_saves_report_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists report_auto_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 9},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["report_auto_hour"] == 9


async def test_patch_settings_report_hour_boundary_zero(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings accepts report_auto_hour=0."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 0},
            headers=auth,
        )

    assert r.status_code == 200


async def test_patch_settings_report_hour_boundary_23(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings accepts report_auto_hour=23."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 23},
            headers=auth,
        )

    assert r.status_code == 200


async def test_patch_settings_report_hour_rejects_24(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings rejects report_auto_hour=24."""
    r = await client.patch(
        "/api/admin/settings",
        json={"report_auto_hour": 24},
        headers=auth,
    )
    assert r.status_code == 422


async def test_patch_settings_report_hour_rejects_negative(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings rejects report_auto_hour=-1."""
    r = await client.patch(
        "/api/admin/settings",
        json={"report_auto_hour": -1},
        headers=auth,
    )
    assert r.status_code == 422


async def test_patch_settings_ops_payload_includes_report_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings includes report_auto_hour in ops /reconfigure payload."""
    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))

    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 9},
            headers=auth,
        )

    assert r.status_code == 200
    call_args = mock_http.post.call_args
    assert "report_auto_hour" in call_args[1]["json"]


# ── Missing coverage for existing hour-type settings ──────────────────────────

async def test_get_settings_returns_backup_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns backup_hour default of 2."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["backup_hour"] == 2


async def test_patch_settings_saves_backup_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists backup_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"backup_hour": 4},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["backup_hour"] == 4


async def test_get_settings_returns_photo_cleanup_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns photo_cleanup_hour default of 3."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["photo_cleanup_hour"] == 3


async def test_patch_settings_saves_photo_cleanup_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists photo_cleanup_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"photo_cleanup_hour": 5},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["photo_cleanup_hour"] == 5


async def test_patch_settings_ops_payload_includes_all_fields(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings sends all tunable fields to ops /reconfigure."""
    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))

    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 1},
            headers=auth,
        )

    assert r.status_code == 200
    payload = mock_http.post.call_args[1]["json"]
    for field in ("report_auto_day", "report_auto_period", "backup_hour",
                  "photo_cleanup_hour", "backup_retention_days", "report_auto_hour"):
        assert field in payload, f"Missing field in ops payload: {field}"
```

- [ ] **Step 2: Run tests to verify they fail**

```
docker compose exec api pytest tests/test_admin.py::test_get_settings_returns_report_hour_default tests/test_admin.py::test_patch_settings_saves_report_hour tests/test_admin.py::test_patch_settings_report_hour_rejects_24 -v
```

Expected: FAIL — `KeyError: 'report_auto_hour'` (field not in response yet)

- [ ] **Step 3: Update `api/schemas/admin.py`**

Replace the full file with:

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
```

- [ ] **Step 4: Update `api/routers/admin.py`**

In `_notify_ops`, the `payload` dict — add `"report_auto_hour": s.report_auto_hour,`:

```python
    payload = {
        "report_auto_day": s.report_auto_day,
        "report_auto_period": s.report_auto_period,
        "report_auto_hour": s.report_auto_hour,
        "backup_hour": s.backup_hour,
        "photo_cleanup_hour": s.photo_cleanup_hour,
        "backup_retention_days": s.backup_retention_days,
    }
```

In `get_admin_settings`, the `AdminSettingsResponse(...)` call — add `report_auto_hour=s.report_auto_hour,`:

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
    )
```

In `update_admin_settings`, the `AdminSettingsResponse(...)` call — same addition:

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
    )
```

- [ ] **Step 5: Run all new admin tests**

```
docker compose exec api pytest tests/test_admin.py -v
```

Expected: all pass (including the previously existing tests)

- [ ] **Step 6: Commit**

```
git add api/schemas/admin.py api/routers/admin.py api/tests/test_admin.py
git commit -m "feat(admin): expose report_auto_hour in schema, router, and ops payload; add missing hour-setting tests"
```

---

## Task 3: Ops server

**Files:**
- Modify: `ops/scripts/ops_server.py`

The ops server has no automated test harness — verify by reading the written crontab content after startup.

- [ ] **Step 1: Update `CRONTAB_TEMPLATE` in `ops/scripts/ops_server.py`**

Replace:
```python
CRONTAB_TEMPLATE = (
    "# m h dom mon dow command\n"
    "0 {backup_hour} * * * /app/scripts/backup.sh {retention_days} >> /proc/1/fd/1 2>&1\n"
    "0 {cleanup_hour} * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1\n"
    "0 7 {day} * * /app/scripts/monthly_report_send.py --period {period}"
    " >> /proc/1/fd/1 2>&1\n"
)
```

With:
```python
CRONTAB_TEMPLATE = (
    "# m h dom mon dow command\n"
    "0 {backup_hour} * * * /app/scripts/backup.sh {retention_days} >> /proc/1/fd/1 2>&1\n"
    "0 {cleanup_hour} * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1\n"
    "0 {report_hour} {day} * * /app/scripts/monthly_report_send.py --period {period}"
    " >> /proc/1/fd/1 2>&1\n"
)
```

- [ ] **Step 2: Update `write_crontab` signature and body**

Replace:
```python
def write_crontab(
    day: int, period: str, backup_hour: int, cleanup_hour: int, retention_days: int
) -> None:
    """Write a new crontab to CRONTAB_PATH and reload crond."""
    content = CRONTAB_TEMPLATE.format(
        day=day,
        period=period,
        backup_hour=backup_hour,
        cleanup_hour=cleanup_hour,
        retention_days=retention_days,
    )
    CRONTAB_PATH.write_text(content)
    reload_crond()
    logger.info(
        "Crontab updated: day=%d period=%s backup_hour=%d cleanup_hour=%d retention_days=%d",
        day, period, backup_hour, cleanup_hour, retention_days,
    )
```

With:
```python
def write_crontab(
    day: int, period: str, backup_hour: int, cleanup_hour: int, retention_days: int,
    report_hour: int = 7,
) -> None:
    """Write a new crontab to CRONTAB_PATH and reload crond."""
    content = CRONTAB_TEMPLATE.format(
        day=day,
        period=period,
        backup_hour=backup_hour,
        cleanup_hour=cleanup_hour,
        retention_days=retention_days,
        report_hour=report_hour,
    )
    CRONTAB_PATH.write_text(content)
    reload_crond()
    logger.info(
        "Crontab updated: day=%d period=%s report_hour=%d backup_hour=%d cleanup_hour=%d retention_days=%d",
        day, period, report_hour, backup_hour, cleanup_hour, retention_days,
    )
```

- [ ] **Step 3: Update `fetch_settings_from_db` query**

Replace the `WHERE name IN (...)` line:
```python
                cur.execute(
                    "SELECT name, value FROM settings"
                    " WHERE name IN ('report_auto_day', 'report_auto_period',"
                    " 'backup_hour', 'photo_cleanup_hour', 'backup_retention_days')"
                )
```

With:
```python
                cur.execute(
                    "SELECT name, value FROM settings"
                    " WHERE name IN ('report_auto_day', 'report_auto_period',"
                    " 'report_auto_hour', 'backup_hour', 'photo_cleanup_hour',"
                    " 'backup_retention_days')"
                )
```

- [ ] **Step 4: Update `do_POST` to parse `report_auto_hour`**

After the `retention_days` line (line 166), add:
```python
        report_hour = max(0, min(int(payload.get("report_auto_hour", 7)), 23))
```

And pass it to `write_crontab`:
```python
        try:
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days, report_hour=report_hour)
```

- [ ] **Step 5: Update `main()` to read `report_auto_hour` from DB**

After the `retention_days` line in `main()`, add:
```python
        report_hour = max(0, min(int(rows.get("report_auto_hour", 7)), 23))
```

And pass it to `write_crontab`:
```python
        try:
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days, report_hour=report_hour)
```

Also update the log line in `main()`:
```python
            logger.info(
                "Startup crontab sync complete (day=%d, period=%s, report_hour=%d, backup_hour=%d, cleanup_hour=%d, retention_days=%d).",
                day, period, report_hour, backup_hour, cleanup_hour, retention_days,
            )
```

- [ ] **Step 6: Rebuild the ops container and verify the crontab**

```
docker compose up -d --build ops
docker compose exec ops cat /etc/crontabs/ops
```

Expected output contains `0 7 28 * *` (default hour=7, day=28) on the monthly report line — not the hardcoded literal `7` from before, but the same value sourced from `{report_hour}`.

- [ ] **Step 7: Commit**

```
git add ops/scripts/ops_server.py
git commit -m "feat(ops): make report cron hour configurable via report_auto_hour setting"
```

---

## Task 4: Data seed migration

**Files:**
- Create: `api/db/migrations/versions/014_seed_report_auto_hour.py`

- [ ] **Step 1: Create the migration file**

```python
"""Seed report_auto_hour setting row.

Revision ID: 014
Revises: 013
Create Date: 2026-05-22
"""
from __future__ import annotations
from typing import Sequence, Union
from alembic import op

revision: str = "014"
down_revision: Union[str, None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the report_auto_hour settings row with default value 7."""
    op.execute(
        "INSERT INTO settings (name, value, value_type) "
        "VALUES ('report_auto_hour', '7', 'int') "
        "ON CONFLICT (name) DO NOTHING"
    )


def downgrade() -> None:
    """Remove the report_auto_hour settings row."""
    op.execute("DELETE FROM settings WHERE name = 'report_auto_hour'")
```

- [ ] **Step 2: Run the migration**

```
docker compose exec api alembic upgrade head
```

Expected: `Running upgrade 013 -> 014, Seed report_auto_hour setting row`

- [ ] **Step 3: Verify the row exists**

```
docker compose exec api alembic current
```

Expected: `014 (head)`

- [ ] **Step 4: Commit**

```
git add api/db/migrations/versions/014_seed_report_auto_hour.py
git commit -m "chore(db): seed report_auto_hour settings row (default 7)"
```

---

## Task 5: Frontend

**Files:**
- Modify: `frontend/js/admin.js`

- [ ] **Step 1: Add the HTML input field in `renderAdmin()`**

In the `setHtml(...)` template literal, after the `a-report-period` field block and before the `a-backup-hour` field block, insert:

```html
        <div class="field">
          <label for="a-report-hour">Ura samodejnega po&#353;iljanja poro&#269;il (0&#8211;23)</label>
          <input id="a-report-hour" type="number" min="0" max="23" style="width:100%;max-width:12rem" step="1" />
        </div>
```

- [ ] **Step 2: Populate the field when settings load**

After `$('a-report-period').value = data.report_auto_period;` (line 78), add:

```javascript
    $('a-report-hour').value   = data.report_auto_hour;
```

- [ ] **Step 3: Read the field in the save handler**

In the `current` object (around line 98), add after `report_auto_period`:

```javascript
      report_auto_hour:       parseInt($('a-report-hour').value, 10),
```

- [ ] **Step 4: Add validation for `report_auto_hour`**

In the validation loop, the existing `if (key === 'backup_hour' || key === 'photo_cleanup_hour')` block handles 0–23 range. Extend it to also cover `report_auto_hour`:

Replace:
```javascript
      if (key === 'backup_hour' || key === 'photo_cleanup_hour') {
        if (!Number.isInteger(val) || val < 0 || val > 23) {
          const label = key === 'backup_hour' ? 'varnostnega kopiranja' : 'čiščenja fotografij';
          errEl.textContent = `Ura ${label} mora biti med 0 in 23.`;
          errEl.style.display = 'block';
          return;
        }
        continue;
      }
```

With:
```javascript
      if (key === 'backup_hour' || key === 'photo_cleanup_hour' || key === 'report_auto_hour') {
        if (!Number.isInteger(val) || val < 0 || val > 23) {
          const labels = {
            backup_hour: 'varnostnega kopiranja',
            photo_cleanup_hour: 'čiščenja fotografij',
            report_auto_hour: 'pošiljanja poročil',
          };
          errEl.textContent = `Ura ${labels[key]} mora biti med 0 in 23.`;
          errEl.style.display = 'block';
          return;
        }
        continue;
      }
```

- [ ] **Step 5: Verify in browser**

Open the admin dashboard → Sistemske nastavitve. Confirm:
- "Ura samodejnega pošiljanja poročil (0–23)" input appears between the period dropdown and the backup hour field
- Field shows value `7` on load
- Entering `24` and clicking Shrani shows the Slovenian validation error
- Entering `9` and saving shows a success toast and persists (reload confirms `9`)

- [ ] **Step 6: Commit**

```
git add frontend/js/admin.js
git commit -m "feat(frontend): add report_auto_hour input to admin settings form"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Task |
|-----------------|------|
| AppSettings `report_auto_hour` property, default 7, clamped 0–23 | Task 1 |
| Schema: `AdminSettingsResponse` and `AdminSettingsUpdate` fields | Task 2 |
| Admin router `_notify_ops` payload and both `AdminSettingsResponse` constructions | Task 2 |
| Ops: `CRONTAB_TEMPLATE` `{report_hour}`, `write_crontab` param, `fetch_settings_from_db` query, `do_POST` parse, `main` startup sync | Task 3 |
| Data seed migration for `report_auto_hour = 7` | Task 4 |
| Frontend input field, populate, read, validate | Task 5 |
| Tests: `report_auto_hour` GET default, PATCH persist, boundary 0/23/24/-1, ops payload | Task 2 |
| Tests: AppSettings unit default/DB/clamp-high/clamp-low | Task 1 |
| Tests: missing `backup_hour` and `photo_cleanup_hour` GET default and PATCH persist | Task 2 |
| Tests: ops payload includes all fields | Task 2 |

All spec items covered. No placeholders. Type and signature consistency confirmed across all tasks.
