# analytics_summary()

> 34 nodes

## Key Concepts

- **persist_report()** (16 connections) — `api/services/report_storage.py`
- **test_report_history.py** (14 connections) — `api/tests/test_report_history.py`
- **test_persist_report_creates_file_and_row()** (5 connections) — `api/tests/test_report_history.py`
- **test_persist_report_overwrites_on_resend()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_volunteer_pdf()** (5 connections) — `api/tests/test_report_history.py`
- **test_send_monthly_persists_consolidated_pdf()** (5 connections) — `api/tests/test_report_history.py`
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
- *... and 9 more nodes in this community*

## Relationships

- [[BelPro Project Memory Public Index]] (6 shared connections)
- [[path]] (6 shared connections)
- [[005_report_prefs.py]] (3 shared connections)
- [[test_documents.py]] (3 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (2 shared connections)
- [[Evolution API (API Gateway)]] (1 shared connections)
- [[LoginRequest (Schema)]] (1 shared connections)

## Source Files

- `api/services/report_storage.py`
- `api/tests/test_report_history.py`

## Audit Trail

- EXTRACTED: 67 (64%)
- INFERRED: 37 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*