# AppSettings

> God node · 26 connections · `api/services/app_settings.py`

**Community:** [[AppSettings]]

## Connections by Relation

### calls
- [[update_admin_settings()]] `INFERRED`
- [[get_admin_settings()]] `INFERRED`
- [[get_app_settings()]] `EXTRACTED`
- [[test_appsettings_uses_db_int_value()]] `INFERRED`
- [[test_appsettings_falls_back_to_env_when_row_missing()]] `INFERRED`
- [[test_appsettings_passthrough_to_env()]] `INFERRED`
- [[test_appsettings_bool_helper_parses_truthy_strings()]] `INFERRED`
- [[test_appsettings_bool_helper_parses_falsy_strings()]] `INFERRED`
- [[test_appsettings_bool_helper_falls_back_to_default()]] `INFERRED`
- [[test_appsettings_str_helper_returns_db_value()]] `INFERRED`
- [[test_appsettings_str_helper_falls_back_to_default()]] `INFERRED`
- [[test_appsettings_report_auto_hour_default()]] `INFERRED`
- [[test_appsettings_report_auto_hour_from_db()]] `INFERRED`
- [[test_appsettings_report_auto_hour_clamped_high()]] `INFERRED`
- [[test_appsettings_report_auto_hour_clamped_low()]] `INFERRED`

### contains
- [[app_settings.py]] `EXTRACTED`

### method
- [[._int()]] `EXTRACTED`
- [[._str()]] `EXTRACTED`
- [[._bool()]] `EXTRACTED`
- [[.__getattr__()]] `EXTRACTED`
- [[.__init__()]] `EXTRACTED`

### rationale_for
- [[Central authority for all configuration — env base + DB runtime overrides.]] `EXTRACTED`

### specifies
- [[Settings Table ISS-026 Design]] `EXTRACTED`
- [[AppSettings Central Configuration Authority]] `EXTRACTED`

### uses
- [[AppSetting]] `INFERRED`
- [[Settings]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*