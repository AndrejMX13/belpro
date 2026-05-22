# Report Auto-Hour Implementation Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the hour at which monthly reports are automatically sent configurable from the admin dashboard, instead of hardcoded to 07:00.

**Architecture:** `report_auto_hour` follows the exact same end-to-end pattern as `backup_hour` and `photo_cleanup_hour` — AppSettings property → schema fields → admin router payload → ops server crontab. Additionally, missing test coverage for existing hour-type settings (`backup_hour`, `photo_cleanup_hour`) is added in the same pass.

**Tech Stack:** Python/FastAPI (AppSettings, schemas, router), plain Python HTTP server (ops_server.py), Alembic (data seed migration), vanilla JS (admin frontend).

---

## Scope

Two concerns in one plan:

1. **Feature:** Add `report_auto_hour` (0–23, default 7) as a runtime-tunable setting.
2. **Test gap:** `backup_hour` and `photo_cleanup_hour` lack GET-default, PATCH-persistence, and ops-payload tests. Add them alongside the new field.

---

## Files Touched

| File | Change |
|------|--------|
| `api/services/app_settings.py` | Add `report_auto_hour` property |
| `api/schemas/admin.py` | Add field to `AdminSettingsResponse` and `AdminSettingsUpdate` |
| `api/routers/admin.py` | Include `report_auto_hour` in ops `/reconfigure` payload |
| `ops/scripts/ops_server.py` | Replace hardcoded `7` in crontab template; wire through all four functions |
| `db/migrations/versions/<new>.py` | Alembic migration that seeds the `report_auto_hour` row in the `settings` table (data-only, no schema change) |
| `frontend/js/admin.js` | Add `report_auto_hour` input in the Sistemske nastavitve section |
| `api/tests/test_admin.py` | Add tests for `report_auto_hour`; add missing tests for `backup_hour` and `photo_cleanup_hour` |
| `api/tests/test_app_settings.py` | Add AppSettings unit tests for `report_auto_hour` |

---

## Design Details

### AppSettings (`api/services/app_settings.py`)

New property, identical pattern to `backup_hour`:

```python
@property
def report_auto_hour(self) -> int:
    """Hour of day (0–23) at which the monthly report cron fires."""
    return max(0, min(self._int("report_auto_hour", 7), 23))
```

### Schemas (`api/schemas/admin.py`)

`AdminSettingsResponse`:
```python
report_auto_hour: int
```

`AdminSettingsUpdate`:
```python
report_auto_hour: int | None = Field(None, ge=0, le=23)
```

### Admin router (`api/routers/admin.py`)

The PATCH handler already builds a payload dict sent to ops. Add:
```python
"report_auto_hour": app_settings.report_auto_hour,
```

### Ops server (`ops/scripts/ops_server.py`)

`CRONTAB_TEMPLATE` — replace hardcoded `7`:
```python
"0 {report_hour} {day} * * /app/scripts/monthly_report_send.py --period {period}"
" >> /proc/1/fd/1 2>&1\n"
```

`write_crontab()` — add `report_hour: int` parameter and include in `format()` call and log line.

`fetch_settings_from_db()` — add `'report_auto_hour'` to the `WHERE name IN (...)` list.

`do_POST()` — add:
```python
report_hour = max(0, min(int(payload.get("report_auto_hour", 7)), 23))
```
Pass `report_hour` to `write_crontab()`.

`main()` — add:
```python
report_hour = max(0, min(int(rows.get("report_auto_hour", 7)), 23))
```
Pass `report_hour` to `write_crontab()`.

### DB seed migration

New Alembic revision (data-only). `upgrade()` inserts:
```sql
INSERT INTO settings (name, value, value_type)
VALUES ('report_auto_hour', '7', 'int')
ON CONFLICT (name) DO NOTHING;
```
`downgrade()` deletes the row.

### Frontend (`frontend/js/admin.js`)

In `renderAdmin()`, add a number input for `report_auto_hour` adjacent to the existing `report_auto_day` field. Range 0–23. On save, include in the PATCH payload.

---

## Test Plan

### New tests — `test_admin.py`

**`report_auto_hour` coverage (mirrors existing `backup_hour` style):**

- `test_get_settings_returns_report_hour_default` — GET returns `report_auto_hour == 7`
- `test_patch_settings_saves_report_hour` — PATCH `{"report_auto_hour": 9}` → response has `9`; subsequent GET also returns `9`
- `test_patch_settings_report_hour_boundary_zero` — PATCH `{"report_auto_hour": 0}` → 200
- `test_patch_settings_report_hour_boundary_23` — PATCH `{"report_auto_hour": 23}` → 200
- `test_patch_settings_report_hour_rejects_24` — PATCH `{"report_auto_hour": 24}` → 422
- `test_patch_settings_report_hour_rejects_negative` — PATCH `{"report_auto_hour": -1}` → 422
- `test_patch_settings_ops_payload_includes_report_hour` — ops call_args JSON contains `report_auto_hour`

**Missing coverage for existing fields:**

- `test_get_settings_returns_backup_hour_default` — GET returns `backup_hour == 2`
- `test_patch_settings_saves_backup_hour` — PATCH `{"backup_hour": 4}` persists
- `test_get_settings_returns_photo_cleanup_hour_default` — GET returns `photo_cleanup_hour == 3`
- `test_patch_settings_saves_photo_cleanup_hour` — PATCH `{"photo_cleanup_hour": 5}` persists
- `test_patch_settings_ops_payload_includes_all_fields` — verify ops payload contains `backup_hour`, `photo_cleanup_hour`, `backup_retention_days`, `report_auto_day`, `report_auto_period`

### New tests — `test_app_settings.py`

- `test_appsettings_report_auto_hour_default` — `AppSettings(env, {}).report_auto_hour == 7`
- `test_appsettings_report_auto_hour_from_db` — `AppSettings(env, {"report_auto_hour": "9"}).report_auto_hour == 9`
- `test_appsettings_report_auto_hour_clamped_high` — `AppSettings(env, {"report_auto_hour": "99"}).report_auto_hour == 23`
- `test_appsettings_report_auto_hour_clamped_low` — `AppSettings(env, {"report_auto_hour": "-5"}).report_auto_hour == 0`
