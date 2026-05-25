# update_admin_settings()

> 12 nodes · cohesion 0.21

## Key Concepts

- **update_admin_settings()** (10 connections) — `api/routers/admin.py`
- **admin.py** (9 connections) — `api/routers/admin.py`
- **_notify_ops()** (7 connections) — `api/routers/admin.py`
- **get_admin_settings()** (6 connections) — `api/routers/admin.py`
- **AdminSettingsResponse** (5 connections) — `api/schemas/admin.py`
- **admin.py** (4 connections) — `api/schemas/admin.py`
- **Admin router — runtime-tunable settings management.** (1 connections) — `api/routers/admin.py`
- **POST /reconfigure to ops. Logs and persists error on failure; never raises.** (1 connections) — `api/routers/admin.py`
- **Return current values of all runtime-tunable settings.** (1 connections) — `api/routers/admin.py`
- **Update one or more runtime-tunable settings. Returns updated state.** (1 connections) — `api/routers/admin.py`
- **Pydantic schemas for the admin settings endpoints.** (1 connections) — `api/schemas/admin.py`
- **Current values of all runtime-tunable settings.** (1 connections) — `api/schemas/admin.py`

## Relationships

- [[Settings Table ISS-026 Design]] (8 shared connections)
- [[AppSettings]] (3 shared connections)
- [[app_settings.py]] (2 shared connections)
- [[Base]] (2 shared connections)
- [[str]] (2 shared connections)
- [[BaseModel]] (2 shared connections)

## Source Files

- `api/routers/admin.py`
- `api/schemas/admin.py`

## Audit Trail

- EXTRACTED: 32 (68%)
- INFERRED: 15 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*