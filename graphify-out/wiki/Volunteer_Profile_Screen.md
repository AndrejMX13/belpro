# Volunteer Profile Screen

> 23 nodes

## Key Concepts

- **test_logo.py** (18 connections) — `api/tests/test_logo.py`
- **_png_1x1()** (7 connections) — `api/tests/test_logo.py`
- **_ico_16x16()** (3 connections) — `api/tests/test_logo.py`
- **test_open_image_rejects_disallowed_format()** (3 connections) — `api/tests/test_logo.py`
- **_clean_logo()** (3 connections) — `api/tests/test_logo.py`
- **test_save_creates_png_on_disk()** (2 connections) — `api/tests/test_logo.py`
- **test_delete_removes_file()** (2 connections) — `api/tests/test_logo.py`
- **test_upload_logo_and_retrieve()** (2 connections) — `api/tests/test_logo.py`
- **test_upload_logo_requires_auth()** (2 connections) — `api/tests/test_logo.py`
- **test_delete_logo()** (2 connections) — `api/tests/test_logo.py`
- **test_logo_not_exists_initially()** (1 connections) — `api/tests/test_logo.py`
- **test_delete_when_no_logo_is_silent()** (1 connections) — `api/tests/test_logo.py`
- **test_open_image_rejects_corrupt_bytes()** (1 connections) — `api/tests/test_logo.py`
- **test_save_overwrites_existing_logo()** (1 connections) — `api/tests/test_logo.py`
- **test_get_logo_returns_404_when_absent()** (1 connections) — `api/tests/test_logo.py`
- **test_upload_invalid_logo_returns_422()** (1 connections) — `api/tests/test_logo.py`
- **test_delete_logo_when_absent_returns_404()** (1 connections) — `api/tests/test_logo.py`
- **test_delete_logo_requires_auth()** (1 connections) — `api/tests/test_logo.py`
- **Tests for NGO logo service and endpoints.** (1 connections) — `api/tests/test_logo.py`
- **Minimal valid 1×1 PNG.** (1 connections) — `api/tests/test_logo.py`
- **Minimal valid 16×16 ICO — openable by Pillow but not in allowed list.** (1 connections) — `api/tests/test_logo.py`
- **ICO is openable by Pillow but excluded from the allowed set.** (1 connections) — `api/tests/test_logo.py`
- **Redirect logo operations to a temporary directory — never touches the real logo** (1 connections) — `api/tests/test_logo.py`

## Relationships

- [[test_auth.py]] (1 shared connections)

## Source Files

- `api/tests/test_logo.py`

## Audit Trail

- EXTRACTED: 56 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*