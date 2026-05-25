# Community 546

> 5 nodes

## Key Concepts

- **GET /api/volunteers/{id} (get_volunteer)** (7 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers/{id} (Next Entry Volunteer Detail)** (2 connections) — `n8n/workflows/manager_approval.json`
- **Shared Volunteer Data Structure (phone, first_name, last_name, id)** (2 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers/{id} (Get Volunteer for Manager Msg)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/volunteers/{id} (Auto Notify Volunteer Detail)** (1 connections) — `n8n/workflows/volunteer_entry.json`

## Relationships

- [[Code: Preveri Slike Stanje]] (2 shared connections)
- [[errors.py]] (1 shared connections)
- [[PDF Generated (Per Volunteer + Consolidated)]] (1 shared connections)
- [[API.reports.downloadHistoryPdf()]] (1 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 12 (92%)
- INFERRED: 1 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*