# Volunteer (ORM)

> 51 nodes · cohesion 0.06

## Key Concepts

- **Volunteer (ORM)** (25 connections) — `api/models/volunteer.py`
- **LogEntry (ORM)** (22 connections) — `api/models/log_entry.py`
- **EntryStatus (Enum)** (15 connections) — `api/models/log_entry.py`
- **Manager (ORM)** (12 connections) — `api/models/manager.py`
- **LogEntryResponse (Schema)** (11 connections) — `api/schemas/log_entry.py`
- **VolunteerResponse (Schema)** (9 connections) — `api/schemas/volunteer.py`
- **LogEntryPhoto (ORM)** (8 connections) — `api/models/log_entry_photo.py`
- **Base (DeclarativeBase)** (7 connections) — `api/models/base.py`
- **render_volunteer_pdf (Service)** (6 connections) — `api/services/report_pdf.py`
- **AnalyticsSummary (Schema)** (5 connections) — `api/schemas/analytics.py`
- **VolunteerCreate (Schema)** (5 connections) — `api/schemas/volunteer.py`
- **render_consent_pdf (Service)** (5 connections) — `api/services/consent_pdf.py`
- **NGOInfo (Dataclass)** (5 connections) — `api/services/report_pdf.py`
- **AppSetting (ORM)** (4 connections) — `api/models/app_setting.py`
- **MonthlyReport (ORM)** (4 connections) — `api/models/monthly_report.py`
- **PhotoResponse (Schema)** (4 connections) — `api/schemas/log_entry.py`
- **VolunteerDetailResponse (Schema)** (4 connections) — `api/schemas/volunteer.py`
- **AppSettings (Service)** (4 connections) — `api/services/app_settings.py`
- **persist_report (Service)** (4 connections) — `api/services/report_storage.py`
- **ErrorLog (ORM)** (3 connections) — `api/models/error_log.py`
- **LogEntryCreate (Schema)** (3 connections) — `api/schemas/log_entry.py`
- **VolunteerMonthlySummary (Schema)** (3 connections) — `api/schemas/report.py`
- **ReportHistoryItem (Schema)** (3 connections) — `api/schemas/report.py`
- **LogEntryBrief (Schema)** (3 connections) — `api/schemas/volunteer.py`
- **send_email (Service)** (3 connections) — `api/services/email.py`
- *... and 26 more nodes in this community*

## Relationships

- [[load_key()]] (26 shared connections)
- [[log_entries.py]] (16 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (7 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (6 shared connections)
- [[GET /api/log-entries (list_log_entries)]] (3 shared connections)
- [[PATCH /api/log-entries/{id}/notify (notify_log_entry)]] (3 shared connections)
- [[get_log_entry()]] (2 shared connections)

## Source Files

- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/models/manager.py`
- `api/models/monthly_report.py`
- `api/models/volunteer.py`
- `api/schemas/admin.py`
- `api/schemas/analytics.py`
- `api/schemas/error_log.py`
- `api/schemas/log_entry.py`
- `api/schemas/manager.py`
- `api/schemas/report.py`
- `api/schemas/volunteer.py`
- `api/services/app_settings.py`
- `api/services/consent_pdf.py`
- `api/services/email.py`
- `api/services/encryption.py`
- `api/services/evolution.py`

## Audit Trail

- EXTRACTED: 155 (70%)
- INFERRED: 66 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*