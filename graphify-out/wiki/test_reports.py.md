# test_reports.py

> 20 nodes · cohesion 0.11

## Key Concepts

- **test_reports.py** (14 connections) — `api/tests/test_reports.py`
- **SmtpNotConfiguredError** (5 connections) — `api/services/email.py`
- **Exception** (5 connections)
- **test_send_monthly_email_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_whatsapp_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_smtp_not_configured_does_not_abort_batch()** (5 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_excludes_volunteers_with_no_entries()** (4 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_includes_any_status_not_only_approved()** (4 connections) — `api/tests/test_reports.py`
- **test_send_monthly_invalid_phone_logged()** (4 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_counts_only_approved_entries()** (3 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_false_includes_all_active_volunteers()** (3 connections) — `api/tests/test_reports.py`
- **Raised when the manager has not configured SMTP.** (1 connections) — `api/services/email.py`
- **test_monthly_summary_empty()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_missing_params_returns_422()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_empty_month_returns_pdf_content_type()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_for_unknown_volunteer_returns_404()** (1 connections) — `api/tests/test_reports.py`
- **Email delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`
- **WhatsApp delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`
- **SmtpNotConfiguredError must NOT abort the batch — response is 200 with error in** (1 connections) — `api/tests/test_reports.py`
- **Volunteer with WhatsApp enabled but invalid phone gets an error log entry.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[volunteer_factory()]] (8 shared connections)
- [[log_entry_factory()]] (7 shared connections)
- [[str]] (3 shared connections)
- [[send_email()]] (2 shared connections)
- [[NGOInfo]] (2 shared connections)
- [[test_admin.py]] (1 shared connections)
- [[test_evolution_service.py]] (1 shared connections)

## Source Files

- `api/services/email.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 40 (61%)
- INFERRED: 26 (39%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*