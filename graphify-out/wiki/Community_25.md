# Community 25

> 25 nodes · cohesion 0.11

## Key Concepts

- **volunteer_factory()** (52 connections) — `api/tests/conftest.py`
- **test_volunteers.py** (23 connections) — `api/tests/test_volunteers.py`
- **test_photo_upload_respects_db_max_photos_setting()** (4 connections) — `api/tests/test_app_settings.py`
- **test_delete_volunteer_with_entries_returns_409()** (3 connections) — `api/tests/test_volunteers.py`
- **test_get_volunteer_found()** (3 connections) — `api/tests/test_volunteers.py`
- **test_activate_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **test_check_emso_already_registered()** (2 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_duplicate_emso_returns_409()** (2 connections) — `api/tests/test_volunteers.py`
- **test_deactivate_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **test_delete_volunteer_happy_path()** (2 connections) — `api/tests/test_volunteers.py`
- **test_list_volunteers_returns_created_volunteer()** (2 connections) — `api/tests/test_volunteers.py`
- **test_update_volunteer_success()** (2 connections) — `api/tests/test_volunteers.py`
- **Returns an async callable that inserts a Volunteer row via flush (not commit)** (1 connections) — `api/tests/conftest.py`
- **upload_photo rejects a second photo when max_photos_per_entry is patched to 1 in** (1 connections) — `api/tests/test_app_settings.py`
- **test_check_emso_not_registered()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_invalid_emso_length_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_invalid_postal_code_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_missing_required_field_returns_422()** (1 connections) — `api/tests/test_volunteers.py`
- **test_create_volunteer_success()** (1 connections) — `api/tests/test_volunteers.py`
- **test_deactivate_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- **test_delete_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- **test_get_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- **test_list_volunteers_empty()** (1 connections) — `api/tests/test_volunteers.py`
- **test_update_volunteer_not_found()** (1 connections) — `api/tests/test_volunteers.py`
- **Creates a volunteer with a unique phone, yields the volunteer dict,     deletes** (1 connections) — `tests/workflow/conftest.py`

## Relationships

- [[Community 22]] (19 shared connections)
- [[Community 32]] (8 shared connections)
- [[Community 11]] (7 shared connections)
- [[Community 8]] (7 shared connections)
- [[Community 77]] (2 shared connections)
- [[Community 80]] (1 shared connections)
- [[Community 61]] (1 shared connections)
- [[Community 36]] (1 shared connections)
- [[Community 40]] (1 shared connections)
- [[Community 27]] (1 shared connections)

## Source Files

- `api/tests/conftest.py`
- `api/tests/test_app_settings.py`
- `api/tests/test_volunteers.py`
- `tests/workflow/conftest.py`

## Audit Trail

- EXTRACTED: 47 (42%)
- INFERRED: 65 (58%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*