# Volunteer (ORM)

> 51 nodes

## Key Concepts

- **volunteer_entry.json** (34 connections) — `n8n/workflows/volunteer_entry.json`
- **BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)** (15 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/managers/me (get_manager)** (9 connections) — `api/routers/managers.py`
- **PATCH /api/log-entries/{id}/notify (notify_log_entry)** (8 connections) — `api/routers/log_entries.py`
- **Shared LogEntry Data Structure (volunteer_id, work_date, hours, activity_description, location, status, raw_transcript)** (8 connections) — `api/routers/log_entries.py`
- **GET /api/volunteers/{id} (get_volunteer)** (7 connections) — `api/routers/volunteers.py`
- **POST /api/log-entries (create_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **DELETE /api/log-entries/{id} (delete_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **POST /api/log-entries/{id}/confirm (confirm_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **GET /api/volunteers (list_volunteers)** (4 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers?search_by=phone (Lookup Volunteer by Phone)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries (Create Entry)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/managers/me (Lookup Manager in Volunteer Workflow)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/log-entries/{id} (get_log_entry)** (3 connections) — `api/routers/log_entries.py`
- **staticData** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **pinData** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries/{id}/confirm (Confirm Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Cancel/Delete Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Delete Old Entry on Edit)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries (Create Edited Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/volunteers/{id} (Next Entry Volunteer Detail)** (2 connections) — `n8n/workflows/manager_approval.json`
- **n8n: GET /api/managers/me (Get Manager for Next Notification)** (2 connections) — `n8n/workflows/manager_approval.json`
- **POST /api/log-entries/{id}/photos/base64 (upload_photo_base64)** (2 connections) — `api/routers/log_entries.py`
- **Shared Volunteer Data Structure (phone, first_name, last_name, id)** (2 connections) — `api/routers/volunteers.py`
- **Shared Manager Data Structure (phone, first_name, last_name)** (2 connections) — `api/routers/managers.py`
- *... and 26 more nodes in this community*

## Relationships

- [[renderDetail() — volunteer detail page]] (9 shared connections)
- [[errors.py]] (5 shared connections)
- [[007_add_ngo_davcna.py]] (3 shared connections)
- [[log_entries.py]] (2 shared connections)
- [[API.reports.exportPdf()]] (1 shared connections)
- [[PasswordChangeRequest (Schema)]] (1 shared connections)
- [[PhotoBase64Request (Schema)]] (1 shared connections)
- [[settings]] (1 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (1 shared connections)
- [[Community 325]] (1 shared connections)
- [[n8n Set Node Pattern]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `api/routers/managers.py`
- `api/routers/volunteers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 149 (93%)
- INFERRED: 11 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*