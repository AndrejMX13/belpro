# scripts/setup.sh

> 27 nodes

## Key Concepts

- **Manager (ORM)** (12 connections) — `api/models/manager.py`
- **Base (DeclarativeBase)** (7 connections) — `api/models/base.py`
- **render_volunteer_pdf (Service)** (6 connections) — `api/services/report_pdf.py`
- **render_consent_pdf (Service)** (5 connections) — `api/services/consent_pdf.py`
- **NGOInfo (Dataclass)** (5 connections) — `api/services/report_pdf.py`
- **AppSetting (ORM)** (4 connections) — `api/models/app_setting.py`
- **MonthlyReport (ORM)** (4 connections) — `api/models/monthly_report.py`
- **AppSettings (Service)** (4 connections) — `api/services/app_settings.py`
- **persist_report (Service)** (4 connections) — `api/services/report_storage.py`
- **ErrorLog (ORM)** (3 connections) — `api/models/error_log.py`
- **VolunteerMonthlySummary (Schema)** (3 connections) — `api/schemas/report.py`
- **ReportHistoryItem (Schema)** (3 connections) — `api/schemas/report.py`
- **send_email (Service)** (3 connections) — `api/services/email.py`
- **EvolutionClient (Service)** (3 connections) — `api/services/evolution.py`
- **render_summary_pdf (Service)** (3 connections) — `api/services/report_pdf.py`
- **AdminSettingsResponse (Schema)** (2 connections) — `api/schemas/admin.py`
- **AdminSettingsUpdate (Schema)** (2 connections) — `api/schemas/admin.py`
- **ManagerResponse (Schema)** (2 connections) — `api/schemas/manager.py`
- **ConfigInfoResponse (Schema)** (2 connections) — `api/schemas/manager.py`
- **logo_src (Service)** (2 connections) — `api/services/logo.py`
- **ngo_header_html (Service)** (2 connections) — `api/services/report_pdf.py`
- **ErrorLogCreate (Schema)** (1 connections) — `api/schemas/error_log.py`
- **ErrorLogResponse (Schema)** (1 connections) — `api/schemas/error_log.py`
- **ManagerCreate (Schema)** (1 connections) — `api/schemas/manager.py`
- **ManagerUpdate (Schema)** (1 connections) — `api/schemas/manager.py`
- *... and 2 more nodes in this community*

## Relationships

- [[connections]] (9 shared connections)

## Source Files

- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/manager.py`
- `api/models/monthly_report.py`
- `api/schemas/admin.py`
- `api/schemas/error_log.py`
- `api/schemas/manager.py`
- `api/schemas/report.py`
- `api/services/app_settings.py`
- `api/services/consent_pdf.py`
- `api/services/email.py`
- `api/services/evolution.py`
- `api/services/logo.py`
- `api/services/report_pdf.py`
- `api/services/report_storage.py`

## Audit Trail

- EXTRACTED: 49 (56%)
- INFERRED: 38 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*