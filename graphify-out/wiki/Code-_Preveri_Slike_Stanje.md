# Code: Preveri Slike Stanje

> 16 nodes

## Key Concepts

- **BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)** (15 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/managers/me (get_manager)** (9 connections) — `api/routers/managers.py`
- **POST /api/log-entries (create_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **DELETE /api/log-entries/{id} (delete_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **POST /api/log-entries/{id}/confirm (confirm_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **GET /api/volunteers (list_volunteers)** (4 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers?search_by=phone (Lookup Volunteer by Phone)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries (Create Entry)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/managers/me (Lookup Manager in Volunteer Workflow)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries/{id}/confirm (Confirm Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Cancel/Delete Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Delete Old Entry on Edit)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries (Create Edited Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/managers/me (Get Manager for Next Notification)** (2 connections) — `n8n/workflows/manager_approval.json`
- **Shared Manager Data Structure (phone, first_name, last_name)** (2 connections) — `api/routers/managers.py`
- **n8n: GET /api/managers/me (Early Lookup at Webhook Entry)** (1 connections) — `n8n/workflows/volunteer_entry.json`

## Relationships

- [[PDF Generated (Per Volunteer + Consolidated)]] (5 shared connections)
- [[LoginRequest (Schema)]] (3 shared connections)
- [[BelPro Project Memory Public Index]] (3 shared connections)
- [[API.reports.downloadHistoryPdf()]] (2 shared connections)
- [[Community 546]] (2 shared connections)
- [[errors.py]] (1 shared connections)
- [[IF: Should Notify? (Auto)]] (1 shared connections)
- [[010_monthly_reports_unique_idx.py]] (1 shared connections)
- [[DevOps Engineer Skill]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `api/routers/managers.py`
- `api/routers/volunteers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 59 (91%)
- INFERRED: 6 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*