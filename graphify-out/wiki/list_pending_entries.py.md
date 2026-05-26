# list_pending_entries.py

> 19 nodes

## Key Concepts

- **errors.py** (6 connections) — `api/routers/errors.py`
- **error_log.py** (4 connections) — `api/schemas/error_log.py`
- **_require_internal_key()** (3 connections) — `api/routers/errors.py`
- **write_error()** (3 connections) — `api/routers/errors.py`
- **unacknowledged_count()** (3 connections) — `api/routers/errors.py`
- **ErrorLogCreate** (3 connections) — `api/schemas/error_log.py`
- **ErrorLogResponse** (3 connections) — `api/schemas/error_log.py`
- **UnacknowledgedCountResponse** (3 connections) — `api/schemas/error_log.py`
- **list_errors()** (2 connections) — `api/routers/errors.py`
- **acknowledge_error()** (2 connections) — `api/routers/errors.py`
- **Error log router — write endpoint for internal services, read endpoints for mana** (1 connections) — `api/routers/errors.py`
- **Validate X-Internal-Key header against API_SECRET_KEY.** (1 connections) — `api/routers/errors.py`
- **Record an operational failure. Called by API exception handlers, n8n, and the op** (1 connections) — `api/routers/errors.py`
- **Return count of unacknowledged errors. Used by nav badge.** (1 connections) — `api/routers/errors.py`
- **List error log entries, newest first. Optionally filter to unacknowledged only.** (1 connections) — `api/routers/errors.py`
- **Mark an error as acknowledged (read by manager).** (1 connections) — `api/routers/errors.py`
- **Pydantic schemas for the error_log endpoint.** (1 connections) — `api/schemas/error_log.py`
- **Payload sent by internal services (API, n8n, ops sidecar).** (1 connections) — `api/schemas/error_log.py`
- **Single error log row returned to the dashboard.** (1 connections) — `api/schemas/error_log.py`

## Relationships

- [[test_app_settings.py]] (3 shared connections)
- [[volunteers.js]] (1 shared connections)
- [[VolunteerUpdate]] (1 shared connections)

## Source Files

- `api/routers/errors.py`
- `api/schemas/error_log.py`

## Audit Trail

- EXTRACTED: 37 (90%)
- INFERRED: 4 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*