# Community 550

> 5 nodes

## Key Concepts

- **loadReportArchive()** (5 connections) — `frontend/js/reports.js`
- **GET /reports/history** (3 connections) — `api/routers/reports.py`
- **API.reports.history()** (2 connections) — `frontend/js/api.js`
- **loadReportArchive()** (2 connections) — `frontend/js/reports.js`
- **ReportHistoryList shape (items[], total)** (2 connections) — `api/routers/reports.py`

## Relationships

- [[make_text_payload()]] (3 shared connections)
- [[001_initial_schema.py]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `frontend/js/api.js`
- `frontend/js/reports.js`

## Audit Trail

- EXTRACTED: 11 (79%)
- INFERRED: 3 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*