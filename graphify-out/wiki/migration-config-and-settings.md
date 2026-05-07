# Migration Config & Settings

**Nodes:** 16 | **Cohesion:** 0.150 | **Internal edges:** 18

## Files & Symbols
- `D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py` — 4 symbols (e.g. settings.py, get_settings(), ...)
- `api\db\migrations\env.py` — 12 symbols (e.g. env.py, _get_url(), ...)

## Bridges To Other Communities
### → API Data Models & Schemas (2 edges)
- settings.py --contains--> Settings [EXTRACTED]
- Settings --calls--> get_settings() [EXTRACTED]
### → API Request Handlers (1 edges)
- get_settings() --calls--> _notify_volunteer_email() [INFERRED]
### → PDF Report Generation (1 edges)
- get_settings() --calls--> send_monthly_reports() [INFERRED]
