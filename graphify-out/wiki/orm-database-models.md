# ORM Database Models

**Nodes:** 8 | **Cohesion:** 0.393 | **Internal edges:** 11

## Files & Symbols
- **__init__.py** `api\models\__init__.py`
- **base.py** `api\models\base.py`
- **SQLAlchemy declarative base shared by all ORM models.** `api\models\base.py`
- **log_entry.py** `api\models\log_entry.py`
- **log_entry_photo.py** `api\models\log_entry_photo.py`
- **LogEntryPhoto ORM model — one row per photo, many per log entry.** `api\models\log_entry_photo.py`
- **monthly_report.py** `api\models\monthly_report.py`
- **MonthlyReport ORM model — tracks generated PDF reports.** `api\models\monthly_report.py`

## Bridges To Other Communities
### → API Data Models & Schemas (11 edges)
- base.py --contains--> Base [EXTRACTED]
- log_entry.py --contains--> EntryStatus [EXTRACTED]
- log_entry.py --contains--> LogEntry [EXTRACTED]
- log_entry.py --rationale_for--> Pydantic schemas for the LogEntry entity. [EXTRACTED]
- log_entry_photo.py --contains--> LogEntryPhoto [EXTRACTED]
  ... and 6 more
