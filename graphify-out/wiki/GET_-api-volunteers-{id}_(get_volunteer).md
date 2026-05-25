# GET /api/volunteers/{id} (get_volunteer)

> 6 nodes · cohesion 0.33

## Key Concepts

- **GET /api/volunteers/{id} (get_volunteer)** (7 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers?search_by=phone (Lookup Volunteer by Phone)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/volunteers/{id} (Next Entry Volunteer Detail)** (2 connections) — `n8n/workflows/manager_approval.json`
- **Shared Volunteer Data Structure (phone, first_name, last_name, id)** (2 connections) — `api/routers/volunteers.py`
- **n8n: GET /api/volunteers/{id} (Get Volunteer for Manager Msg)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/volunteers/{id} (Auto Notify Volunteer Detail)** (1 connections) — `n8n/workflows/volunteer_entry.json`

## Relationships

- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (2 shared connections)
- [[load_key()]] (2 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (1 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (1 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 15 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*