# ops_server.py

> 47 nodes

## Key Concepts

- **path** (17 connections) — `scripts/gen_architecture_docx.js`
- **persist_report()** (16 connections) — `api/services/report_storage.py`
- **test_report_history.py** (14 connections) — `api/tests/test_report_history.py`
- **main()** (6 connections) — `ops/scripts/photo_cleanup.py`
- **test_persist_report_creates_file_and_row()** (5 connections) — `api/tests/test_report_history.py`
- **test_persist_report_overwrites_on_resend()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_volunteer_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_consolidated_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **download_history_pdf()** (4 connections) — `api/routers/reports.py`
- **report_storage.py** (4 connections) — `api/services/report_storage.py`
- **report_path()** (4 connections) — `api/services/report_storage.py`
- **test_persist_report_consolidated_overwrites_on_resend()** (4 connections) — `api/tests/test_report_history.py`
- **test_get_history_returns_items()** (4 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_missing_file_returns_404()** (4 connections) — `api/tests/test_report_history.py`
- **render()** (4 connections) — `scripts/render_diagrams.py`
- **test_persist_report_consolidated_has_null_volunteer()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_filter_by_year_month()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_streams_file()** (3 connections) — `api/tests/test_report_history.py`
- **photo_cleanup.py** (3 connections) — `ops/scripts/photo_cleanup.py`
- **report_error()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **dsn_from_url()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **main()** (3 connections) — `scripts/render_diagrams.py`
- **test_get_history_empty()** (2 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_unknown_id_returns_404()** (2 connections) — `api/tests/test_report_history.py`
- **render_diagrams.py** (2 connections) — `scripts/render_diagrams.py`
- *... and 22 more nodes in this community*

## Relationships

- [[load_key()]] (13 shared connections)
- [[Community 439]] (2 shared connections)
- [[n8n Set Node Pattern]] (2 shared connections)
- [[errors.py]] (2 shared connections)
- [[VolunteerUpdate]] (1 shared connections)
- [[POST /api/logo (upload_logo)]] (1 shared connections)
- [[BelPro System Specification]] (1 shared connections)
- [[Community 406]] (1 shared connections)
- [[EMŠO Encryption (AES-256-GCM at rest)]] (1 shared connections)
- [[GET /api/volunteers/{id} (get_volunteer)]] (1 shared connections)
- [[Community 318]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/services/report_storage.py`
- `api/tests/test_report_history.py`
- `ops/scripts/photo_cleanup.py`
- `scripts/gen_architecture_docx.js`
- `scripts/render_diagrams.py`

## Audit Trail

- EXTRACTED: 94 (63%)
- INFERRED: 56 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*