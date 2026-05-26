# VolunteerUpdate

> 35 nodes

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
- **AppSetting** (6 connections) — `api/models/app_setting.py`
- **MonthlyReport** (6 connections) — `api/models/monthly_report.py`
- **volunteer.py** (6 connections) — `api/models/volunteer.py`
- **log_entry_photo.py** (5 connections) — `api/models/log_entry_photo.py`
- **manager.py** (5 connections) — `api/models/manager.py`
- **monthly_report.py** (5 connections) — `api/models/monthly_report.py`
- **app_setting.py** (4 connections) — `api/models/app_setting.py`
- **error_log.py** (4 connections) — `api/models/error_log.py`
- **AppSetting ORM model — runtime-tunable key-value configuration.** (1 connections) — `api/models/app_setting.py`
- **One row per named setting. All values stored as TEXT.** (1 connections) — `api/models/app_setting.py`
- **DeclarativeBase** (1 connections)
- **SQLAlchemy declarative base shared by all ORM models.** (1 connections) — `api/models/base.py`
- **Declarative base — import and subclass in every model.** (1 connections) — `api/models/base.py`
- **ErrorLog ORM model — structured record of operational failures.** (1 connections) — `api/models/error_log.py`
- **One row per operational failure. Written by API, n8n, and ops sidecar.** (1 connections) — `api/models/error_log.py`
- *... and 10 more nodes in this community*

## Relationships

- [[test_app_settings.py]] (4 shared connections)
- [[n8n MCP Workflow Management Guide]] (3 shared connections)
- [[errors.py]] (3 shared connections)
- [[list_pending_entries.py]] (1 shared connections)
- [[n8n Set Node Pattern]] (1 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (1 shared connections)
- [[Community 406]] (1 shared connections)
- [[ops_server.py]] (1 shared connections)
- [[log_entries.py]] (1 shared connections)
- [[Community 405]] (1 shared connections)

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

- EXTRACTED: 103 (73%)
- INFERRED: 38 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*