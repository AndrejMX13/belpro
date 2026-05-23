# Community 36

> 19 nodes · cohesion 0.11

## Key Concepts

- **get_settings()** (21 connections) — `api/core/settings.py`
- **test_appsettings_bool_helper_parses_falsy_strings()** (5 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_bool_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_falls_back_to_env_when_row_missing()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_passthrough_to_env()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_report_auto_hour_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_falls_back_to_default()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_str_helper_returns_db_value()** (4 connections) — `api/tests/test_app_settings.py`
- **test_appsettings_uses_db_int_value()** (4 connections) — `api/tests/test_app_settings.py`
- **Return a cached Settings instance (constructed once per process).** (1 connections) — `api/core/settings.py`
- **_str() returns the default when key is absent.** (1 connections) — `api/tests/test_app_settings.py`
- **report_auto_hour defaults to 7 when no DB row exists.** (1 connections) — `api/tests/test_app_settings.py`
- **DB value overrides env default for integer settings.** (1 connections) — `api/tests/test_app_settings.py`
- **Env default is used when the DB row is absent.** (1 connections) — `api/tests/test_app_settings.py`
- **Non-tunable attributes delegate to the underlying env Settings.** (1 connections) — `api/tests/test_app_settings.py`
- **_bool() accepts 'true', '1', 'yes' as True.** (1 connections) — `api/tests/test_app_settings.py`
- **_bool() returns False for any non-truthy string.** (1 connections) — `api/tests/test_app_settings.py`
- **_bool() returns the default when the key is absent.** (1 connections) — `api/tests/test_app_settings.py`
- **_str() returns the DB string when present.** (1 connections) — `api/tests/test_app_settings.py`

## Relationships

- [[Community 27]] (9 shared connections)
- [[Community 23]] (8 shared connections)
- [[Community 83]] (2 shared connections)
- [[Community 3]] (2 shared connections)
- [[Community 51]] (1 shared connections)
- [[Community 50]] (1 shared connections)
- [[Community 57]] (1 shared connections)
- [[Community 69]] (1 shared connections)
- [[Community 61]] (1 shared connections)
- [[Community 25]] (1 shared connections)
- [[Community 31]] (1 shared connections)

## Source Files

- `api/core/settings.py`
- `api/tests/test_app_settings.py`

## Audit Trail

- EXTRACTED: 30 (47%)
- INFERRED: 34 (53%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*