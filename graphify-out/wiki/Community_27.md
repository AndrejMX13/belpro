# Community 27

> 24 nodes · cohesion 0.08

## Key Concepts

- **test_app_settings.py** (20 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_from_db()** (6 connections) — `api/tests/test_app_settings.py`
- **test_get_admin_settings_requires_auth()** (2 connections) — `api/tests/test_app_settings.py`
- **test_get_admin_settings_returns_seeded_defaults()** (2 connections) — `api/tests/test_app_settings.py`
- **test_login_cookie_max_age_reflects_db_session_duration()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_get_reflects_change()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_rejects_negative()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_rejects_zero()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_requires_auth()** (2 connections) — `api/tests/test_app_settings.py`
- **test_patch_admin_settings_updates_single_field()** (2 connections) — `api/tests/test_app_settings.py`
- **test_settings_table_seeded()** (2 connections) — `api/tests/test_app_settings.py`
- **Tests for the settings table, AppSettings service, and admin settings router.** (1 connections) — `api/tests/test_app_settings.py`
- **GET /api/admin/settings returns the seeded default values.** (1 connections) — `api/tests/test_app_settings.py`
- **Migration seeds the three default settings rows.** (1 connections) — `api/tests/test_app_settings.py`
- **Unauthenticated request is rejected.** (1 connections) — `api/tests/test_app_settings.py`
- **PATCH updates a single field; others are unchanged.** (1 connections) — `api/tests/test_app_settings.py`
- **Subsequent GET reflects a PATCHed value.** (1 connections) — `api/tests/test_app_settings.py`
- **PATCH rejects zero (ge=1 constraint).** (1 connections) — `api/tests/test_app_settings.py`
- **PATCH rejects negative values.** (1 connections) — `api/tests/test_app_settings.py`
- **Unauthenticated PATCH is rejected.** (1 connections) — `api/tests/test_app_settings.py`
- **Login sets a cookie whose max_age matches the session_duration_hours DB setting.** (1 connections) — `api/tests/test_app_settings.py`
- **report_auto_hour reads the DB value when present.** (1 connections) — `api/tests/test_app_settings.py`
- **report_auto_hour clamps values above 23 to 23.** (1 connections) — `api/tests/test_app_settings.py`
- **report_auto_hour clamps negative values to 0.** (1 connections) — `api/tests/test_app_settings.py`

## Relationships

- [[Community 36]] (9 shared connections)
- [[Community 25]] (1 shared connections)
- [[Community 23]] (1 shared connections)

## Source Files

- `api/tests/test_app_settings.py`

## Audit Trail

- EXTRACTED: 55 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*