# HTTP: PATCH /notify (Manual)

> 15 nodes

## Key Concepts

- **AppSettings** (26 connections) — `api/services/app_settings.py`
- **AppSettings Central Configuration Authority** (10 connections) — `docs/superpowers/specs/2026-05-20-settings-table-design.md`
- **AppSetting** (6 connections) — `api/models/app_setting.py`
- **get_app_settings()** (6 connections) — `api/services/app_settings.py`
- **._str()** (4 connections) — `api/services/app_settings.py`
- **._bool()** (3 connections) — `api/services/app_settings.py`
- **report_auto_period()** (3 connections) — `api/services/app_settings.py`
- **.__getattr__()** (3 connections) — `api/services/app_settings.py`
- **.__init__()** (2 connections) — `api/services/app_settings.py`
- **One row per named setting. All values stored as TEXT.** (1 connections) — `api/models/app_setting.py`
- **Central authority for all configuration — env base + DB runtime overrides.** (1 connections) — `api/services/app_settings.py`
- **Resolve a boolean setting: 'true'/'1'/'yes' → True, else False.** (1 connections) — `api/services/app_settings.py`
- **Resolve a string setting: DB value first, default fallback.** (1 connections) — `api/services/app_settings.py`
- **Delegate any non-overridden attribute to the underlying env Settings.** (1 connections) — `api/services/app_settings.py`
- **FastAPI dependency — returns the central settings authority for this request.** (1 connections) — `api/services/app_settings.py`

## Relationships

- [[monthly_reports.json]] (12 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (9 shared connections)
- [[Code: Clear State Preklici]] (6 shared connections)
- [[Evolution API (API Gateway)]] (3 shared connections)
- [[Community 589]] (1 shared connections)

## Source Files

- `api/models/app_setting.py`
- `api/services/app_settings.py`
- `docs/superpowers/specs/2026-05-20-settings-table-design.md`

## Audit Trail

- EXTRACTED: 49 (71%)
- INFERRED: 20 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*