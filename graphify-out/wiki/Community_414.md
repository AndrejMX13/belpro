# Community 414

> 8 nodes

## Key Concepts

- **GET /api/log-entries (list_log_entries)** (10 connections) — `api/routers/log_entries.py`
- **n8n: GET /api/log-entries?status=pending_manager (Post-Action Queue Check)** (2 connections) — `n8n/workflows/manager_approval.json`
- **analytics_summary** (2 connections) — `api/routers/analytics.py`
- **n8n: GET /api/log-entries?status=pending_manager (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/log-entries?status=pending_manager (Auto Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/log-entries?status=pending_manager (Get Notified Entry)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **GET /api/reports/monthly (monthly_summary)** (1 connections) — `api/routers/reports.py`
- **loadAnalytics** (1 connections) — `frontend/js/analytics.js`

## Relationships

- [[API.reports.downloadHistoryPdf()]] (2 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)
- [[010_monthly_reports_unique_idx.py]] (1 shared connections)
- [[PDF Generated (Per Volunteer + Consolidated)]] (1 shared connections)

## Source Files

- `api/routers/analytics.py`
- `api/routers/log_entries.py`
- `api/routers/reports.py`
- `frontend/js/analytics.js`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 14 (74%)
- INFERRED: 5 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*