# Base

> 18 nodes · cohesion 0.18

## Key Concepts

- **Base** (11 connections) — `api/models/base.py`
- **Volunteer** (9 connections) — `api/models/volunteer.py`
- **LogEntryPhoto** (8 connections) — `api/models/log_entry_photo.py`
- **Base** (7 connections)
- **ErrorLog** (7 connections) — `api/models/error_log.py`
- **LogEntry** (7 connections) — `api/models/log_entry.py`
- **Manager** (7 connections) — `api/models/manager.py`
- **AppSetting** (6 connections) — `api/models/app_setting.py`
- **MonthlyReport** (6 connections) — `api/models/monthly_report.py`
- **One row per named setting. All values stored as TEXT.** (1 connections) — `api/models/app_setting.py`
- **DeclarativeBase** (1 connections)
- **Declarative base — import and subclass in every model.** (1 connections) — `api/models/base.py`
- **One row per operational failure. Written by API, n8n, and ops sidecar.** (1 connections) — `api/models/error_log.py`
- **Individual work diary entry submitted by a volunteer.** (1 connections) — `api/models/log_entry.py`
- **A photo attached to a log entry.** (1 connections) — `api/models/log_entry_photo.py`
- **NGO manager.  Single row expected per deployment.** (1 connections) — `api/models/manager.py`
- **Tracks generated PDF reports for audit and re-delivery purposes.      volunteer_** (1 connections) — `api/models/monthly_report.py`
- **Registered volunteer.  Soft-deleted via active=False — never hard-deleted.** (1 connections) — `api/models/volunteer.py`

## Relationships

- [[base.py]] (8 shared connections)
- [[BaseModel]] (3 shared connections)
- [[update_admin_settings()]] (2 shared connections)
- [[log_entries.py]] (2 shared connections)
- [[AppSettings]] (1 shared connections)
- [[errors.py]] (1 shared connections)
- [[send_monthly_reports()]] (1 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (1 shared connections)
- [[managers.py]] (1 shared connections)
- [[conftest.py]] (1 shared connections)
- [[persist_report()]] (1 shared connections)
- [[load_key()]] (1 shared connections)

## Source Files

- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/models/manager.py`
- `api/models/monthly_report.py`
- `api/models/volunteer.py`

## Audit Trail

- EXTRACTED: 40 (52%)
- INFERRED: 37 (48%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*