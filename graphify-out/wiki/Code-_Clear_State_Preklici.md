# Code: Clear State Preklici

> 16 nodes

## Key Concepts

- **app_settings.py** (16 connections) — `api/services/app_settings.py`
- **._int()** (11 connections) — `api/services/app_settings.py`
- **download_consent_pdf()** (5 connections) — `api/routers/documents.py`
- **documents.py** (4 connections) — `api/routers/documents.py`
- **photo_retention_days()** (4 connections) — `api/services/app_settings.py`
- **session_duration_hours()** (4 connections) — `api/services/app_settings.py`
- **max_photos_per_entry()** (3 connections) — `api/services/app_settings.py`
- **report_auto_day()** (3 connections) — `api/services/app_settings.py`
- **backup_hour()** (2 connections) — `api/services/app_settings.py`
- **photo_cleanup_hour()** (2 connections) — `api/services/app_settings.py`
- **report_auto_hour()** (2 connections) — `api/services/app_settings.py`
- **backup_retention_days()** (2 connections) — `api/services/app_settings.py`
- **Documents router — downloadable compliance documents.** (1 connections) — `api/routers/documents.py`
- **Generate and stream the GDPR Article 13 consent notice PDF.** (1 connections) — `api/routers/documents.py`
- **AppSettings — central authority for all configuration.  Wraps the env-only Setti** (1 connections) — `api/services/app_settings.py`
- **Resolve an integer setting: DB value first, env default fallback.          Falls** (1 connections) — `api/services/app_settings.py`

## Relationships

- [[Manager WhatsApp Approval Workflow Design]] (7 shared connections)
- [[HTTP: PATCH /notify (Manual)]] (6 shared connections)
- [[main()]] (2 shared connections)
- [[DevOps Engineer Skill]] (1 shared connections)

## Source Files

- `api/routers/documents.py`
- `api/services/app_settings.py`

## Audit Trail

- EXTRACTED: 61 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*