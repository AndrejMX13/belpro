# GET /log-entries/{id}/photos/{pid}/file

> 18 nodes

## Key Concepts

- **send_monthly_reports()** (15 connections) — `api/routers/reports.py`
- **reports.py** (13 connections) — `api/routers/reports.py`
- **EvolutionClient** (7 connections) — `api/services/evolution.py`
- **_summary_items()** (6 connections) — `api/routers/reports.py`
- **monthly_summary()** (4 connections) — `api/routers/reports.py`
- **download_history_pdf()** (4 connections) — `api/routers/reports.py`
- **.send_document()** (4 connections) — `api/services/evolution.py`
- **.get_connected_phone()** (3 connections) — `api/services/evolution.py`
- **evolution.py** (2 connections) — `api/services/evolution.py`
- **Reports router — monthly aggregation and PDF export endpoints.** (1 connections) — `api/routers/reports.py`
- **Return per-volunteer totals of approved entries for the given year/month.** (1 connections) — `api/routers/reports.py`
- **Run the monthly aggregation query and return per-volunteer summaries.** (1 connections) — `api/routers/reports.py`
- **Generate monthly PDFs and deliver them via email and/or WhatsApp.      Default** (1 connections) — `api/routers/reports.py`
- **Stream a previously generated PDF from disk. Returns 404 if the row or file is m** (1 connections) — `api/routers/reports.py`
- **.__init__()** (1 connections) — `api/services/evolution.py`
- **Async HTTP client for the Evolution API WhatsApp gateway.** (1 connections) — `api/services/evolution.py`
- **Return (normalized_phone, state) for the configured instance.          States: "** (1 connections) — `api/services/evolution.py`
- **Send a PDF document to a WhatsApp number via Evolution API sendMedia.** (1 connections) — `api/services/evolution.py`

## Relationships

- [[list_pending_entries.py]] (6 shared connections)
- [[POST /api/managers (create_manager)]] (3 shared connections)
- [[Community 435]] (2 shared connections)
- [[loadReports()]] (2 shared connections)
- [[analytics_summary()]] (2 shared connections)
- [[Normalise phone to bare E.164 digits, pass through None.]] (2 shared connections)
- [[LoginRequest (Schema)]] (2 shared connections)
- [[Settings Table ISS-026 Design]] (1 shared connections)
- [[monthly_reports.json]] (1 shared connections)
- [[Evolution API (API Gateway)]] (1 shared connections)
- [[005_report_prefs.py]] (1 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/services/evolution.py`

## Audit Trail

- EXTRACTED: 49 (73%)
- INFERRED: 18 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*