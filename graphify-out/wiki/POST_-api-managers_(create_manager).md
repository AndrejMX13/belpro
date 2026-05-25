# POST /api/managers (create_manager)

> 12 nodes

## Key Concepts

- **get_report_history()** (5 connections) — `api/routers/reports.py`
- **report.py** (5 connections) — `api/schemas/report.py`
- **VolunteerMonthlySummary** (4 connections) — `api/schemas/report.py`
- **MonthlyReportSummary** (4 connections) — `api/schemas/report.py`
- **ReportHistoryItem** (4 connections) — `api/schemas/report.py`
- **ReportHistoryList** (4 connections) — `api/schemas/report.py`
- **List persisted PDF reports, newest first. Optionally filter by year and/or month** (1 connections) — `api/routers/reports.py`
- **Pydantic schemas for monthly report summaries.** (1 connections) — `api/schemas/report.py`
- **Per-volunteer aggregated totals for a given month.** (1 connections) — `api/schemas/report.py`
- **Aggregated monthly summary across all active volunteers.** (1 connections) — `api/schemas/report.py`
- **One persisted report record in the history list.** (1 connections) — `api/schemas/report.py`
- **List of persisted report records.** (1 connections) — `api/schemas/report.py`

## Relationships

- [[Porocila Page - Monthly Reports Overview]] (4 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (3 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/schemas/report.py`

## Audit Trail

- EXTRACTED: 25 (78%)
- INFERRED: 7 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*