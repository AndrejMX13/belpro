# Maximum photos allowed per log entry.

> 14 nodes

## Key Concepts

- **test_evolution_service.py** (6 connections) — `api/tests/test_evolution_service.py`
- **Exception** (5 connections)
- **_make_mock_http()** (5 connections) — `api/tests/test_evolution_service.py`
- **test_send_monthly_email_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_send_monthly_whatsapp_failure_logged()** (5 connections) — `api/tests/test_reports.py`
- **test_patch_settings_ops_failure_does_not_break_save()** (3 connections) — `api/tests/test_admin.py`
- **test_connected_returns_normalized_phone_and_open_state()** (2 connections) — `api/tests/test_evolution_service.py`
- **test_disconnected_returns_none_and_close_state()** (2 connections) — `api/tests/test_evolution_service.py`
- **test_network_error_returns_unreachable()** (2 connections) — `api/tests/test_evolution_service.py`
- **test_lid_jid_returns_lid_unsupported()** (2 connections) — `api/tests/test_evolution_service.py`
- **test_instance_not_in_response_returns_close()** (2 connections) — `api/tests/test_evolution_service.py`
- **PATCH /api/admin/settings still returns 200 when ops service is unreachable.** (1 connections) — `api/tests/test_admin.py`
- **Email delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`
- **WhatsApp delivery failure writes an ErrorLog row and appears in response errors.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[path]] (2 shared connections)
- [[test_documents.py]] (2 shared connections)
- [[005_report_prefs.py]] (2 shared connections)
- [[Community 435]] (1 shared connections)
- [[log_entries.py]] (1 shared connections)

## Source Files

- `api/tests/test_admin.py`
- `api/tests/test_evolution_service.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 30 (71%)
- INFERRED: 12 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*