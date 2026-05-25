# AppSettings — Runtime-Tunable Configuration (DB-first, env-fallback)

> 37 nodes

## Key Concepts

- **make_text_payload()** (12 connections) — `tests/workflow/helpers.py`
- **post_to_webhook()** (11 connections) — `tests/workflow/helpers.py`
- **poll_for_entry()** (10 connections) — `tests/workflow/helpers.py`
- **make_response_payload()** (8 connections) — `tests/workflow/helpers.py`
- **test_edit_path()** (8 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_volunteer_entry.py** (7 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_happy_path_text_confirm()** (7 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_cancel_path()** (7 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_add_photos_then_confirm()** (7 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_add_photos_then_cancel()** (7 connections) — `tests/workflow/test_volunteer_entry.py`
- **helpers.py** (6 connections) — `tests/workflow/helpers.py`
- **poll_for_entry_status()** (5 connections) — `tests/workflow/helpers.py`
- **poll_for_entry_gone()** (5 connections) — `tests/workflow/helpers.py`
- **test_photo_upload.py** (5 connections) — `tests/workflow/test_photo_upload.py`
- **test_upload_photo_happy_path()** (5 connections) — `tests/workflow/test_photo_upload.py`
- **test_upload_second_photo_increments_count()** (5 connections) — `tests/workflow/test_photo_upload.py`
- **test_upload_photo_bad_extension()** (5 connections) — `tests/workflow/test_photo_upload.py`
- **test_unknown_volunteer_creates_no_entry()** (4 connections) — `tests/workflow/test_volunteer_entry.py`
- **test_upload_photo_unknown_entry()** (3 connections) — `tests/workflow/test_photo_upload.py`
- **Build a WhatsApp text-message webhook body for the given bare-digit phone.** (1 connections) — `tests/workflow/helpers.py`
- **Build a volunteer response payload. response_type must be one of:     'confirm'** (1 connections) — `tests/workflow/helpers.py`
- **POST a WhatsApp event to the n8n webhook. Asserts 200.** (1 connections) — `tests/workflow/helpers.py`
- **Poll GET /api/log-entries until at least one entry for volunteer_id appears.** (1 connections) — `tests/workflow/helpers.py`
- **Poll GET /api/log-entries/{entry_id} until its status matches expected_status.** (1 connections) — `tests/workflow/helpers.py`
- **Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError** (1 connections) — `tests/workflow/helpers.py`
- *... and 12 more nodes in this community*

## Relationships

- [[load_key()]] (1 shared connections)

## Source Files

- `tests/workflow/helpers.py`
- `tests/workflow/test_photo_upload.py`
- `tests/workflow/test_volunteer_entry.py`

## Audit Trail

- EXTRACTED: 70 (48%)
- INFERRED: 75 (52%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*