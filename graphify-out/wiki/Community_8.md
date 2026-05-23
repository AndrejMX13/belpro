# Community 8

> 37 nodes · cohesion 0.07

## Key Concepts

- **path** (16 connections) — `scripts/gen_architecture_docx.js`
- **persist_report()** (15 connections) — `api/services/report_storage.py`
- **test_report_history.py** (14 connections) — `api/tests/test_report_history.py`
- **main()** (6 connections) — `ops/scripts/photo_cleanup.py`
- **test_persist_report_creates_file_and_row()** (5 connections) — `api/tests/test_report_history.py`
- **test_persist_report_overwrites_on_resend()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_consolidated_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_volunteer_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **report_path()** (4 connections) — `api/services/report_storage.py`
- **test_get_history_pdf_missing_file_returns_404()** (4 connections) — `api/tests/test_report_history.py`
- **test_get_history_returns_items()** (4 connections) — `api/tests/test_report_history.py`
- **test_persist_report_consolidated_overwrites_on_resend()** (4 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_resend_overwrites_row()** (4 connections) — `api/tests/test_report_history.py`
- **report_storage.py** (3 connections) — `api/services/report_storage.py`
- **test_get_history_filter_by_year_month()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_streams_file()** (3 connections) — `api/tests/test_report_history.py`
- **test_persist_report_consolidated_has_null_volunteer()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_empty()** (2 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_unknown_id_returns_404()** (2 connections) — `api/tests/test_report_history.py`
- **Query approved entries older than retention cutoff, delete their photos and DB r** (1 connections) — `ops/scripts/photo_cleanup.py`
- **PDF report storage — disk write and upsert of MonthlyReport rows.** (1 connections) — `api/services/report_storage.py`
- **Return the canonical filesystem path for a report PDF.** (1 connections) — `api/services/report_storage.py`
- **Write pdf_bytes to disk and upsert a MonthlyReport row.      If a row already ex** (1 connections) — `api/services/report_storage.py`
- **Tests for PDF report persistence and history endpoints.** (1 connections) — `api/tests/test_report_history.py`
- **Second persist_report() for consolidated (volunteer_id=None, year, month) must o** (1 connections) — `api/tests/test_report_history.py`
- *... and 12 more nodes in this community*

## Relationships

- [[Community 25]] (7 shared connections)
- [[Community 11]] (6 shared connections)
- [[Community 13]] (3 shared connections)
- [[Community 23]] (3 shared connections)
- [[Community 22]] (3 shared connections)
- [[Community 0]] (1 shared connections)
- [[Community 7]] (1 shared connections)
- [[Community 61]] (1 shared connections)
- [[Community 28]] (1 shared connections)
- [[Community 69]] (1 shared connections)

## Source Files

- `api/services/report_storage.py`
- `api/tests/test_report_history.py`
- `ops/scripts/photo_cleanup.py`
- `scripts/gen_architecture_docx.js`

## Audit Trail

- EXTRACTED: 72 (58%)
- INFERRED: 53 (42%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*