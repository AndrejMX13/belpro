# BaseModel

> 27 nodes · cohesion 0.11

## Key Concepts

- **BaseModel** (33 connections)
- **EntryStatus** (20 connections) — `api/models/log_entry.py`
- **log_entry.py** (7 connections) — `api/schemas/log_entry.py`
- **LogEntryListResponse** (5 connections) — `api/schemas/log_entry.py`
- **EmsoCheckResponse** (5 connections) — `api/schemas/volunteer.py`
- **VolunteerListResponse** (5 connections) — `api/schemas/volunteer.py`
- **LogEntryCreate** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoBase64Request** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryUpdate** (4 connections) — `api/schemas/log_entry.py`
- **EmsoCheckRequest** (4 connections) — `api/schemas/volunteer.py`
- **VolunteerCreate** (4 connections) — `api/schemas/volunteer.py`
- **AdminSettingsUpdate** (3 connections) — `api/schemas/admin.py`
- **Volunteer diary entry status.  Flows one way only — never backwards.** (1 connections) — `api/models/log_entry.py`
- **Partial update for runtime-tunable settings. Only provided fields are written.** (1 connections) — `api/schemas/admin.py`
- **Pydantic schemas for the LogEntry entity.** (1 connections) — `api/schemas/log_entry.py`
- **Fields required to create a new log entry.** (1 connections) — `api/schemas/log_entry.py`
- **Full log entry returned by the API.** (1 connections) — `api/schemas/log_entry.py`
- **A single photo attached to a log entry.** (1 connections) — `api/schemas/log_entry.py`
- **Base64-encoded photo upload — used by n8n workflows.** (1 connections) — `api/schemas/log_entry.py`
- **Editable fields — blocked once the entry is approved.** (1 connections) — `api/schemas/log_entry.py`
- **Paginated log entry list.** (1 connections) — `api/schemas/log_entry.py`
- **Plaintext EMŠO submitted for duplicate check before creating a volunteer.** (1 connections) — `api/schemas/volunteer.py`
- **Result of an EMŠO duplicate check.** (1 connections) — `api/schemas/volunteer.py`
- *... and 2 more nodes in this community*

## Relationships

- [[volunteer.py]] (9 shared connections)
- [[analytics_summary()]] (4 shared connections)
- [[manager.py]] (4 shared connections)
- [[get_report_history()]] (4 shared connections)
- [[Base]] (3 shared connections)
- [[errors.py]] (3 shared connections)
- [[VolunteerUpdate]] (2 shared connections)
- [[update_admin_settings()]] (2 shared connections)
- [[test_auth.py]] (2 shared connections)
- [[load_key()]] (2 shared connections)
- [[base.py]] (1 shared connections)
- [[str]] (1 shared connections)

## Source Files

- `api/models/log_entry.py`
- `api/schemas/admin.py`
- `api/schemas/log_entry.py`
- `api/schemas/volunteer.py`

## Audit Trail

- EXTRACTED: 89 (75%)
- INFERRED: 30 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*