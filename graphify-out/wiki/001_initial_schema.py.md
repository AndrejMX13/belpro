# 001_initial_schema.py

> 20 nodes

## Key Concepts

- **reports.js** (10 connections) — `frontend/js/reports.js`
- **loadReports()** (7 connections) — `frontend/js/reports.js`
- **renderReports()** (5 connections) — `frontend/js/reports.js`
- **renderReportsTable()** (5 connections) — `frontend/js/reports.js`
- **downloadHistoryPdf()** (4 connections) — `frontend/js/reports.js`
- **exportReportPdf()** (3 connections) — `frontend/js/reports.js`
- **loadReports()** (3 connections) — `frontend/js/reports.js`
- **GET /reports/monthly** (3 connections) — `api/routers/reports.py`
- **fmtHours()** (2 connections) — `frontend/js/reports.js`
- **API.reports.monthly()** (2 connections) — `frontend/js/api.js`
- **API.reports.exportPdf()** (2 connections) — `frontend/js/api.js`
- **API.reports.downloadHistoryPdf()** (2 connections) — `frontend/js/api.js`
- **POST /reports/monthly/pdf** (2 connections) — `api/routers/reports.py`
- **GET /reports/history/{id}/pdf** (2 connections) — `api/routers/reports.py`
- **MonthlyReportSummary shape (items[], total_hours, total_entries)** (2 connections) — `api/routers/reports.py`
- **SL_MONTHS** (1 connections) — `frontend/js/reports.js`
- **reportsState** (1 connections) — `frontend/js/reports.js`
- **exportReportPdf()** (1 connections) — `frontend/js/reports.js`
- **downloadHistoryPdf()** (1 connections) — `frontend/js/reports.js`
- **renderReports() — reports page** (1 connections) — `frontend/js/reports.js`

## Relationships

- [[make_text_payload()]] (11 shared connections)
- [[Community 550]] (1 shared connections)
- [[test_managers.py]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `frontend/js/api.js`
- `frontend/js/reports.js`

## Audit Trail

- EXTRACTED: 48 (81%)
- INFERRED: 11 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*