# settings.local.json

> 21 nodes

## Key Concepts

- **test_errors.py** (11 connections) — `api/tests/test_errors.py`
- **_internal_header()** (7 connections) — `api/tests/test_errors.py`
- **test_post_error_valid_internal_key()** (3 connections) — `api/tests/test_errors.py`
- **test_get_errors_returns_list()** (3 connections) — `api/tests/test_errors.py`
- **test_get_errors_filter_unacknowledged()** (3 connections) — `api/tests/test_errors.py`
- **test_acknowledge_error()** (3 connections) — `api/tests/test_errors.py`
- **test_unacknowledged_count()** (3 connections) — `api/tests/test_errors.py`
- **test_post_error_missing_key_rejected()** (2 connections) — `api/tests/test_errors.py`
- **test_post_error_wrong_key_rejected()** (2 connections) — `api/tests/test_errors.py`
- **test_get_errors_requires_manager_auth()** (2 connections) — `api/tests/test_errors.py`
- **test_acknowledge_nonexistent_returns_404()** (2 connections) — `api/tests/test_errors.py`
- **Tests for POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge.** (1 connections) — `api/tests/test_errors.py`
- **POST with valid internal key creates a record.** (1 connections) — `api/tests/test_errors.py`
- **POST without internal key is rejected.** (1 connections) — `api/tests/test_errors.py`
- **POST with wrong internal key is rejected.** (1 connections) — `api/tests/test_errors.py`
- **GET /api/errors without manager auth is rejected.** (1 connections) — `api/tests/test_errors.py`
- **GET returns all error log entries, newest first.** (1 connections) — `api/tests/test_errors.py`
- **GET ?unacknowledged=true filters to unacknowledged only.** (1 connections) — `api/tests/test_errors.py`
- **PATCH /{id}/acknowledge sets acknowledged to True.** (1 connections) — `api/tests/test_errors.py`
- **PATCH /{id}/acknowledge on unknown id returns 404.** (1 connections) — `api/tests/test_errors.py`
- **GET /api/errors/unacknowledged-count returns integer count.** (1 connections) — `api/tests/test_errors.py`

## Relationships

- [[monthly_reports.json]] (1 shared connections)

## Source Files

- `api/tests/test_errors.py`

## Audit Trail

- EXTRACTED: 50 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*