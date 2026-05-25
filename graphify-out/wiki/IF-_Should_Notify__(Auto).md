# IF: Should Notify? (Auto)

> 14 nodes

## Key Concepts

- **managers.py** (6 connections) — `api/routers/managers.py`
- **create_manager()** (4 connections) — `api/routers/managers.py`
- **get_config_info()** (4 connections) — `api/routers/managers.py`
- **ConfigInfoResponse** (4 connections) — `api/schemas/manager.py`
- **get_manager()** (3 connections) — `api/routers/managers.py`
- **update_manager()** (3 connections) — `api/routers/managers.py`
- **change_password()** (2 connections) — `api/routers/managers.py`
- **Managers router — single-manager setup and profile.** (1 connections) — `api/routers/managers.py`
- **Return the single manager profile, or 404 if setup has not been completed.** (1 connections) — `api/routers/managers.py`
- **Seed the manager profile (first-time setup). Returns 409 if already configured.** (1 connections) — `api/routers/managers.py`
- **Update manager and/or NGO fields.  Only provided (non-None) fields are written.** (1 connections) — `api/routers/managers.py`
- **Return config status for the settings UI; auto-syncs WhatsApp phone if connected** (1 connections) — `api/routers/managers.py`
- **Change the manager password.  Verifies the current password before updating.** (1 connections) — `api/routers/managers.py`
- **Response schema for GET /managers/me/config-info.** (1 connections) — `api/schemas/manager.py`

## Relationships

- [[005_report_prefs.py]] (2 shared connections)
- [[Code: Preveri Slike Stanje]] (1 shared connections)
- [[Evolution API (API Gateway)]] (1 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (1 shared connections)
- [[Porocila Page - Monthly Reports Overview]] (1 shared connections)
- [[DELETE /api/log-entries/{id}/photos/{photo_id} (delete_photo)]] (1 shared connections)

## Source Files

- `api/routers/managers.py`
- `api/schemas/manager.py`

## Audit Trail

- EXTRACTED: 26 (79%)
- INFERRED: 7 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*