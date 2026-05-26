# Community 317

> 11 nodes

## Key Concepts

- **renderList() — volunteers page** (5 connections) — `frontend/js/volunteers.js`
- **GET /volunteers** (4 connections) — `api/routers/volunteers.py`
- **loadVolunteers()** (3 connections) — `frontend/js/volunteers.js`
- **loadHealthWidget()** (3 connections) — `frontend/js/errors.js`
- **API.volunteers.list()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.activate()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.deactivate()** (2 connections) — `frontend/js/api.js`
- **VolunteerListResponse shape (items[], total)** (2 connections) — `api/routers/volunteers.py`
- **API.health.detailed()** (1 connections) — `frontend/js/api.js`
- **PATCH /volunteers/{id}/activate** (1 connections) — `api/routers/volunteers.py`
- **PATCH /volunteers/{id}/deactivate** (1 connections) — `api/routers/volunteers.py`

## Relationships

- [[test_auth.py]] (2 shared connections)
- [[path]] (1 shared connections)
- [[Community 404]] (1 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `frontend/js/api.js`
- `frontend/js/errors.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 25 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*