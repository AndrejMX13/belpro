# DELETE /api/log-entries/{id}/photos/{photo_id} (delete_photo)

> 12 nodes

## Key Concepts

- **manager.py** (8 connections) — `api/schemas/manager.py`
- **ManagerCreate** (3 connections) — `api/schemas/manager.py`
- **ManagerUpdate** (3 connections) — `api/schemas/manager.py`
- **PasswordChangeRequest** (3 connections) — `api/schemas/manager.py`
- **ManagerResponse** (3 connections) — `api/schemas/manager.py`
- **_validate_davcna_checksum()** (2 connections) — `api/schemas/manager.py`
- **normalize_wa_phone()** (2 connections) — `api/schemas/manager.py`
- **Pydantic schemas for the Manager entity.** (1 connections) — `api/schemas/manager.py`
- **Fields required for first-time manager setup.** (1 connections) — `api/schemas/manager.py`
- **Partial update — all fields optional.  Only provided fields are written.** (1 connections) — `api/schemas/manager.py`
- **Payload for the change-password endpoint.** (1 connections) — `api/schemas/manager.py`
- **Manager profile returned by the API.** (1 connections) — `api/schemas/manager.py`

## Relationships

- [[Porocila Page - Monthly Reports Overview]] (4 shared connections)
- [[IF: Should Notify? (Auto)]] (1 shared connections)
- [[Code: Check Pending (Manual)]] (1 shared connections)
- [[Normalise phone to bare E.164 digits, pass through None.]] (1 shared connections)

## Source Files

- `api/schemas/manager.py`

## Audit Trail

- EXTRACTED: 27 (93%)
- INFERRED: 2 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*