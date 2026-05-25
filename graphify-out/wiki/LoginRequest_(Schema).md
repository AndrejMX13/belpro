# LoginRequest (Schema)

> 11 nodes

## Key Concepts

- **PATCH /api/log-entries/{id}/notify (notify_log_entry)** (8 connections) — `api/routers/log_entries.py`
- **Shared LogEntry Data Structure (volunteer_id, work_date, hours, activity_description, location, status, raw_transcript)** (8 connections) — `api/routers/log_entries.py`
- **n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)** (7 connections) — `n8n/workflows/monthly_reports.json`
- **POST /api/reports/send-monthly (send_monthly_reports)** (3 connections) — `api/routers/reports.py`
- **BelPro - Mesecna Porocila (Monthly Reports Workflow)** (2 connections) — `n8n/workflows/monthly_reports.json`
- **POST /api/log-entries/{id}/photos/base64 (upload_photo_base64)** (2 connections) — `api/routers/log_entries.py`
- **n8n: PATCH /api/log-entries/{id}/notify (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: PATCH /api/log-entries/{id}/notify (Auto Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: POST /api/log-entries/{id}/photos/base64 (Photo Upload)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: PATCH /api/log-entries/{id}/notify (Next Entry Notify)** (1 connections) — `n8n/workflows/manager_approval.json`
- **GET /api/log-entries/photo-limit (get_photo_limit)** (1 connections) — `api/routers/log_entries.py`

## Relationships

- [[Code: Preveri Slike Stanje]] (3 shared connections)
- [[API.reports.downloadHistoryPdf()]] (3 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (2 shared connections)
- [[Community 435]] (1 shared connections)
- [[list_pending_entries.py]] (1 shared connections)
- [[analytics_summary()]] (1 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)
- [[PDF Generated (Per Volunteer + Consolidated)]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `api/routers/reports.py`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/monthly_reports.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 28 (80%)
- INFERRED: 7 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*