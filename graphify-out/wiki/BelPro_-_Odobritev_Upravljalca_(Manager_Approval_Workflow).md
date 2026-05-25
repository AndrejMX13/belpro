# BelPro - Odobritev Upravljalca (Manager Approval Workflow)

> 13 nodes · cohesion 0.19

## Key Concepts

- **BelPro - Odobritev Upravljalca (Manager Approval Workflow)** (13 connections) — `n8n/workflows/manager_approval.json`
- **Shared LogEntry Data Structure (volunteer_id, work_date, hours, activity_description, location, status, raw_transcript)** (8 connections) — `api/routers/log_entries.py`
- **PATCH /api/log-entries/{id}/approve (approve_log_entry)** (7 connections) — `api/routers/log_entries.py`
- **PATCH /api/log-entries/{id}/reject (reject_log_entry)** (7 connections) — `api/routers/log_entries.py`
- **approve_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **reject_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **n8n: PATCH /api/log-entries/{id}/approve** (4 connections) — `n8n/workflows/manager_approval.json`
- **n8n: PATCH /api/log-entries/{id}/reject** (4 connections) — `n8n/workflows/manager_approval.json`
- **POST /api/log-entries/{id}/photos/base64 (upload_photo_base64)** (2 connections) — `api/routers/log_entries.py`
- **Approve a pending_manager log entry.** (1 connections) — `api/routers/log_entries.py`
- **Reject a pending_manager log entry.** (1 connections) — `api/routers/log_entries.py`
- **n8n: POST /api/log-entries/{id}/photos/base64 (Photo Upload)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/log-entries/photo-limit (get_photo_limit)** (1 connections) — `api/routers/log_entries.py`

## Relationships

- [[Volunteer (ORM)]] (6 shared connections)
- [[Manager WhatsApp Approval Implementation Plan]] (6 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (6 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (3 shared connections)
- [[log_entries.py]] (2 shared connections)
- [[PATCH /api/log-entries/{id}/notify (notify_log_entry)]] (2 shared connections)
- [[n8n/workflows/manager_approval.json]] (2 shared connections)
- [[GET /api/log-entries (list_log_entries)]] (1 shared connections)
- [[GET /api/volunteers/{id} (get_volunteer)]] (1 shared connections)
- [[GET /api/managers/me (get_manager)]] (1 shared connections)
- [[n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 55 (90%)
- INFERRED: 6 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*