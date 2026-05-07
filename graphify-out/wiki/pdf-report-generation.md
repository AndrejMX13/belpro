# PDF Report Generation

**Nodes:** 32 | **Cohesion:** 0.133 | **Internal edges:** 66

## Files & Symbols
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py` — 13 symbols (e.g. reports.py, monthly_summary(), ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py` — 6 symbols (e.g. report.py, VolunteerMonthlySummary, ...)
- `D:\Andrej\vsCode-workspace\BelPro\api\services\report_pdf.py` — 13 symbols (e.g. report_pdf.py, _esc(), ...)

## Bridges To Other Communities
### → API Data Models & Schemas (36 edges)
- EntryStatus --uses--> Reports router — monthly aggregation and PDF export endpoints. [INFERRED]
- LogEntry --uses--> Reports router — monthly aggregation and PDF export endpoints. [INFERRED]
- Manager --uses--> Reports router — monthly aggregation and PDF export endpoints. [INFERRED]
- Volunteer --uses--> Reports router — monthly aggregation and PDF export endpoints. [INFERRED]
- Reports router — monthly aggregation and PDF export endpoints. --uses--> SmtpNotConfiguredError [INFERRED]
  ... and 31 more
### → API Request Handlers (2 edges)
- str --calls--> send_monthly_reports() [INFERRED]
- send_monthly_reports() --calls--> send_email() [INFERRED]
### → Analytics Engine (2 edges)
- BaseModel --inherits--> VolunteerMonthlySummary [EXTRACTED]
- BaseModel --inherits--> MonthlyReportSummary [EXTRACTED]
### → Migration Config & Settings (1 edges)
- get_settings() --calls--> send_monthly_reports() [INFERRED]
