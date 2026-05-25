# GET /api/log-entries (list_log_entries)

> 9 nodes · cohesion 0.22

## Key Concepts

- **GET /api/log-entries (list_log_entries)** (10 connections) — `api/routers/log_entries.py`
- **list_log_entries()** (7 connections) — `api/routers/log_entries.py`
- **n8n: GET /api/log-entries?status=pending_manager (Post-Action Queue Check)** (2 connections) — `n8n/workflows/manager_approval.json`
- **analytics_summary** (2 connections) — `api/routers/analytics.py`
- **List log entries with optional filters, sorting, and pagination.** (1 connections) — `api/routers/log_entries.py`
- **n8n: GET /api/log-entries?status=pending_manager (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/log-entries?status=pending_manager (Auto Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/log-entries?status=pending_manager (Get Notified Entry)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/reports/monthly (monthly_summary)** (1 connections) — `api/routers/reports.py`

## Relationships

- [[Volunteer (ORM)]] (3 shared connections)
- [[log_entries.py]] (1 shared connections)
- [[BaseModel]] (1 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (1 shared connections)
- [[n8n/workflows/manager_approval.json]] (1 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (1 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (1 shared connections)

## Source Files

- `api/routers/analytics.py`
- `api/routers/log_entries.py`
- `api/routers/reports.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 19 (73%)
- INFERRED: 7 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*