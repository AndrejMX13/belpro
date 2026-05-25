# loadAppLog()

> 5 nodes · cohesion 0.50

## Key Concepts

- **loadAppLog()** (3 connections) — `frontend/js/errors.js`
- **GET /errors** (3 connections) — `api/routers/errors.py`
- **API.errors.list()** (2 connections) — `frontend/js/api.js`
- **ErrorLogResponse shape (id, service, operation, message, detail, acknowledged, created_at)** (2 connections) — `api/routers/errors.py`
- **renderAppLog() — app log page** (1 connections) — `frontend/js/errors.js`

## Relationships

- [[volunteers.js]] (1 shared connections)

## Source Files

- `api/routers/errors.py`
- `frontend/js/api.js`
- `frontend/js/errors.js`

## Audit Trail

- EXTRACTED: 11 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*