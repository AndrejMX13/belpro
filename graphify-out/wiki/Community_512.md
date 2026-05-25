# Community 512

> 6 nodes

## Key Concepts

- **submitAddVolunteer()** (3 connections) — `frontend/js/volunteers.js`
- **POST /volunteers/check-emso** (3 connections) — `api/routers/volunteers.py`
- **API.volunteers.checkEmso()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.create()** (2 connections) — `frontend/js/api.js`
- **POST /volunteers** (2 connections) — `api/routers/volunteers.py`
- **EmsoCheckResponse shape ({exists})** (2 connections) — `api/routers/volunteers.py`

## Relationships

- [[make_text_payload()]] (2 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `frontend/js/api.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 14 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*