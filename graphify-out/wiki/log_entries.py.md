# log_entries.py

> 36 nodes

## Key Concepts

- **test_admin.py** (19 connections) — `api/tests/test_admin.py`
- **test_get_settings_returns_report_defaults()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_saves_report_fields()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_notifies_ops()** (2 connections) — `api/tests/test_admin.py`
- **test_get_settings_returns_backup_retention_default()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_saves_backup_retention()** (2 connections) — `api/tests/test_admin.py`
- **test_get_settings_returns_report_hour_default()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_saves_report_hour()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_report_hour_boundary_zero()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_report_hour_boundary_23()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_report_hour_rejects_24()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_report_hour_rejects_negative()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_ops_payload_includes_report_hour()** (2 connections) — `api/tests/test_admin.py`
- **test_get_settings_returns_backup_hour_default()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_saves_backup_hour()** (2 connections) — `api/tests/test_admin.py`
- **test_get_settings_returns_photo_cleanup_hour_default()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_saves_photo_cleanup_hour()** (2 connections) — `api/tests/test_admin.py`
- **test_patch_settings_ops_payload_includes_all_fields()** (2 connections) — `api/tests/test_admin.py`
- **Tests for report auto-delivery settings.** (1 connections) — `api/tests/test_admin.py`
- **GET /api/admin/settings returns defaults for report_auto_day and report_auto_per** (1 connections) — `api/tests/test_admin.py`
- **PATCH /api/admin/settings persists report_auto_day and report_auto_period.** (1 connections) — `api/tests/test_admin.py`
- **PATCH /api/admin/settings calls ops /reconfigure with updated values.** (1 connections) — `api/tests/test_admin.py`
- **GET /api/admin/settings returns default backup_retention_days of 30.** (1 connections) — `api/tests/test_admin.py`
- **PATCH /api/admin/settings persists backup_retention_days.** (1 connections) — `api/tests/test_admin.py`
- **GET /api/admin/settings returns report_auto_hour default of 7.** (1 connections) — `api/tests/test_admin.py`
- *... and 11 more nodes in this community*

## Relationships

- [[Maximum photos allowed per log entry.]] (1 shared connections)

## Source Files

- `api/tests/test_admin.py`

## Audit Trail

- EXTRACTED: 71 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*