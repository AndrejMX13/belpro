# Manager WhatsApp Approval Workflow Design

> 24 nodes

## Key Concepts

- **Settings Table ISS-026 Design** (14 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **Auto Monthly Report Delivery Design** (13 connections) — `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- **update_admin_settings()** (10 connections) — `api/routers/admin.py`
- **admin.py** (9 connections) — `api/routers/admin.py`
- **_notify_ops()** (7 connections) — `api/routers/admin.py`
- **api/routers/admin.py GET and PATCH /api/admin/settings** (7 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **get_admin_settings()** (6 connections) — `api/routers/admin.py`
- **AdminSettingsResponse** (5 connections) — `api/schemas/admin.py`
- **admin.py** (4 connections) — `api/schemas/admin.py`
- **ops/scripts/ops_server.py ThreadingHTTPServer** (4 connections) — `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- **Report Auto-Hour Configurable Setting Design** (4 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Monthly Report Sample porocilo_2026_05-primer** (2 connections) — `docs/images/porocilo_2026_05-primer.pdf`
- **GET /api/admin/settings (get_admin_settings)** (2 connections) — `api/routers/admin.py`
- **PATCH /api/admin/settings (update_admin_settings)** (2 connections) — `api/routers/admin.py`
- **Admin router — runtime-tunable settings management.** (1 connections) — `api/routers/admin.py`
- **POST /reconfigure to ops. Logs and persists error on failure; never raises.** (1 connections) — `api/routers/admin.py`
- **Return current values of all runtime-tunable settings.** (1 connections) — `api/routers/admin.py`
- **Update one or more runtime-tunable settings. Returns updated state.** (1 connections) — `api/routers/admin.py`
- **Pydantic schemas for the admin settings endpoints.** (1 connections) — `api/schemas/admin.py`
- **Current values of all runtime-tunable settings.** (1 connections) — `api/schemas/admin.py`
- **AppSetting ORM Model settings table** (1 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **ops/scripts/monthly_report_send.py Cron Script** (1 connections) — `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- **ops/requirements.txt psycopg2-binary and requests** (1 connections) — `ops/requirements.txt`
- **Volunteer Report Sample Pridni Slavko** (1 connections) — `docs/images/porocilo_Pridni_Slavko_2026_05-primer.pdf`

## Relationships

- [[HTTP: PATCH /notify (Manual)]] (9 shared connections)
- [[Code: Clear State Preklici]] (7 shared connections)
- [[005_report_prefs.py]] (2 shared connections)
- [[Porocila Page - Monthly Reports Overview]] (2 shared connections)
- [[POST /api/logo (upload_logo)]] (2 shared connections)
- [[Evolution API (API Gateway)]] (1 shared connections)
- [[monthly_reports.json]] (1 shared connections)
- [[Community 540]] (1 shared connections)

## Source Files

- `api/routers/admin.py`
- `api/schemas/admin.py`
- `docs/images/porocilo_2026_05-primer.pdf`
- `docs/images/porocilo_Pridni_Slavko_2026_05-primer.pdf`
- `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- `docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md`
- `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- `ops/requirements.txt`

## Audit Trail

- EXTRACTED: 77 (78%)
- INFERRED: 22 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*