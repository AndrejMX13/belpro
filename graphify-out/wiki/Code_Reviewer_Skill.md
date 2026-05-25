# Code Reviewer Skill

> 43 nodes

## Key Concepts

- **volunteer_entry.json** (34 connections) — `n8n/workflows/volunteer_entry.json`
- **BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)** (15 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/managers/me (get_manager)** (9 connections) — `api/routers/managers.py`
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
- **Shared Volunteer Data Structure (phone, first_name, last_name, id)** (2 connections) — `api/routers/volunteers.py`
- **Shared Manager Data Structure (phone, first_name, last_name)** (2 connections) — `api/routers/managers.py`
- **updatedAt** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **createdAt** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **id** (1 connections) — `n8n/workflows/volunteer_entry.json`
- *... and 18 more nodes in this community*

## Relationships

- [[scripts/gen_diagrams_sl.py]] (8 shared connections)
- [[connections]] (6 shared connections)
- [[005_report_prefs.py]] (3 shared connections)
- [[report_pdf.py]] (2 shared connections)
- [[002_add_emso_hash.py]] (1 shared connections)
- [[Community 345]] (1 shared connections)
- [[Community 313]] (1 shared connections)
- [[merge_ast_semantic.py]] (1 shared connections)
- [[HTTP: Fetch Media]] (1 shared connections)
- [[Community 321]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `api/routers/managers.py`
- `api/routers/volunteers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 129 (94%)
- INFERRED: 8 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*