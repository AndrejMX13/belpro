# Configurable Backup Retention Days Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the backup retention period configurable from the Administracija dashboard page, stored in the `settings` DB table alongside the existing schedule settings.

**Architecture:** `backup_retention_days` follows the exact same pattern as `backup_hour` and `photo_cleanup_hour` added in the previous session. The value is stored in the `AppSetting` key-value table, exposed via `GET/PATCH /api/admin/settings`, included in the `POST /reconfigure` payload to the ops server, and passed as a CLI argument `$1` to `backup.sh` in the generated crontab line — keeping the existing `BACKUP_RETENTION_DAYS` env var as a silent fallback so existing deployments don't break.

**Tech Stack:** FastAPI + Pydantic (API), Python stdlib (ops_server), Bash (backup.sh), vanilla JS (frontend)

---

## Files Changed

| File | Change |
|------|--------|
| `api/services/app_settings.py` | Add `backup_retention_days` property |
| `api/schemas/admin.py` | Add field to response and update schemas |
| `api/routers/admin.py` | Include in `_notify_ops` payload and both `AdminSettingsResponse` constructions |
| `api/tests/test_admin.py` | Add two tests (default value + save round-trip) |
| `ops/scripts/ops_server.py` | Pass `{retention_days}` arg to backup.sh in template; update `write_crontab` signature, `fetch_settings_from_db` query, `do_POST`, and startup sync |
| `ops/scripts/backup.sh` | Read `${1:-${BACKUP_RETENTION_DAYS:-30}}` instead of `${BACKUP_RETENTION_DAYS:-30}` |
| `frontend/js/admin.js` | Add `backup_retention_days` number input; existing `>= 1` validation covers it |
| `README.md` | Update backup section: retention now configurable from dashboard |
| `README_SL.md` | Same in Slovenian |

---

## Task 1: AppSettings property + schemas

**Files:**
- Modify: `api/services/app_settings.py`
- Modify: `api/schemas/admin.py`

- [ ] **Step 1: Add `backup_retention_days` property to `AppSettings`**

In `api/services/app_settings.py`, add after the `photo_cleanup_hour` property (around line 92):

```python
@property
def backup_retention_days(self) -> int:
    """Number of days local backup archives are kept before pruning."""
    return max(1, self._int("backup_retention_days", 30))
```

- [ ] **Step 2: Add fields to `AdminSettingsResponse` and `AdminSettingsUpdate`**

In `api/schemas/admin.py`, the full file becomes:

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
    backup_hour: int | None = Field(None, ge=0, le=23)
    photo_cleanup_hour: int | None = Field(None, ge=0, le=23)
    backup_retention_days: int | None = Field(None, ge=1)
```

- [ ] **Step 3: Commit**

```bash
git add api/services/app_settings.py api/schemas/admin.py
git commit -m "feat: add backup_retention_days AppSettings property and schema fields"
```

---

## Task 2: Admin router

**Files:**
- Modify: `api/routers/admin.py`

- [ ] **Step 1: Add `backup_retention_days` to the `_notify_ops` payload**

In `api/routers/admin.py`, find the `payload` dict inside `_notify_ops` (currently lines 26–29) and add the new key:

```python
    payload = {
        "report_auto_day": s.report_auto_day,
        "report_auto_period": s.report_auto_period,
        "backup_hour": s.backup_hour,
        "photo_cleanup_hour": s.photo_cleanup_hour,
        "backup_retention_days": s.backup_retention_days,
    }
```

- [ ] **Step 2: Add `backup_retention_days` to both `AdminSettingsResponse` constructions**

There are two `return AdminSettingsResponse(...)` calls — one in `get_admin_settings` and one in `update_admin_settings`. Both need the new field. Find and update both:

```python
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
        backup_hour=s.backup_hour,
        photo_cleanup_hour=s.photo_cleanup_hour,
        backup_retention_days=s.backup_retention_days,
    )
