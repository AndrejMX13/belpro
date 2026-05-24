---
name: project-app-settings
description: AppSetting table and AppSettings service — how runtime-tunable settings work in BelPro
metadata: 
  node_type: memory
  type: project
  originSessionId: d0df1aaf-d949-4f0a-a6a7-98526ac1d9e6
---

BelPro has a generic key-value `settings` table (model: `api/models/app_setting.py`, class `AppSetting`) for runtime-tunable configuration. Each row has `name` (TEXT, unique), `type` (TEXT), and `value` (TEXT, nullable).

The `AppSettings` service (`api/services/app_settings.py`) wraps env-level `Settings` + DB rows, exposing typed properties (`_int`, `_bool`, `_str` helpers). Env is the fallback; DB overrides at runtime.

**Current settings:** `max_photos_per_entry`, `photo_retention_days`, `session_duration_hours`.

**API:** `GET /admin/settings` and `PATCH /admin/settings` in `api/routers/admin.py`, schemas in `api/schemas/admin.py`.

**UI:** Sistemske nastavitve card in `frontend/js/admin.js` (calls `API.admin.getSettings()` / `API.admin.updateSettings()`).

**Why:** Allows the manager to tune operational parameters from the dashboard without touching `.env` or restarting containers.

**How to apply:** When adding a new runtime-tunable setting, follow this pattern:
1. Add a property to `AppSettings` with the appropriate `_int`/`_bool`/`_str` helper
2. Add fields to `AdminSettingsResponse` and `AdminSettingsUpdate` schemas
3. Add a UI field in `admin.js`
4. No migration needed — new rows are inserted by the PATCH endpoint on first save
