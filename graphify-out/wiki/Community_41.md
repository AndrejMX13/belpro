# Community 41

> 16 nodes · cohesion 0.12

## Key Concepts

- **manager.py** (8 connections) — `api/schemas/manager.py`
- **get_config_info()** (4 connections) — `api/routers/managers.py`
- **ConfigInfoResponse** (4 connections) — `api/schemas/manager.py`
- **ManagerCreate** (3 connections) — `api/schemas/manager.py`
- **ManagerResponse** (3 connections) — `api/schemas/manager.py`
- **ManagerUpdate** (3 connections) — `api/schemas/manager.py`
- **PasswordChangeRequest** (3 connections) — `api/schemas/manager.py`
- **normalize_wa_phone()** (2 connections) — `api/schemas/manager.py`
- **_validate_davcna_checksum()** (2 connections) — `api/schemas/manager.py`
- **Return config status for the settings UI; auto-syncs WhatsApp phone if connected** (1 connections) — `api/routers/managers.py`
- **Pydantic schemas for the Manager entity.** (1 connections) — `api/schemas/manager.py`
- **Response schema for GET /managers/me/config-info.** (1 connections) — `api/schemas/manager.py`
- **Fields required for first-time manager setup.** (1 connections) — `api/schemas/manager.py`
- **Partial update — all fields optional.  Only provided fields are written.** (1 connections) — `api/schemas/manager.py`
- **Payload for the change-password endpoint.** (1 connections) — `api/schemas/manager.py`
- **Manager profile returned by the API.** (1 connections) — `api/schemas/manager.py`

## Relationships

- [[Community 37]] (5 shared connections)
- [[Community 3]] (2 shared connections)
- [[Community 55]] (1 shared connections)
- [[Community 42]] (1 shared connections)

## Source Files

- `api/routers/managers.py`
- `api/schemas/manager.py`

## Audit Trail

- EXTRACTED: 34 (87%)
- INFERRED: 5 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*