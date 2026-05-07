# Analytics Engine

**Nodes:** 43 | **Cohesion:** 0.101 | **Internal edges:** 91

## Files & Symbols
- **BaseModel** `(no file)`
- **manager.py** `D:\Andrej\vsCode-workspace\BelPro\api\models\manager.py`
- **volunteer.py** `D:\Andrej\vsCode-workspace\BelPro\api\models\volunteer.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\analytics.py` — 5 symbols (e.g. analytics.py, analytics_summary(), ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\managers.py` — 12 symbols (e.g. managers.py, get_manager(), ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\analytics.py` — 10 symbols (e.g. Pydantic schemas for the analytics summary endpoint., analytics.py, ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py` — 10 symbols (e.g. Pydantic schemas for the Manager entity., manager.py, ...)
- **LogEntryBrief** `D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py`
- **Compact log entry view — used inside VolunteerDetailResponse.** `D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py`
- **Change the manager password.  Verifies the current password before updating.** `api\routers\managers.py`

## Bridges To Other Communities
### → API Data Models & Schemas (42 edges)
- manager.py --contains--> Manager [EXTRACTED]
- Base --uses--> Pydantic schemas for the Manager entity. [INFERRED]
- Pydantic schemas for the Manager entity. --uses--> Volunteer [INFERRED]
- volunteer.py --contains--> Volunteer [EXTRACTED]
- EntryStatus --uses--> Pydantic schemas for the analytics summary endpoint. [INFERRED]
  ... and 37 more
### → API Request Handlers (2 edges)
- str --calls--> create_manager() [INFERRED]
- str --calls--> update_manager() [INFERRED]
### → PDF Report Generation (2 edges)
- BaseModel --inherits--> VolunteerMonthlySummary [EXTRACTED]
- BaseModel --inherits--> MonthlyReportSummary [EXTRACTED]
