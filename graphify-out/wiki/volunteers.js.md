# volunteers.js

> 82 nodes

## Key Concepts

- **test_app_settings.py** (27 connections) — `api/tests/test_app_settings.py`
- **get_settings()** (26 connections) — `api/core/settings.py`
- **health_detailed()** (5 connections) — `api/main.py`
- **Settings** (5 connections) — `api/core/settings.py`
- **test_appsettings_uses_db_int_value()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_falls_back_to_env_when_row_missing()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_passthrough_to_env()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_parses_truthy_strings()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_parses_falsy_strings()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_falls_back_to_default()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_returns_db_value()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_falls_back_to_default()** (5 connections) — `api/tests/test_app_settings.py`
- **test_photo_upload_respects_db_max_photos_setting()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_default()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_from_db()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_high()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_low()** (5 connections) — `api/tests/test_app_settings.py`
- **test_photo_upload_base64_respects_db_max_photos_setting()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_evolution_instance_name_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_evolution_instance_name_from_db()** (4 connections) — `api/tests/test_app_settings.py`
- **settings.py** (3 connections) — `api/core/settings.py`
- **test_get_admin_settings_returns_seeded_defaults()** (3 connections) — `api/tests/test_app_settings.py`
- **test_get_admin_settings_requires_auth()** (3 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_updates_single_field()** (3 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_get_reflects_change()** (3 connections) — `api/tests/test_app_settings.py`
- *... and 57 more nodes in this community*

## Relationships

- [[n8n MCP Workflow Management Guide]] (16 shared connections)
- [[load_key()]] (6 shared connections)
- [[Normalise phone to bare E.164 digits, pass through None.]] (1 shared connections)
- [[BelPro README (English)]] (1 shared connections)
- [[DELETE /api/log-entries/{id}/photos/{photo_id} (delete_photo)]] (1 shared connections)
- [[list_pending_entries.py]] (1 shared connections)
- [[n8n Set Node Pattern]] (1 shared connections)
- [[Community 406]] (1 shared connections)
- [[001_initial_schema.py]] (1 shared connections)

## Source Files

- `api/core/settings.py`
- `api/main.py`
- `api/tests/test_app_settings.py`

## Audit Trail

- EXTRACTED: 169 (74%)
- INFERRED: 58 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*