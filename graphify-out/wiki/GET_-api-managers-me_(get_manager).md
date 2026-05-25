# GET /api/managers/me (get_manager)

> 6 nodes · cohesion 0.40

## Key Concepts

- **GET /api/managers/me (get_manager)** (9 connections) — `api/routers/managers.py`
- **n8n: GET /api/managers/me (Lookup Manager in Volunteer Workflow)** (3 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/managers/me (Get Manager for Next Notification)** (2 connections) — `n8n/workflows/manager_approval.json`
- **POST /api/auth/login (login)** (2 connections) — `api/routers/auth.py`
- **Shared Manager Data Structure (phone, first_name, last_name)** (2 connections) — `api/routers/managers.py`
- **n8n: GET /api/managers/me (Early Lookup at Webhook Entry)** (1 connections) — `n8n/workflows/volunteer_entry.json`

## Relationships

- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (2 shared connections)
- [[managers.py]] (1 shared connections)
- [[n8n/workflows/manager_approval.json]] (1 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (1 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (1 shared connections)
- [[Settings Table ISS-026 Design]] (1 shared connections)

## Source Files

- `api/routers/auth.py`
- `api/routers/managers.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 16 (84%)
- INFERRED: 3 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*