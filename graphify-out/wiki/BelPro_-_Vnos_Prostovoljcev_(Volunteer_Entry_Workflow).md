# BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)

> 13 nodes · cohesion 0.22

## Key Concepts

- **BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)** (15 connections) — `n8n/workflows/volunteer_entry.json`
- **create_log_entry()** (8 connections) — `api/routers/log_entries.py`
- **confirm_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **POST /api/log-entries (create_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **DELETE /api/log-entries/{id} (delete_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **POST /api/log-entries/{id}/confirm (confirm_log_entry)** (5 connections) — `api/routers/log_entries.py`
- **n8n: POST /api/log-entries (Create Entry)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries/{id}/confirm (Confirm Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Cancel/Delete Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: DELETE /api/log-entries/{id} (Delete Old Entry on Edit)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries (Create Edited Entry)** (2 connections) — `n8n/workflows/volunteer_entry.json`
- **Create a new log entry.  Volunteer must exist and be active.** (1 connections) — `api/routers/log_entries.py`
- **Volunteer confirmed the entry. Transitions pending_volunteer → pending_manager.** (1 connections) — `api/routers/log_entries.py`

## Relationships

- [[Volunteer (ORM)]] (7 shared connections)
- [[log_entries.py]] (3 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (3 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (3 shared connections)
- [[GET /api/volunteers/{id} (get_volunteer)]] (2 shared connections)
- [[GET /api/managers/me (get_manager)]] (2 shared connections)
- [[Base]] (1 shared connections)
- [[PATCH /api/log-entries/{id}/notify (notify_log_entry)]] (1 shared connections)
- [[load_key()]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 51 (89%)
- INFERRED: 6 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*