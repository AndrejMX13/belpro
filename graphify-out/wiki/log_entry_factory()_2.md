# log_entry_factory()

> God node · 39 connections · `api/tests/conftest.py`

**Community:** [[log_entry_factory()]]

## Connections by Relation

### calls
- [[test_send_monthly_email_failure_logged()]] `INFERRED`
- [[test_send_monthly_whatsapp_failure_logged()]] `INFERRED`
- [[test_send_monthly_smtp_not_configured_does_not_abort_batch()]] `INFERRED`
- [[test_send_monthly_persists_volunteer_pdf()]] `INFERRED`
- [[test_send_monthly_persists_consolidated_pdf()]] `INFERRED`
- [[test_analytics_rejected_hours_excluded()]] `INFERRED`
- [[test_analytics_all_rejected_returns_zero_hours()]] `INFERRED`
- [[test_photo_upload_respects_db_max_photos_setting()]] `INFERRED`
- [[test_photo_upload_base64_respects_db_max_photos_setting()]] `INFERRED`
- [[test_list_entries_filter_by_volunteer()]] `INFERRED`
- [[test_get_entry_found()]] `INFERRED`
- [[test_with_entries_only_excludes_volunteers_with_no_entries()]] `INFERRED`
- [[test_with_entries_only_includes_any_status_not_only_approved()]] `INFERRED`
- [[test_send_monthly_invalid_phone_logged()]] `INFERRED`
- [[test_send_monthly_resend_overwrites_row()]] `INFERRED`
- [[test_analytics_summary_counts_approved_hours()]] `INFERRED`
- [[test_list_entries_returns_created_entry()]] `INFERRED`
- [[test_list_entries_filter_by_status()]] `INFERRED`
- [[test_update_entry_success()]] `INFERRED`
- [[test_approve_pending_manager_entry()]] `INFERRED`

### contains
- [[conftest.py]] `EXTRACTED`

### rationale_for
- [[Returns an async callable that inserts a LogEntry row via flush.]] `EXTRACTED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*