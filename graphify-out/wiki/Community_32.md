# Community 32

> 20 nodes · cohesion 0.11

## Key Concepts

- **test_reports.py** (13 connections) — `api/tests/test_reports.py`
- **Exception** (5 connections)
- **SmtpNotConfiguredError** (5 connections) — `api/services/email.py`
- **test_send_monthly_email_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_smtp_not_configured_does_not_abort_batch()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_whatsapp_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_invalid_phone_logged()** (4 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_excludes_volunteers_with_no_entries()** (4 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_includes_any_status_not_only_approved()** (4 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_counts_only_approved_entries()** (3 connections) — `api/tests/test_reports.py`
- **test_with_entries_only_false_includes_all_active_volunteers()** (3 connections) — `api/tests/test_reports.py`
- **Raised when the manager has not configured SMTP.** (1 connections) — `api/services/email.py`
- **Email delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`
- **WhatsApp delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`
- **SmtpNotConfiguredError must NOT abort the batch — response is 200 with error in** (1 connections) — `api/tests/test_reports.py`
- **Volunteer with WhatsApp enabled but invalid phone gets an error log entry.** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_empty_month_returns_pdf_content_type()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_pdf_for_unknown_volunteer_returns_404()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_empty()** (1 connections) — `api/tests/test_reports.py`
- **test_monthly_summary_missing_params_returns_422()** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[Community 25]] (8 shared connections)
- [[Community 22]] (7 shared connections)
- [[Community 11]] (3 shared connections)
- [[Community 79]] (2 shared connections)
- [[Community 86]] (1 shared connections)
- [[Community 20]] (1 shared connections)
- [[Community 76]] (1 shared connections)

## Source Files

- `api/services/email.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 39 (60%)
- INFERRED: 26 (40%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*