# persist_report()

> 30 nodes · cohesion 0.09

## Key Concepts

- **persist_report()** (16 connections) — `api/services/report_storage.py`
- **test_report_history.py** (14 connections) — `api/tests/test_report_history.py`
- **test_persist_report_creates_file_and_row()** (5 connections) — `api/tests/test_report_history.py`
- **test_persist_report_overwrites_on_resend()** (5 connections) — `api/tests/test_report_history.py`
- **report_storage.py** (4 connections) — `api/services/report_storage.py`
- **report_path()** (4 connections) — `api/services/report_storage.py`
- **test_persist_report_consolidated_overwrites_on_resend()** (4 connections) — `api/tests/test_report_history.py`
- **test_get_history_returns_items()** (4 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_missing_file_returns_404()** (4 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_resend_overwrites_row()** (4 connections) — `api/tests/test_report_history.py`
- **test_persist_report_consolidated_has_null_volunteer()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_filter_by_year_month()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_streams_file()** (3 connections) — `api/tests/test_report_history.py`
- **test_get_history_empty()** (2 connections) — `api/tests/test_report_history.py`
- **test_get_history_pdf_unknown_id_returns_404()** (2 connections) — `api/tests/test_report_history.py`
- **PDF report storage — disk write and upsert of MonthlyReport rows.** (1 connections) — `api/services/report_storage.py`
- **Return the canonical filesystem path for a report PDF.** (1 connections) — `api/services/report_storage.py`
- **Write pdf_bytes to disk and upsert a MonthlyReport row.      If a row already ex** (1 connections) — `api/services/report_storage.py`
- **Tests for PDF report persistence and history endpoints.** (1 connections) — `api/tests/test_report_history.py`
- **persist_report() must write bytes to disk and insert a MonthlyReport row.** (1 connections) — `api/tests/test_report_history.py`
- **Consolidated report rows must have volunteer_id=None.** (1 connections) — `api/tests/test_report_history.py`
- **Second persist_report() for same (volunteer, year, month) must overwrite — no ne** (1 connections) — `api/tests/test_report_history.py`
- **Second persist_report() for consolidated (volunteer_id=None, year, month) must o** (1 connections) — `api/tests/test_report_history.py`
- **GET /reports/history with no rows returns empty list.** (1 connections) — `api/tests/test_report_history.py`
- **GET /reports/history returns one item per MonthlyReport row.** (1 connections) — `api/tests/test_report_history.py`
- *... and 5 more nodes in this community*

## Relationships

- [[path]] (6 shared connections)
- [[volunteer_factory()]] (4 shared connections)
- [[str]] (3 shared connections)
- [[send_monthly_reports()]] (2 shared connections)
- [[Base]] (1 shared connections)
- [[n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)]] (1 shared connections)
- [[log_entry_factory()]] (1 shared connections)

## Source Files

- `api/services/report_storage.py`
- `api/tests/test_report_history.py`

## Audit Trail

- EXTRACTED: 61 (66%)
- INFERRED: 31 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*