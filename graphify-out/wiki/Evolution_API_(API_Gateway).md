# Evolution API (API Gateway)

> 33 nodes

## Key Concepts

- **Base** (11 connections) — `api/models/base.py`
- **base.py** (10 connections) — `api/models/base.py`
- **__init__.py** (10 connections) — `api/models/__init__.py`
- **Volunteer** (9 connections) — `api/models/volunteer.py`
- **LogEntryPhoto** (8 connections) — `api/models/log_entry_photo.py`
- **Base** (7 connections)
- **ErrorLog** (7 connections) — `api/models/error_log.py`
- **log_entry.py** (7 connections) — `api/models/log_entry.py`
- **LogEntry** (7 connections) — `api/models/log_entry.py`
- **Manager** (7 connections) — `api/models/manager.py`
- **MonthlyReport** (6 connections) — `api/models/monthly_report.py`
- **volunteer.py** (6 connections) — `api/models/volunteer.py`
- **log_entry_photo.py** (5 connections) — `api/models/log_entry_photo.py`
- **manager.py** (5 connections) — `api/models/manager.py`
- **monthly_report.py** (5 connections) — `api/models/monthly_report.py`
- **app_setting.py** (4 connections) — `api/models/app_setting.py`
- **error_log.py** (4 connections) — `api/models/error_log.py`
- **AppSetting ORM model — runtime-tunable key-value configuration.** (1 connections) — `api/models/app_setting.py`
- **DeclarativeBase** (1 connections)
- **SQLAlchemy declarative base shared by all ORM models.** (1 connections) — `api/models/base.py`
- **Declarative base — import and subclass in every model.** (1 connections) — `api/models/base.py`
- **ErrorLog ORM model — structured record of operational failures.** (1 connections) — `api/models/error_log.py`
- **One row per operational failure. Written by API, n8n, and ops sidecar.** (1 connections) — `api/models/error_log.py`
- **LogEntry ORM model — core audit trail for volunteer work diary entries.** (1 connections) — `api/models/log_entry.py`
- **Individual work diary entry submitted by a volunteer.** (1 connections) — `api/models/log_entry.py`
- *... and 8 more nodes in this community*

## Relationships

- [[Porocila Page - Monthly Reports Overview]] (4 shared connections)
- [[HTTP: PATCH /notify (Manual)]] (3 shared connections)
- [[BelPro Project Memory Public Index]] (3 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (1 shared connections)
- [[011_manager_gdpr_clauses.py]] (1 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (1 shared connections)
- [[IF: Should Notify? (Auto)]] (1 shared connections)
- [[Community 405]] (1 shared connections)
- [[analytics_summary()]] (1 shared connections)
- [[errors.py]] (1 shared connections)
- [[Community 362]] (1 shared connections)

## Source Files

- `api/models/__init__.py`
- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/models/manager.py`
- `api/models/monthly_report.py`
- `api/models/volunteer.py`

## Audit Trail

- EXTRACTED: 99 (74%)
- INFERRED: 35 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*