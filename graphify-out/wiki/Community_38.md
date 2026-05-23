# Community 38

> 18 nodes · cohesion 0.18

## Key Concepts

- **EntryStatus** (20 connections) — `api/models/log_entry.py`
- **log_entry_photo.py** (11 connections) — `api/models/log_entry_photo.py`
- **base.py** (10 connections) — `api/models/base.py`
- **__init__.py** (9 connections) — `api/models/__init__.py`
- **log_entry.py** (7 connections) — `api/models/log_entry.py`
- **volunteer.py** (6 connections) — `api/models/volunteer.py`
- **manager.py** (5 connections) — `api/models/manager.py`
- **app_setting.py** (4 connections) — `api/models/app_setting.py`
- **error_log.py** (4 connections) — `api/models/error_log.py`
- **AppSetting ORM model — runtime-tunable key-value configuration.** (1 connections) — `api/models/app_setting.py`
- **SQLAlchemy declarative base shared by all ORM models.** (1 connections) — `api/models/base.py`
- **ErrorLog ORM model — structured record of operational failures.** (1 connections) — `api/models/error_log.py`
- **SQLAlchemy ORM models — import all to ensure they register with Base.metadata.** (1 connections) — `api/models/__init__.py`
- **LogEntryPhoto ORM model — one row per photo, many per log entry.** (1 connections) — `api/models/log_entry_photo.py`
- **A photo attached to a log entry.** (1 connections) — `api/models/log_entry_photo.py`
- **LogEntry ORM model — core audit trail for volunteer work diary entries.** (1 connections) — `api/models/log_entry.py`
- **Volunteer diary entry status.  Flows one way only — never backwards.** (1 connections) — `api/models/log_entry.py`
- **Manager ORM model — one row per deployment (single-tenant).** (1 connections) — `api/models/manager.py`

## Relationships

- [[Community 46]] (9 shared connections)
- [[Community 29]] (7 shared connections)
- [[Community 37]] (6 shared connections)
- [[Community 13]] (3 shared connections)
- [[Community 11]] (3 shared connections)
- [[Community 33]] (2 shared connections)
- [[Community 45]] (1 shared connections)

## Source Files

- `api/models/__init__.py`
- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/models/manager.py`
- `api/models/volunteer.py`

## Audit Trail

- EXTRACTED: 63 (74%)
- INFERRED: 22 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*