# Community 23

> 27 nodes · cohesion 0.10

## Key Concepts

- **app_settings.py** (30 connections) — `api/services/app_settings.py`
- **._int()** (10 connections) — `api/services/app_settings.py`
- **photo_cleanup.py** (5 connections) — `ops/scripts/photo_cleanup.py`
- **dsn_from_url()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **report_error()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **._str()** (3 connections) — `api/services/app_settings.py`
- **._bool()** (2 connections) — `api/services/app_settings.py`
- **.__getattr__()** (2 connections) — `api/services/app_settings.py`
- **backup_hour()** (2 connections) — `api/services/app_settings.py`
- **backup_retention_days()** (2 connections) — `api/services/app_settings.py`
- **get_app_settings()** (2 connections) — `api/services/app_settings.py`
- **max_photos_per_entry()** (2 connections) — `api/services/app_settings.py`
- **photo_retention_days()** (2 connections) — `api/services/app_settings.py`
- **report_auto_day()** (2 connections) — `api/services/app_settings.py`
- **report_auto_hour()** (2 connections) — `api/services/app_settings.py`
- **report_auto_period()** (2 connections) — `api/services/app_settings.py`
- **session_duration_hours()** (2 connections) — `api/services/app_settings.py`
- **POST failure to the API error log.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **Convert asyncpg DATABASE_URL to psycopg2 DSN.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **.__init__()** (1 connections) — `api/services/app_settings.py`
- **AppSettings — central authority for all configuration.  Wraps the env-only Setti** (1 connections) — `api/services/app_settings.py`
- **Delegate any non-overridden attribute to the underlying env Settings.** (1 connections) — `api/services/app_settings.py`
- **FastAPI dependency — returns the central settings authority for this request.** (1 connections) — `api/services/app_settings.py`
- **Central authority for all configuration — env base + DB runtime overrides.** (1 connections) — `api/services/app_settings.py`
- **Resolve an integer setting: DB value first, env default fallback.          Falls** (1 connections) — `api/services/app_settings.py`
- *... and 2 more nodes in this community*

## Relationships

- [[Community 36]] (8 shared connections)
- [[Community 8]] (3 shared connections)
- [[Community 50]] (2 shared connections)
- [[Community 83]] (1 shared connections)
- [[Community 46]] (1 shared connections)
- [[Community 27]] (1 shared connections)

## Source Files

- `api/services/app_settings.py`
- `ops/scripts/photo_cleanup.py`

## Audit Trail

- EXTRACTED: 73 (85%)
- INFERRED: 13 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*