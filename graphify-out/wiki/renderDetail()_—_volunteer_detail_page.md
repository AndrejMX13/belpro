# renderDetail() — volunteer detail page

> 42 nodes

## Key Concepts

- **BaseModel** (33 connections)
- **EntryStatus** (20 connections) — `api/models/log_entry.py`
- **volunteer.py** (13 connections) — `api/schemas/volunteer.py`
- **log_entry.py** (7 connections) — `api/schemas/log_entry.py`
- **VolunteerResponse** (6 connections) — `api/schemas/volunteer.py`
- **LogEntryListResponse** (5 connections) — `api/schemas/log_entry.py`
- **EmsoCheckResponse** (5 connections) — `api/schemas/volunteer.py`
- **VolunteerDetailResponse** (5 connections) — `api/schemas/volunteer.py`
- **VolunteerListResponse** (5 connections) — `api/schemas/volunteer.py`
- **AdminSettingsUpdate** (4 connections) — `api/schemas/admin.py`
- **LogEntryCreate** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoBase64Request** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryUpdate** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryBrief** (4 connections) — `api/schemas/volunteer.py`
- **EmsoCheckRequest** (4 connections) — `api/schemas/volunteer.py`
- **VolunteerCreate** (4 connections) — `api/schemas/volunteer.py`
- **LoginRequest** (3 connections) — `api/schemas/auth.py`
- **_normalise_phone()** (3 connections) — `api/schemas/volunteer.py`
- **_normalise_phone_field()** (2 connections) — `api/schemas/volunteer.py`
- **Volunteer diary entry status.  Flows one way only — never backwards.** (1 connections) — `api/models/log_entry.py`
- **Partial update for runtime-tunable settings. Only provided fields are written.** (1 connections) — `api/schemas/admin.py`
- **Body for POST /api/auth/login.** (1 connections) — `api/schemas/auth.py`
- **Pydantic schemas for the LogEntry entity.** (1 connections) — `api/schemas/log_entry.py`
- *... and 17 more nodes in this community*

## Relationships

- [[connections]] (5 shared connections)
- [[BelPro System Specification]] (4 shared connections)
- [[Code: Build Image Media Body]] (4 shared connections)
- [[n8n Set Node Pattern]] (4 shared connections)
- [[n8n Code Node Pattern]] (4 shared connections)
- [[HTTP: GET Pending (Auto)]] (3 shared connections)
- [[009_rename_entry_date_to_work_date.py]] (3 shared connections)
- [[n8n MCP Workflow Management Guide]] (2 shared connections)
- [[GET /api/log-entries/{id}/photos/{photo_id}/file (get_photo_file)]] (2 shared connections)
- [[load_key()]] (1 shared connections)
- [[HTTP: Fetch Media]] (1 shared connections)
- [[Community 315]] (1 shared connections)

## Source Files

- `api/models/log_entry.py`
- `api/schemas/admin.py`
- `api/schemas/auth.py`
- `api/schemas/log_entry.py`
- `api/schemas/volunteer.py`

## Audit Trail

- EXTRACTED: 129 (79%)
- INFERRED: 35 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*