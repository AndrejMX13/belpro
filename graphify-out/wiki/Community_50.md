# Community 50

> 12 nodes · cohesion 0.20

## Key Concepts

- **update_admin_settings()** (7 connections) — `api/routers/admin.py`
- **get_admin_settings()** (5 connections) — `api/routers/admin.py`
- **_notify_ops()** (5 connections) — `api/routers/admin.py`
- **AdminSettingsResponse** (5 connections) — `api/schemas/admin.py`
- **admin.py** (4 connections) — `api/routers/admin.py`
- **admin.py** (3 connections) — `api/schemas/admin.py`
- **Admin router — runtime-tunable settings management.** (1 connections) — `api/routers/admin.py`
- **POST /reconfigure to ops. Logs and persists error on failure; never raises.** (1 connections) — `api/routers/admin.py`
- **Return current values of all runtime-tunable settings.** (1 connections) — `api/routers/admin.py`
- **Update one or more runtime-tunable settings. Returns updated state.** (1 connections) — `api/routers/admin.py`
- **Pydantic schemas for the admin settings endpoints.** (1 connections) — `api/schemas/admin.py`
- **Current values of all runtime-tunable settings.** (1 connections) — `api/schemas/admin.py`

## Relationships

- [[Community 37]] (2 shared connections)
- [[Community 23]] (2 shared connections)
- [[Community 46]] (2 shared connections)
- [[Community 11]] (2 shared connections)
- [[Community 36]] (1 shared connections)

## Source Files

- `api/routers/admin.py`
- `api/schemas/admin.py`

## Audit Trail

- EXTRACTED: 24 (69%)
- INFERRED: 11 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*