# send_monthly_reports()

> 12 nodes · cohesion 0.23

## Key Concepts

- **send_monthly_reports()** (15 connections) — `api/routers/reports.py`
- **reports.py** (13 connections) — `api/routers/reports.py`
- **generate_monthly_pdf()** (7 connections) — `api/routers/reports.py`
- **_summary_items()** (6 connections) — `api/routers/reports.py`
- **logo_src()** (5 connections) — `api/services/logo.py`
- **monthly_summary()** (4 connections) — `api/routers/reports.py`
- **Reports router — monthly aggregation and PDF export endpoints.** (1 connections) — `api/routers/reports.py`
- **Return per-volunteer totals of approved entries for the given year/month.** (1 connections) — `api/routers/reports.py`
- **Run the monthly aggregation query and return per-volunteer summaries.** (1 connections) — `api/routers/reports.py`
- **Generate a monthly PDF report for one volunteer or all active volunteers.** (1 connections) — `api/routers/reports.py`
- **Generate monthly PDFs and deliver them via email and/or WhatsApp.      Default** (1 connections) — `api/routers/reports.py`
- **Return a data URI for the NGO logo, or None if no logo is uploaded.** (1 connections) — `api/services/logo.py`

## Relationships

- [[report_pdf.py]] (5 shared connections)
- [[get_report_history()]] (3 shared connections)
- [[EvolutionClient]] (3 shared connections)
- [[send_email()]] (2 shared connections)
- [[logo.py]] (2 shared connections)
- [[persist_report()]] (2 shared connections)
- [[NGOInfo]] (2 shared connections)
- [[path]] (1 shared connections)
- [[monthly_reports.json]] (1 shared connections)
- [[AppSettings]] (1 shared connections)
- [[Base]] (1 shared connections)
- [[normalize_phone()]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/services/logo.py`

## Audit Trail

- EXTRACTED: 37 (66%)
- INFERRED: 19 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*