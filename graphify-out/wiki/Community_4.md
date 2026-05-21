# Community 4

> 73 nodes · cohesion 0.07

## Key Concepts

- **BaseModel** (33 connections)
- **EvolutionClient** (20 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\services\evolution.py`
- **MonthlyReportSummary** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py`
- **ReportHistoryItem** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py`
- **ReportHistoryList** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py`
- **VolunteerMonthlySummary** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py`
- **Reports router — monthly aggregation and PDF export endpoints.** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Generate a monthly PDF report for one volunteer or all active volunteers.** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Generate monthly PDFs and deliver them via email and/or WhatsApp.      Default** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **List persisted PDF reports, newest first. Optionally filter by year and/or month** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Stream a previously generated PDF from disk. Returns 404 if the row or file is m** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Return per-volunteer totals of approved entries for the given year/month.** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Run the monthly aggregation query and return per-volunteer summaries.** (11 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **ConfigInfoResponse** (10 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **send_monthly_reports()** (10 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- **Analytics router — aggregated summary for the dashboard analytics page.** (9 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\analytics.py`
- **ManagerCreate** (9 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **ManagerResponse** (9 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **ManagerUpdate** (9 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **PasswordChangeRequest** (9 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **Return `count` consecutive (year, month) tuples ending at (year, month).** (8 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\analytics.py`
- **Return aggregated analytics data scoped to the given month.      Defaults to t** (8 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\analytics.py`
- **manager.py** (8 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- **Managers router — single-manager setup and profile.** (8 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\managers.py`
- **Change the manager password.  Verifies the current password before updating.** (8 connections) — `D:\Andrej\vsCode-workspace\BelPro\api\routers\managers.py`
- *... and 48 more nodes in this community*

## Relationships

- [[Community 0]] (1 shared connections)

## Source Files

- `D:\Andrej\vsCode-workspace\BelPro\api\routers\analytics.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\managers.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\analytics.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\schemas\report.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\services\evolution.py`
- `D:\Andrej\vsCode-workspace\BelPro\api\services\logo.py`

## Audit Trail

- EXTRACTED: 187 (42%)
- INFERRED: 256 (58%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*