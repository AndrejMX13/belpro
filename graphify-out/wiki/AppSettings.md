# AppSettings

> 31 nodes · cohesion 0.09

## Key Concepts

- **AppSettings** (26 connections) — `api/services/app_settings.py`
- **get_settings()** (24 connections) — `api/core/settings.py`
- **test_appsettings_uses_db_int_value()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_falls_back_to_env_when_row_missing()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_passthrough_to_env()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_parses_falsy_strings()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_returns_db_value()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_from_db()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_high()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_clamped_low()** (4 connections) — `api/tests/test_app_settings.py`
- **._bool()** (3 connections) — `api/services/app_settings.py`
- **.__getattr__()** (3 connections) — `api/services/app_settings.py`
- **.__init__()** (2 connections) — `api/services/app_settings.py`
- **Return a cached Settings instance (constructed once per process).** (1 connections) — `api/core/settings.py`
- **Central authority for all configuration — env base + DB runtime overrides.** (1 connections) — `api/services/app_settings.py`
- **Resolve a boolean setting: 'true'/'1'/'yes' → True, else False.** (1 connections) — `api/services/app_settings.py`
- **Delegate any non-overridden attribute to the underlying env Settings.** (1 connections) — `api/services/app_settings.py`
- **DB value overrides env default for integer settings.** (1 connections) — `api/tests/test_app_settings.py`
- **Env default is used when the DB row is absent.** (1 connections) — `api/tests/test_app_settings.py`
- **Non-tunable attributes delegate to the underlying env Settings.** (1 connections) — `api/tests/test_app_settings.py`
- **_bool() returns False for any non-truthy string.** (1 connections) — `api/tests/test_app_settings.py`
- **_bool() returns the default when the key is absent.** (1 connections) — `api/tests/test_app_settings.py`
- *... and 6 more nodes in this community*

## Relationships

- [[test_app_settings.py]] (13 shared connections)
- [[Settings Table ISS-026 Design]] (5 shared connections)
- [[app_settings.py]] (4 shared connections)
- [[Settings]] (3 shared connections)
- [[update_admin_settings()]] (3 shared connections)
- [[api/main.py]] (2 shared connections)
- [[env.py]] (1 shared connections)
- [[errors.py]] (1 shared connections)
- [[send_monthly_reports()]] (1 shared connections)
- [[conftest.py]] (1 shared connections)
- [[volunteer_factory()]] (1 shared connections)
- [[test_errors.py]] (1 shared connections)

## Source Files

- `api/core/settings.py`
- `api/services/app_settings.py`
- `api/tests/test_app_settings.py`

## Audit Trail

- EXTRACTED: 58 (50%)
- INFERRED: 59 (50%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*