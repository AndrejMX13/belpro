# load_key()

> 71 nodes

## Key Concepts

- **volunteer_factory()** (57 connections) — `api/tests/conftest.py`
- **str** (39 connections)
- **log_entry_factory()** (39 connections) — `api/tests/conftest.py`
- **test_log_entries.py** (33 connections) — `api/tests/test_log_entries.py`
- **test_reports.py** (14 connections) — `api/tests/test_reports.py`
- **test_analytics.py** (7 connections) — `api/tests/test_analytics.py`
- **test_send_monthly_email_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_whatsapp_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_smtp_not_configured_does_not_abort_batch()** (5 connections) — `api/tests/test_reports.py`
- **test_analytics_rejected_hours_excluded()** (4 connections) — `api/tests/test_analytics.py`
- **test_analytics_all_rejected_returns_zero_hours()** (4 connections) — `api/tests/test_analytics.py`
- **test_list_entries_filter_by_volunteer()** (4 connections) — `api/tests/test_log_entries.py`
- **test_get_entry_found()** (4 connections) — `api/tests/test_log_entries.py`
- **test_with_entries_only_excludes_volunteers_with_no_entries()** (4 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_includes_any_status_not_only_approved()** (4 connections) — `api/tests/test_reports.py`
- **test_send_monthly_invalid_phone_logged()** (4 connections) — `api/tests/test_reports.py`
- **test_send_monthly_resend_overwrites_row()** (4 connections) — `api/tests/test_report_history.py`
- **test_analytics_summary_counts_approved_hours()** (3 connections) — `api/tests/test_analytics.py`
- **test_list_entries_returns_created_entry()** (3 connections) — `api/tests/test_log_entries.py`
- **test_list_entries_filter_by_status()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_success()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_inactive_volunteer_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_missing_required_field_returns_422()** (3 connections) — `api/tests/test_log_entries.py`
- **test_update_entry_success()** (3 connections) — `api/tests/test_log_entries.py`
- **test_approve_pending_manager_entry()** (3 connections) — `api/tests/test_log_entries.py`
- *... and 46 more nodes in this community*

## Relationships

- [[ops_server.py]] (13 shared connections)
- [[loadReports()]] (9 shared connections)
- [[volunteers.js]] (6 shared connections)
- [[errors.py]] (4 shared connections)
- [[BelPro System Specification]] (4 shared connections)
- [[Community 406]] (3 shared connections)
- [[volunteer.py]] (3 shared connections)
- [[Community 349]] (3 shared connections)
- [[n8n MCP Workflow Management Guide]] (2 shared connections)
- [[009_rename_entry_date_to_work_date.py]] (2 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (2 shared connections)
- [[Community 318]] (2 shared connections)

## Source Files

- `api/tests/conftest.py`
- `api/tests/test_analytics.py`
- `api/tests/test_log_entries.py`
- `api/tests/test_report_history.py`
- `api/tests/test_reports.py`
- `api/tests/test_volunteers.py`

## Audit Trail

- EXTRACTED: 132 (38%)
- INFERRED: 215 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*