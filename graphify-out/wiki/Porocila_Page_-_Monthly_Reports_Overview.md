# Porocila Page - Monthly Reports Overview

> 40 nodes

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
- **LogEntryCreate** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoResponse** (4 connections) — `api/schemas/log_entry.py`
- **PhotoBase64Request** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryUpdate** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryBrief** (4 connections) — `api/schemas/volunteer.py`
- **EmsoCheckRequest** (4 connections) — `api/schemas/volunteer.py`
- **VolunteerCreate** (4 connections) — `api/schemas/volunteer.py`
- **AdminSettingsUpdate** (3 connections) — `api/schemas/admin.py`
- **_normalise_phone()** (3 connections) — `api/schemas/volunteer.py`
- **_validate_emso_checksum()** (2 connections) — `api/schemas/volunteer.py`
- **_normalise_phone_field()** (2 connections) — `api/schemas/volunteer.py`
- **Volunteer diary entry status.  Flows one way only — never backwards.** (1 connections) — `api/models/log_entry.py`
- **Partial update for runtime-tunable settings. Only provided fields are written.** (1 connections) — `api/schemas/admin.py`
- **Pydantic schemas for the LogEntry entity.** (1 connections) — `api/schemas/log_entry.py`
- **Fields required to create a new log entry.** (1 connections) — `api/schemas/log_entry.py`
- *... and 15 more nodes in this community*

## Relationships

- [[Evolution API (API Gateway)]] (4 shared connections)
- [[Code: Pripravi Prostovoljca]] (4 shared connections)
- [[DELETE /api/log-entries/{id}/photos/{photo_id} (delete_photo)]] (4 shared connections)
- [[POST /api/managers (create_manager)]] (4 shared connections)
- [[errors.py]] (4 shared connections)
- [[Ima Vnos?]] (3 shared connections)
- [[011_manager_gdpr_clauses.py]] (3 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (2 shared connections)
- [[DevOps Engineer Skill]] (2 shared connections)
- [[005_report_prefs.py]] (1 shared connections)
- [[IF: Should Notify? (Auto)]] (1 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)

## Source Files

- `api/models/log_entry.py`
- `api/schemas/admin.py`
- `api/schemas/log_entry.py`
- `api/schemas/volunteer.py`

## Audit Trail

- EXTRACTED: 124 (78%)
- INFERRED: 36 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*