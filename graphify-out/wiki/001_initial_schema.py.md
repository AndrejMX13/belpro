# 001_initial_schema.py

> 20 nodes

## Key Concepts

- **test_managers.py** (14 connections) — `api/tests/test_managers.py`
- **seed_whatsapp_phone_from_env()** (6 connections) — `api/main.py`
- **test_seed_whatsapp_phone_populates_null_db_field()** (3 connections) — `api/tests/test_managers.py`
- **test_seed_whatsapp_phone_does_not_overwrite_existing_value()** (3 connections) — `api/tests/test_managers.py`
- **test_change_password_invalidates_old_credentials()** (2 connections) — `api/tests/test_managers.py`
- **Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.** (1 connections) — `api/main.py`
- **test_get_manager_returns_profile()** (1 connections) — `api/tests/test_managers.py`
- **test_create_manager_returns_409_when_already_configured()** (1 connections) — `api/tests/test_managers.py`
- **test_auth_wrong_password_returns_401()** (1 connections) — `api/tests/test_managers.py`
- **test_auth_missing_credentials_returns_401()** (1 connections) — `api/tests/test_managers.py`
- **test_config_info_includes_wa_fields()** (1 connections) — `api/tests/test_managers.py`
- **test_config_info_auto_syncs_when_evolution_reports_new_phone()** (1 connections) — `api/tests/test_managers.py`
- **test_config_info_no_sync_when_phone_already_matches()** (1 connections) — `api/tests/test_managers.py`
- **test_config_info_shows_db_phone_when_disconnected()** (1 connections) — `api/tests/test_managers.py`
- **test_update_manager_normalizes_whatsapp_phone()** (1 connections) — `api/tests/test_managers.py`
- **test_update_manager_rejects_too_short_phone()** (1 connections) — `api/tests/test_managers.py`
- **test_update_manager_empty_phone_not_stored_as_empty_string()** (1 connections) — `api/tests/test_managers.py`
- **seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null** (1 connections) — `api/tests/test_managers.py`
- **seed_whatsapp_phone_from_env leaves existing DB value untouched.** (1 connections) — `api/tests/test_managers.py`
- **After a password change, old credentials return 401 and new ones return 200.** (1 connections) — `api/tests/test_managers.py`

## Relationships

- [[HTTP: GET Volunteer (Mgr)]] (2 shared connections)
- [[Normalise phone to bare E.164 digits, pass through None.]] (1 shared connections)

## Source Files

- `api/main.py`
- `api/tests/test_managers.py`

## Audit Trail

- EXTRACTED: 38 (88%)
- INFERRED: 5 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*