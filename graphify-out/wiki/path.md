# path

> 14 nodes · cohesion 0.16

## Key Concepts

- **path** (16 connections) — `scripts/gen_architecture_docx.js`
- **main()** (6 connections) — `ops/scripts/photo_cleanup.py`
- **test_send_monthly_persists_volunteer_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_consolidated_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **download_history_pdf()** (4 connections) — `api/routers/reports.py`
- **photo_cleanup.py** (3 connections) — `ops/scripts/photo_cleanup.py`
- **report_error()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **dsn_from_url()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **Stream a previously generated PDF from disk. Returns 404 if the row or file is m** (1 connections) — `api/routers/reports.py`
- **send_monthly_reports must persist one MonthlyReport row per volunteer PDF.** (1 connections) — `api/tests/test_report_history.py`
- **send_monthly_reports must persist a consolidated MonthlyReport row when manager** (1 connections) — `api/tests/test_report_history.py`
- **POST failure to the API error log.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **Convert asyncpg DATABASE_URL to psycopg2 DSN.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **Query approved entries older than retention cutoff, delete their photos and DB r** (1 connections) — `ops/scripts/photo_cleanup.py`

## Relationships

- [[persist_report()]] (6 shared connections)
- [[str]] (3 shared connections)
- [[volunteer_factory()]] (2 shared connections)
- [[log_entry_factory()]] (2 shared connections)
- [[log_entries.py]] (2 shared connections)
- [[send_monthly_reports()]] (1 shared connections)
- [[get_report_history()]] (1 shared connections)
- [[load_key()]] (1 shared connections)
- [[conftest.py]] (1 shared connections)
- [[test_logo.py]] (1 shared connections)
- [[gen_architecture_docx.js]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/tests/test_report_history.py`
- `ops/scripts/photo_cleanup.py`
- `scripts/gen_architecture_docx.js`

## Audit Trail

- EXTRACTED: 26 (51%)
- INFERRED: 25 (49%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*