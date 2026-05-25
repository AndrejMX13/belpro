# log_entry_factory()

> 31 nodes · cohesion 0.10

## Key Concepts

- **log_entry_factory()** (39 connections) — `api/tests/conftest.py`
- **test_log_entries.py** (33 connections) — `api/tests/test_log_entries.py`
- **test_list_entries_returns_created_entry()** (3 connections) — `api/tests/test_log_entries.py`
- **test_list_entries_filter_by_status()** (3 connections) — `api/tests/test_log_entries.py`
- **test_update_entry_success()** (3 connections) — `api/tests/test_log_entries.py`
- **test_approve_pending_manager_entry()** (3 connections) — `api/tests/test_log_entries.py`
- **test_approve_already_approved_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_reject_pending_manager_entry()** (3 connections) — `api/tests/test_log_entries.py`
- **test_reject_approved_entry_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_confirm_pending_volunteer_entry()** (3 connections) — `api/tests/test_log_entries.py`
- **test_confirm_already_approved_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_status_cannot_go_from_approved_to_pending_manager()** (3 connections) — `api/tests/test_log_entries.py`
- **test_status_cannot_go_from_rejected_to_approved()** (3 connections) — `api/tests/test_log_entries.py`
- **test_delete_entry_happy_path()** (3 connections) — `api/tests/test_log_entries.py`
- **test_delete_pending_manager_entry_succeeds()** (3 connections) — `api/tests/test_log_entries.py`
- **test_delete_rejected_entry_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_delete_approved_entry_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_update_approved_entry_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_photo_upload_unsupported_extension_returns_400_or_422()** (3 connections) — `api/tests/test_log_entries.py`
- **test_approve_pending_volunteer_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_reject_pending_volunteer_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_photo_limit_returns_default()** (2 connections) — `api/tests/test_log_entries.py`
- **Returns an async callable that inserts a LogEntry row via flush.** (1 connections) — `api/tests/conftest.py`
- **test_list_entries_empty()** (1 connections) — `api/tests/test_log_entries.py`
- **test_get_entry_not_found()** (1 connections) — `api/tests/test_log_entries.py`
- *... and 6 more nodes in this community*

## Relationships

- [[volunteer_factory()]] (22 shared connections)
- [[str]] (8 shared connections)
- [[test_reports.py]] (7 shared connections)
- [[test_analytics.py]] (3 shared connections)
- [[path]] (2 shared connections)
- [[conftest.py]] (1 shared connections)
- [[persist_report()]] (1 shared connections)

## Source Files

- `api/tests/conftest.py`
- `api/tests/test_log_entries.py`

## Audit Trail

- EXTRACTED: 65 (46%)
- INFERRED: 75 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*