# Community 55

> 10 nodes · cohesion 0.20

## Key Concepts

- **managers.py** (6 connections) — `api/routers/managers.py`
- **create_manager()** (4 connections) — `api/routers/managers.py`
- **update_manager()** (3 connections) — `api/routers/managers.py`
- **change_password()** (2 connections) — `api/routers/managers.py`
- **get_manager()** (2 connections) — `api/routers/managers.py`
- **Managers router — single-manager setup and profile.** (1 connections) — `api/routers/managers.py`
- **Change the manager password.  Verifies the current password before updating.** (1 connections) — `api/routers/managers.py`
- **Return the single manager profile, or 404 if setup has not been completed.** (1 connections) — `api/routers/managers.py`
- **Seed the manager profile (first-time setup). Returns 409 if already configured.** (1 connections) — `api/routers/managers.py`
- **Update manager and/or NGO fields.  Only provided (non-None) fields are written.** (1 connections) — `api/routers/managers.py`

## Relationships

- [[Community 11]] (2 shared connections)
- [[Community 41]] (1 shared connections)
- [[Community 46]] (1 shared connections)

## Source Files

- `api/routers/managers.py`

## Audit Trail

- EXTRACTED: 19 (86%)
- INFERRED: 3 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*