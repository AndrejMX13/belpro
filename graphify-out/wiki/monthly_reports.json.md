# monthly_reports.json

> 48 nodes

## Key Concepts

- **get_settings()** (24 connections) — `api/core/settings.py`
- **test_app_settings.py** (24 connections) — `api/tests/test_app_settings.py`
- **health_detailed()** (4 connections) — `api/main.py`
- **test_appsettings_uses_db_int_value()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_falls_back_to_env_when_row_missing()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_passthrough_to_env()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_parses_truthy_strings()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_parses_falsy_strings()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_returns_db_value()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_from_db()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_high()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_low()** (4 connections) — `api/tests/test_app_settings.py`
- **test_settings_table_seeded()** (2 connections) — `api/tests/test_app_settings.py`
- **test_get_admin_settings_returns_seeded_defaults()** (2 connections) — `api/tests/test_app_settings.py`
- **test_get_admin_settings_requires_auth()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_updates_single_field()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_get_reflects_change()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_rejects_zero()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_rejects_negative()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_requires_auth()** (2 connections) — `api/tests/test_app_settings.py`
- **test_login_cookie_max_age_reflects_db_session_duration()** (2 connections) — `api/tests/test_app_settings.py`
- **Per-service health status for the manager dashboard widget.** (1 connections) — `api/main.py`
- *... and 23 more nodes in this community*

## Relationships

- [[HTTP: PATCH /notify (Manual)]] (12 shared connections)
- [[path]] (3 shared connections)
- [[HTTP: GET Volunteer (Mgr)]] (2 shared connections)
- [[Community 589]] (2 shared connections)
- [[005_report_prefs.py]] (1 shared connections)
- [[DELETE /api/logo (remove_logo)]] (1 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (1 shared connections)
- [[011_manager_gdpr_clauses.py]] (1 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (1 shared connections)
- [[Community 405]] (1 shared connections)
- [[settings.local.json]] (1 shared connections)

## Source Files

- `api/core/settings.py`
- `api/main.py`
- `api/tests/test_app_settings.py`

## Audit Trail

- EXTRACTED: 95 (67%)
- INFERRED: 47 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*