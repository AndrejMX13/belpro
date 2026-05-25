# PATCH /api/log-entries/{id}/notify (notify_log_entry)

> 6 nodes · cohesion 0.33

## Key Concepts

- **PATCH /api/log-entries/{id}/notify (notify_log_entry)** (8 connections) — `api/routers/log_entries.py`
- **notify_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **Mark a pending_manager entry as notified (sets manager_notified_at).      Only** (1 connections) — `api/routers/log_entries.py`
- **n8n: PATCH /api/log-entries/{id}/notify (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: PATCH /api/log-entries/{id}/notify (Auto Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: PATCH /api/log-entries/{id}/notify (Next Entry Notify)** (1 connections) — `n8n/workflows/manager_approval.json`

## Relationships

- [[Volunteer (ORM)]] (3 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (2 shared connections)
- [[log_entries.py]] (1 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (1 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 16 (89%)
- INFERRED: 2 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*