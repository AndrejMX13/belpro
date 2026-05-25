# __init__.py

> 24 nodes

## Key Concepts

- **errors.js** (10 connections) — `frontend/js/errors.js`
- **renderAppLog()** (6 connections) — `frontend/js/errors.js`
- **showApp()** (6 connections) — `frontend/js/volunteers.js`
- **loadHealthWidget()** (4 connections) — `frontend/js/errors.js`
- **GET /errors/unacknowledged-count** (4 connections) — `api/routers/errors.py`
- **startHealthWidget()** (3 connections) — `frontend/js/errors.js`
- **refreshErrorBadge()** (3 connections) — `frontend/js/errors.js`
- **loadAppLog()** (3 connections) — `frontend/js/errors.js`
- **initAppLogPage()** (3 connections) — `frontend/js/errors.js`
- **_refreshSidebarLogo()** (3 connections) — `frontend/js/volunteers.js`
- **loadAppLog()** (3 connections) — `frontend/js/errors.js`
- **GET /errors** (3 connections) — `api/routers/errors.py`
- **renderHealthWidget()** (2 connections) — `frontend/js/errors.js`
- **stopHealthWidget()** (2 connections) — `frontend/js/errors.js`
- **API.errors.list()** (2 connections) — `frontend/js/api.js`
- **API.errors.unacknowledgedCount()** (2 connections) — `frontend/js/api.js`
- **API.errors.acknowledge()** (2 connections) — `frontend/js/api.js`
- **refreshErrorBadge()** (2 connections) — `frontend/js/errors.js`
- **PATCH /errors/{id}/acknowledge** (2 connections) — `api/routers/errors.py`
- **ErrorLogResponse shape (id, service, operation, message, detail, acknowledged, created_at)** (2 connections) — `api/routers/errors.py`
- **UnacknowledgedCountResponse shape ({count})** (2 connections) — `api/routers/errors.py`
- **SERVICE_LABELS** (1 connections) — `frontend/js/errors.js`
- **acknowledgeError()** (1 connections) — `frontend/js/errors.js`
- **renderAppLog() — app log page** (1 connections) — `frontend/js/errors.js`

## Relationships

- [[make_text_payload()]] (8 shared connections)
- [[Community 358]] (2 shared connections)
- [[test_managers.py]] (2 shared connections)

## Source Files

- `api/routers/errors.py`
- `frontend/js/api.js`
- `frontend/js/errors.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 63 (88%)
- INFERRED: 9 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*