# 005_report_prefs.py

> 20 nodes

## Key Concepts

- **str** (39 connections)
- **test_reports.py** (14 connections) — `api/tests/test_reports.py`
- **test_send_monthly_smtp_not_configured_does_not_abort_batch()** (5 connections) — `api/tests/test_reports.py`
- **test_list_entries_filter_by_volunteer()** (4 connections) — `api/tests/test_log_entries.py`
- **test_get_entry_found()** (4 connections) — `api/tests/test_log_entries.py`
- **test_with_entries_only_excludes_volunteers_with_no_entries()** (4 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_includes_any_status_not_only_approved()** (4 connections) — `api/tests/test_reports.py`
- **test_send_monthly_invalid_phone_logged()** (4 connections) — `api/tests/test_reports.py`
- **test_create_entry_success()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_inactive_volunteer_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_missing_required_field_returns_422()** (3 connections) — `api/tests/test_log_entries.py`
- **test_monthly_summary_counts_only_approved_entries()** (3 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_false_includes_all_active_volunteers()** (3 connections) — `api/tests/test_reports.py`
- **test_create_entry_unknown_volunteer_returns_404()** (2 connections) — `api/tests/test_log_entries.py`
- **test_monthly_summary_empty()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_missing_params_returns_422()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_empty_month_returns_pdf_content_type()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_for_unknown_volunteer_returns_404()** (1 connections) — `api/tests/test_reports.py`
- **SmtpNotConfiguredError must NOT abort the batch — response is 200 with error in** (1 connections) — `api/tests/test_reports.py`
- **Volunteer with WhatsApp enabled but invalid phone gets an error log entry.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[test_documents.py]] (13 shared connections)
- [[path]] (12 shared connections)
- [[BelPro Project Memory Public Index]] (4 shared connections)
- [[Community 404]] (3 shared connections)
- [[analytics_summary()]] (3 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (2 shared connections)
- [[loadReports()]] (2 shared connections)
- [[IF: Should Notify? (Auto)]] (2 shared connections)
- [[012_settings_table.py]] (2 shared connections)
- [[Community 318]] (2 shared connections)
- [[list_pending_entries.py]] (2 shared connections)
- [[Maximum photos allowed per log entry.]] (2 shared connections)

## Source Files

- `api/tests/test_log_entries.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 35 (35%)
- INFERRED: 66 (65%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*