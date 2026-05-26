# n8n MCP Workflow Management Guide

> 57 nodes

## Key Concepts

- **AppSettings** (28 connections) — `api/services/app_settings.py`
- **app_settings.py** (17 connections) — `api/services/app_settings.py`
- **Settings Table ISS-026 Design** (14 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **Auto Monthly Report Delivery Design** (13 connections) — `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- **update_admin_settings()** (11 connections) — `api/routers/admin.py`
- **._int()** (11 connections) — `api/services/app_settings.py`
- **AppSettings Central Configuration Authority** (10 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **admin.py** (9 connections) — `api/routers/admin.py`
- **_notify_ops()** (7 connections) — `api/routers/admin.py`
- **get_app_settings()** (7 connections) — `api/services/app_settings.py`
- **api/routers/admin.py GET and PATCH /api/admin/settings** (7 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **get_admin_settings()** (6 connections) — `api/routers/admin.py`
- **download_consent_pdf()** (5 connections) — `api/routers/documents.py`
- **AdminSettingsResponse** (5 connections) — `api/schemas/admin.py`
- **._str()** (5 connections) — `api/services/app_settings.py`
- **documents.py** (4 connections) — `api/routers/documents.py`
- **admin.py** (4 connections) — `api/schemas/admin.py`
- **photo_retention_days()** (4 connections) — `api/services/app_settings.py`
- **session_duration_hours()** (4 connections) — `api/services/app_settings.py`
- **.__getattr__()** (4 connections) — `api/services/app_settings.py`
- **ops/scripts/ops_server.py ThreadingHTTPServer** (4 connections) — `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- **Report Auto-Hour Configurable Setting Design** (4 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **._bool()** (3 connections) — `api/services/app_settings.py`
- **max_photos_per_entry()** (3 connections) — `api/services/app_settings.py`
- **report_auto_day()** (3 connections) — `api/services/app_settings.py`
- *... and 32 more nodes in this community*

## Relationships

- [[volunteers.js]] (16 shared connections)
- [[VolunteerUpdate]] (3 shared connections)
- [[load_key()]] (2 shared connections)
- [[GDPR Consent PDF (Dogovor o prostovoljstvu)]] (2 shared connections)
- [[test_app_settings.py]] (2 shared connections)
- [[PATCH /api/log-entries/{id} (update_log_entry)]] (2 shared connections)
- [[Community 325]] (1 shared connections)
- [[Community 544]] (1 shared connections)

## Source Files

- `api/routers/admin.py`
- `api/routers/documents.py`
- `api/schemas/admin.py`
- `api/services/app_settings.py`
- `docs/images/porocilo_2026_05-primer.pdf`
- `docs/images/porocilo_Pridni_Slavko_2026_05-primer.pdf`
- `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- `ops/requirements.txt`

## Audit Trail

- EXTRACTED: 193 (82%)
- INFERRED: 42 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*