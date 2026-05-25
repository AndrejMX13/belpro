# path

> 29 nodes

## Key Concepts

- **volunteer_factory()** (57 connections) — `api/tests/conftest.py`
- **test_volunteers.py** (21 connections) — `api/tests/test_volunteers.py`
- **test_photo_upload_respects_db_max_photos_setting()** (4 connections) — `api/tests/test_app_settings.py`
- **test_photo_upload_base64_respects_db_max_photos_setting()** (4 connections) — `api/tests/test_app_settings.py`
- **test_get_volunteer_found()** (3 connections) — `api/tests/test_volunteers.py`
- **test_delete_volunteer_with_entries_returns_409()** (3 connections) — `api/tests/test_volunteers.py`
- **test_list_volunteers_returns_created_volunteer()** (2 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_duplicate_emso_returns_409()** (2 connections) — `api/tests/test_volunteers.py`
- **test_update_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **test_deactivate_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **test_activate_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **test_delete_volunteer_happy_path()** (2 connections) — `api/tests/test_volunteers.py`
- **test_check_emso_already_registered()** (2 connections) — `api/tests/test_volunteers.py`
- **test_emso_stored_encrypted()** (2 connections) — `api/tests/test_volunteers.py`
- **Returns an async callable that inserts a Volunteer row via flush (not commit)** (1 connections) — `api/tests/conftest.py`
- **upload_photo rejects a second photo when max_photos_per_entry is patched to 1 in** (1 connections) — `api/tests/test_app_settings.py`
- **upload_photo_base64 rejects a second photo when max_photos_per_entry is 1 in DB.** (1 connections) — `api/tests/test_app_settings.py`
- **test_list_volunteers_empty()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_success()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_missing_required_field_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_invalid_postal_code_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_invalid_emso_length_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_invalid_emso_checksum_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_get_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- **test_update_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- *... and 4 more nodes in this community*

## Relationships

- [[test_documents.py]] (22 shared connections)
- [[005_report_prefs.py]] (12 shared connections)
- [[analytics_summary()]] (6 shared connections)
- [[Community 349]] (4 shared connections)
- [[monthly_reports.json]] (3 shared connections)
- [[Maximum photos allowed per log entry.]] (2 shared connections)
- [[get_report_history()]] (1 shared connections)
- [[Community 405]] (1 shared connections)

## Source Files

- `api/tests/conftest.py`
- `api/tests/test_app_settings.py`
- `api/tests/test_volunteers.py`

## Audit Trail

- EXTRACTED: 53 (43%)
- INFERRED: 70 (57%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*