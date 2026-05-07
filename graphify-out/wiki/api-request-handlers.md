# API Request Handlers

**Nodes:** 33 | **Cohesion:** 0.072 | **Internal edges:** 38

## Files & Symbols
- **str** `(no file)`
- **Exception** `(no file)`
- **BaseHTTPRequestHandler** `(no file)`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\log_entries.py` — 14 symbols (e.g. log_entries.py, _notify_volunteer_email(), ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\services\email.py` — 4 symbols (e.g. email.py, send_email(), ...)
- `D:\Andrej\vsCode-workspace\BelPro\whisper\transcribe.py` — 12 symbols (e.g. transcribe.py, _Handler, ...)

## Bridges To Other Communities
### → API Data Models & Schemas (21 edges)
- EntryStatus --inherits--> str [EXTRACTED]
- log_entries.py --rationale_for--> Log entries CRUD router — volunteer work diary entries. [EXTRACTED]
- _notify_volunteer_email() --rationale_for--> Best-effort email notification to volunteer after approve/reject.      Silentl [EXTRACTED]
- _extract_exif() --rationale_for--> Extract timestamp and GPS from image EXIF. All best-effort — never raises. [EXTRACTED]
- list_log_entries() --rationale_for--> List log entries with optional filters, sorting, and pagination. [EXTRACTED]
  ... and 16 more
### → Analytics Engine (2 edges)
- str --calls--> create_manager() [INFERRED]
- str --calls--> update_manager() [INFERRED]
### → Encryption & Volunteer CRUD (1 edges)
- str --calls--> create_volunteer() [INFERRED]
### → Migration Config & Settings (1 edges)
- get_settings() --calls--> _notify_volunteer_email() [INFERRED]
### → PDF Report Generation (2 edges)
- str --calls--> send_monthly_reports() [INFERRED]
- send_monthly_reports() --calls--> send_email() [INFERRED]
