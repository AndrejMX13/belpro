# API Data Models & Schemas

**Nodes:** 115 | **Cohesion:** 0.093 | **Internal edges:** 608

## Files & Symbols
- **BaseSettings** `(no file)`
- **DeclarativeBase** `(no file)`
- **Base** `(no file)`
- **Settings** `D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py`
- **All configuration for the Belpro API service.      Values are read from the proc** `D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py`
- **Manager** `D:\Andrej\vsCode-workspace\BelPro\api\models\manager.py`
- **NGO manager.  Single row expected per deployment.** `D:\Andrej\vsCode-workspace\BelPro\api\models\manager.py`
- **Volunteer** `D:\Andrej\vsCode-workspace\BelPro\api\models\volunteer.py`
- **Registered volunteer.  Soft-deleted via active=False — never hard-deleted.** `D:\Andrej\vsCode-workspace\BelPro\api\models\volunteer.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\log_entries.py` — 14 symbols (e.g. Log entries CRUD router — volunteer work diary entries., Best-effort email notification to volunteer after approve/reject.      Silentl, ...)
- **Generate monthly PDFs and send them via email.      Defaults to the current ca** `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\volunteers.py` — 11 symbols (e.g. Volunteers CRUD router., Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object., ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py` — 30 symbols (e.g. volunteer.py, _normalise_phone(), ...)
- **SmtpNotConfiguredError** `D:\Andrej\vsCode-workspace\BelPro\api\services\email.py`
- **Raised when the manager has not configured SMTP.** `D:\Andrej\vsCode-workspace\BelPro\api\services\email.py`
- **SQLAlchemy ORM models — import all to ensure they register with Base.metadata.** `api\models\__init__.py`
- **Base** `api\models\base.py`
- **Declarative base — import and subclass in every model.** `api\models\base.py`
- `api\models\log_entry.py` — 4 symbols (e.g. EntryStatus, LogEntry, ...)
- **LogEntryPhoto** `api\models\log_entry_photo.py`
- **A photo attached to a log entry.** `api\models\log_entry_photo.py`
- **MonthlyReport** `api\models\monthly_report.py`
- **Tracks generated PDF reports for audit and re-delivery purposes.      volunteer_** `api\models\monthly_report.py`
- `api\routers\log_entries.py` — 10 symbols (e.g. Extract timestamp and GPS from image EXIF. All best-effort — never raises., List log entries with optional filters, sorting, and pagination., ...)
- `api\routers\volunteers.py` — 9 symbols (e.g. Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object., Same as _to_response but includes sorted log_entries and computed hours for the, ...)
- `api\schemas\log_entry.py` — 12 symbols (e.g. Pydantic schemas for the LogEntry entity., log_entry.py, ...)
- `api\schemas\volunteer.py` — 6 symbols (e.g. Paginated volunteer list., Plaintext EMŠO submitted for duplicate check before creating a volunteer., ...)

## Bridges To Other Communities
### → API Authentication (4 edges)
- Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw --uses--> Settings [INFERRED]
- FastAPI dependency — rejects requests without the correct manager password. --uses--> Settings [INFERRED]
- Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw --uses--> Manager [INFERRED]
- FastAPI dependency — rejects requests without the correct manager password. --uses--> Manager [INFERRED]
### → API Request Handlers (21 edges)
- EntryStatus --inherits--> str [EXTRACTED]
- LogEntry --calls--> create_log_entry() [INFERRED]
- LogEntryPhoto --calls--> upload_photo() [INFERRED]
- log_entries.py --rationale_for--> Log entries CRUD router — volunteer work diary entries. [EXTRACTED]
- _notify_volunteer_email() --rationale_for--> Best-effort email notification to volunteer after approve/reject.      Silentl [EXTRACTED]
  ... and 16 more
### → Analytics Engine (42 edges)
- Settings --uses--> Managers router — single-manager setup and profile. [INFERRED]
- Settings --uses--> Return the single manager profile, or 404 if setup has not been completed. [INFERRED]
- Settings --uses--> Seed the manager profile (first-time setup). Returns 409 if already configured. [INFERRED]
- Settings --uses--> Update manager and/or NGO fields.  Only provided (non-None) fields are written. [INFERRED]
- Settings --uses--> Return non-secret config status for the settings UI. [INFERRED]
  ... and 37 more
### → Encryption & Volunteer CRUD (16 edges)
- Volunteer --calls--> create_volunteer() [INFERRED]
- volunteers.py --rationale_for--> Volunteers CRUD router. [EXTRACTED]
- _to_response() --rationale_for--> Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object. [EXTRACTED]
- _to_detail_response() --rationale_for--> Same as _to_response but includes sorted log_entries and computed hours for the [EXTRACTED]
- list_volunteers() --rationale_for--> List volunteers with optional filters, sorting, and pagination. [EXTRACTED]
  ... and 11 more
### → Migration Config & Settings (2 edges)
- settings.py --contains--> Settings [EXTRACTED]
- Settings --calls--> get_settings() [EXTRACTED]
### → ORM Database Models (11 edges)
- base.py --contains--> Base [EXTRACTED]
- Base --uses--> LogEntryPhoto ORM model — one row per photo, many per log entry. [INFERRED]
- Base --uses--> MonthlyReport ORM model — tracks generated PDF reports. [INFERRED]
- log_entry.py --contains--> EntryStatus [EXTRACTED]
- log_entry.py --contains--> LogEntry [EXTRACTED]
  ... and 6 more
### → PDF Report Generation (36 edges)
- EntryStatus --uses--> Reports router — monthly aggregation and PDF export endpoints. [INFERRED]
- EntryStatus --uses--> Return per-volunteer totals of approved entries for the given year/month. [INFERRED]
- EntryStatus --uses--> Run the monthly aggregation query and return per-volunteer summaries. [INFERRED]
- EntryStatus --uses--> Generate a monthly PDF report for one volunteer or all active volunteers. [INFERRED]
- EntryStatus --uses--> Generate monthly PDFs and send them via email.      Defaults to the current ca [INFERRED]
  ... and 31 more
