# app_settings.py

> 17 nodes · cohesion 0.17

## Key Concepts

- **app_settings.py** (16 connections) — `api/services/app_settings.py`
- **._int()** (11 connections) — `api/services/app_settings.py`
- **get_app_settings()** (6 connections) — `api/services/app_settings.py`
- **._str()** (4 connections) — `api/services/app_settings.py`
- **photo_retention_days()** (4 connections) — `api/services/app_settings.py`
- **session_duration_hours()** (4 connections) — `api/services/app_settings.py`
- **max_photos_per_entry()** (3 connections) — `api/services/app_settings.py`
- **report_auto_day()** (3 connections) — `api/services/app_settings.py`
- **report_auto_period()** (3 connections) — `api/services/app_settings.py`
- **backup_hour()** (2 connections) — `api/services/app_settings.py`
- **photo_cleanup_hour()** (2 connections) — `api/services/app_settings.py`
- **report_auto_hour()** (2 connections) — `api/services/app_settings.py`
- **backup_retention_days()** (2 connections) — `api/services/app_settings.py`
- **AppSettings — central authority for all configuration.  Wraps the env-only Setti** (1 connections) — `api/services/app_settings.py`
- **Resolve an integer setting: DB value first, env default fallback.          Falls** (1 connections) — `api/services/app_settings.py`
- **Resolve a string setting: DB value first, default fallback.** (1 connections) — `api/services/app_settings.py`
- **FastAPI dependency — returns the central settings authority for this request.** (1 connections) — `api/services/app_settings.py`

## Relationships

- [[Settings Table ISS-026 Design]] (11 shared connections)
- [[AppSettings]] (4 shared connections)
- [[render_consent_pdf()]] (3 shared connections)
- [[update_admin_settings()]] (2 shared connections)

## Source Files

- `api/services/app_settings.py`

## Audit Trail

- EXTRACTED: 65 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*