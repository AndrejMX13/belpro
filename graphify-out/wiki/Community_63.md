# Community 63

> 9 nodes · cohesion 0.22

## Key Concepts

- **error_log.py** (4 connections) — `api/schemas/error_log.py`
- **unacknowledged_count()** (3 connections) — `api/routers/errors.py`
- **ErrorLogCreate** (3 connections) — `api/schemas/error_log.py`
- **ErrorLogResponse** (3 connections) — `api/schemas/error_log.py`
- **UnacknowledgedCountResponse** (3 connections) — `api/schemas/error_log.py`
- **Return count of unacknowledged errors. Used by nav badge.** (1 connections) — `api/routers/errors.py`
- **Pydantic schemas for the error_log endpoint.** (1 connections) — `api/schemas/error_log.py`
- **Payload sent by internal services (API, n8n, ops sidecar).** (1 connections) — `api/schemas/error_log.py`
- **Single error log row returned to the dashboard.** (1 connections) — `api/schemas/error_log.py`

## Relationships

- [[Community 37]] (3 shared connections)
- [[Community 57]] (1 shared connections)

## Source Files

- `api/routers/errors.py`
- `api/schemas/error_log.py`

## Audit Trail

- EXTRACTED: 18 (90%)
- INFERRED: 2 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*