```

- [ ] **Step 3: Commit**

```bash
git add api/routers/admin.py
git commit -m "feat: include backup_retention_days in ops notification and settings response"
```

---

## Task 3: Tests

**Files:**
- Modify: `api/tests/test_admin.py`

- [ ] **Step 1: Add two tests to `api/tests/test_admin.py`**

Append to the end of the file:

```python
async def test_get_settings_returns_backup_retention_default(
    client: AsyncClient, auth: dict
) -> None:
    """GET /api/admin/settings returns default backup_retention_days of 30."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["backup_retention_days"] == 30


async def test_patch_settings_saves_backup_retention(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH /api/admin/settings persists backup_retention_days."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"backup_retention_days": 14},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["backup_retention_days"] == 14
```

- [ ] **Step 2: Run tests — expect failure (field not yet in ops_server)**

```bash
docker compose exec api pytest tests/test_admin.py -v
```

Expected: `test_get_settings_returns_backup_retention_default` and `test_patch_settings_saves_backup_retention` both FAIL because the API container is not yet rebuilt with Task 1–2 changes.

- [ ] **Step 3: Rebuild API container and re-run**

```bash
docker compose up -d --build api
docker compose exec api pytest tests/test_admin.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 4: Commit**

```bash
git add api/tests/test_admin.py
git commit -m "test: add backup_retention_days default and save tests"
```

---

## Task 4: ops_server.py + backup.sh

**Files:**
- Modify: `ops/scripts/ops_server.py`
- Modify: `ops/scripts/backup.sh`

- [ ] **Step 1: Update `CRONTAB_TEMPLATE` in `ops/scripts/ops_server.py`**

Pass `{retention_days}` as `$1` to `backup.sh`. Find the `CRONTAB_TEMPLATE` constant (currently lines 40–46) and replace it:

```python
CRONTAB_TEMPLATE = (
    "# m h dom mon dow command\n"
    "0 {backup_hour} * * * /app/scripts/backup.sh {retention_days} >> /proc/1/fd/1 2>&1\n"
    "0 {cleanup_hour} * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1\n"
    "0 7 {day} * * /app/scripts/monthly_report_send.py --period {period}"
    " >> /proc/1/fd/1 2>&1\n"
)
```

- [ ] **Step 2: Update `write_crontab` signature**

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

- [ ] **Step 3: Update `fetch_settings_from_db` query**

Find the `cur.execute(...)` call in `fetch_settings_from_db` and add `'backup_retention_days'` to the `IN` list:

```python
            cur.execute(
                "SELECT name, value FROM settings"
                " WHERE name IN ('report_auto_day', 'report_auto_period',"
                " 'backup_hour', 'photo_cleanup_hour', 'backup_retention_days')"
            )
```

- [ ] **Step 4: Update `do_POST` — extract `backup_retention_days` from payload**

In the `do_POST` method, add after the `cleanup_hour` line:

```python
        retention_days = max(1, int(payload.get("backup_retention_days", 30)))
```

Then update the `write_crontab(...)` call in `do_POST` to pass the new argument:

```python
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days)
```

- [ ] **Step 5: Update startup sync in `main()`**

In `main()`, add after the `cleanup_hour` line:

```python
        retention_days = max(1, int(rows.get("backup_retention_days", 30)))
```

Then update the `write_crontab(...)` call in `main()`:

```python
            write_crontab(day, period, backup_hour, cleanup_hour, retention_days)
```

And update the log line:

```python
            logger.info(
                "Startup crontab sync complete (day=%d, period=%s, backup_hour=%d, cleanup_hour=%d, retention_days=%d).",
                day, period, backup_hour, cleanup_hour, retention_days,
            )
```

- [ ] **Step 6: Update `backup.sh` to read `$1` as retention days**

In `ops/scripts/backup.sh`, change line 6 from:

```bash
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
```

to:

```bash
RETENTION_DAYS="${1:-${BACKUP_RETENTION_DAYS:-30}}"
```

No other changes needed in `backup.sh`.

- [ ] **Step 7: Rebuild ops container and verify crontab**

```bash
docker compose up -d --build ops
docker compose exec ops cat /etc/crontabs/ops
```

Expected output (with defaults):
```
# m h dom mon dow command
0 2 * * * /app/scripts/backup.sh 30 >> /proc/1/fd/1 2>&1
0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1
0 7 28 * * /app/scripts/monthly_report_send.py --period current >> /proc/1/fd/1 2>&1
```

- [ ] **Step 8: Commit**

```bash
git add ops/scripts/ops_server.py ops/scripts/backup.sh
git commit -m "feat: pass backup_retention_days as CLI arg to backup.sh via crontab"
```

---

## Task 5: Frontend

**Files:**
- Modify: `frontend/js/admin.js`

- [ ] **Step 1: Add the HTML input field**

In `renderAdmin()`, add a new `.field` div after the `a-cleanup-hour` block (just before `admin-settings-error`):

```html
        <div class="field">
          <label for="a-backup-retention">Hranjenje varnostnih kopij (dni)</label>
          <input id="a-backup-retention" type="number" min="1" style="width:100%;max-width:12rem" step="1" />
        </div>
```

- [ ] **Step 2: Load the value from API response**

In the settings load block, add after the `a-cleanup-hour` line:

```js
    $('a-backup-retention').value = data.backup_retention_days;
```

- [ ] **Step 3: Include in the `current` object**

In the save handler's `current` object, add:

```js
      backup_retention_days:  parseInt($('a-backup-retention').value, 10),
```

- [ ] **Step 4: Validation**

The existing `>= 1` check in the validation loop already covers `backup_retention_days` (it's an integer field with no upper bound). No extra validation needed.

- [ ] **Step 5: Hard-reload browser and verify**

Navigate to `http://localhost/#admin`. The new field "Hranjenje varnostnih kopij (dni)" should appear showing `30`. Change it to `14`, click Shrani, reload — should persist `14`. Then reset to `30` and save.

- [ ] **Step 6: Commit**

```bash
git add frontend/js/admin.js
git commit -m "feat: add backup_retention_days input to Sistemske nastavitve"
```

---

## Task 6: README updates

**Files:**
- Modify: `README.md`
- Modify: `README_SL.md`

- [ ] **Step 1: Update English README**

In `README.md`, find the backup section sentence that currently reads:

```
Retention is controlled by `BACKUP_RETENTION_DAYS` in `.env` (default: 30 days).
```

Replace with:

```
Retention is configurable from the System administration page (default: 30 days); the `BACKUP_RETENTION_DAYS` env var is still accepted as a fallback.
```

Also update the **System administration** bullet (line ~44) to include the new setting in the list — change:

```
... backup hour, photo-cleanup hour; ...
```

to:

```
... backup hour, photo-cleanup hour, backup retention period; ...
```

- [ ] **Step 2: Update Slovenian README**

In `README_SL.md`, find:

```
Čas hrambe kopij je določen s spremenljivko `BACKUP_RETENTION_DAYS` v `.env` (privzeto: 30 dni).
```

Replace with:

```
Čas hrambe kopij je nastavljiv na strani Administracija (privzeto: 30 dni); spremenljivka `BACKUP_RETENTION_DAYS` v `.env` je še vedno sprejeta kot nadomestna vrednost.
```

Also update the **Administracija** bullet to include the new setting — change:

```
... ura varnostnega kopiranja, ura čiščenja fotografij; ...
```

to:

```
... ura varnostnega kopiranja, ura čiščenja fotografij, obdobje hrambe varnostnih kopij; ...
```

- [ ] **Step 3: Commit**

```bash
git add README.md README_SL.md
git commit -m "docs: update READMEs — backup retention now configurable from dashboard"
```
