# Community 618

> 4 nodes

## Key Concepts

- **POST /reports/send-monthly** (3 connections) — `api/routers/reports.py`
- **API.reports.sendMonthly()** (2 connections) — `frontend/js/api.js`
- **sendReports()** (2 connections) — `frontend/js/reports.js`
- **send-monthly JSON response (sent_via_email[], sent_via_whatsapp[], skipped_no_entries[], skipped_no_channel[], manager_email_sent, manager_whatsapp_sent, errors[])** (2 connections) — `api/routers/reports.py`

## Relationships

- [[make_text_payload()]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `frontend/js/api.js`
- `frontend/js/reports.js`

## Audit Trail

- EXTRACTED: 9 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*