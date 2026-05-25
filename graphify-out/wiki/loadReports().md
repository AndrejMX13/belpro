# loadReports()

> 5 nodes · cohesion 0.50

## Key Concepts

- **loadReports()** (3 connections) — `frontend/js/reports.js`
- **GET /reports/monthly** (3 connections) — `api/routers/reports.py`
- **API.reports.monthly()** (2 connections) — `frontend/js/api.js`
- **MonthlyReportSummary shape (items[], total_hours, total_entries)** (2 connections) — `api/routers/reports.py`
- **renderReports() — reports page** (1 connections) — `frontend/js/reports.js`

## Relationships

- [[volunteers.js]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `frontend/js/api.js`
- `frontend/js/reports.js`

## Audit Trail

- EXTRACTED: 11 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*