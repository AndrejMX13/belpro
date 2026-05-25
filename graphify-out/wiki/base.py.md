# base.py

> 17 nodes · cohesion 0.20

## Key Concepts

- **base.py** (10 connections) — `api/models/base.py`
- **__init__.py** (10 connections) — `api/models/__init__.py`
- **log_entry.py** (7 connections) — `api/models/log_entry.py`
- **volunteer.py** (6 connections) — `api/models/volunteer.py`
- **log_entry_photo.py** (5 connections) — `api/models/log_entry_photo.py`
- **manager.py** (5 connections) — `api/models/manager.py`
- **monthly_report.py** (5 connections) — `api/models/monthly_report.py`
- **app_setting.py** (4 connections) — `api/models/app_setting.py`
- **error_log.py** (4 connections) — `api/models/error_log.py`
- **AppSetting ORM model — runtime-tunable key-value configuration.** (1 connections) — `api/models/app_setting.py`
- **SQLAlchemy declarative base shared by all ORM models.** (1 connections) — `api/models/base.py`
- **ErrorLog ORM model — structured record of operational failures.** (1 connections) — `api/models/error_log.py`
- **LogEntry ORM model — core audit trail for volunteer work diary entries.** (1 connections) — `api/models/log_entry.py`
- **LogEntryPhoto ORM model — one row per photo, many per log entry.** (1 connections) — `api/models/log_entry_photo.py`
- **Manager ORM model — one row per deployment (single-tenant).** (1 connections) — `api/models/manager.py`
- **MonthlyReport ORM model — tracks generated PDF reports.** (1 connections) — `api/models/monthly_report.py`
- **SQLAlchemy ORM models — import all to ensure they register with Base.metadata.** (1 connections) — `api/models/__init__.py`

## Relationships

- [[Base]] (8 shared connections)
- [[BaseModel]] (1 shared connections)
- [[__init__.py]] (1 shared connections)

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

- EXTRACTED: 63 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*