# loadReports()

> 20 nodes

## Key Concepts

- **logo.py** (9 connections) — `api/services/logo.py`
- **logo.py** (5 connections) — `api/routers/logo.py`
- **logo_src()** (5 connections) — `api/services/logo.py`
- **get_logo()** (4 connections) — `api/routers/logo.py`
- **upload_logo()** (4 connections) — `api/routers/logo.py`
- **remove_logo()** (4 connections) — `api/routers/logo.py`
- **logo_exists()** (4 connections) — `api/services/logo.py`
- **save_logo()** (4 connections) — `api/services/logo.py`
- **delete_logo()** (3 connections) — `api/services/logo.py`
- **_open_image()** (3 connections) — `api/services/logo.py`
- **Logo router — public GET + authenticated POST and DELETE.** (1 connections) — `api/routers/logo.py`
- **Return the NGO logo as PNG, or 404 if none has been uploaded.** (1 connections) — `api/routers/logo.py`
- **Upload or replace the NGO logo. Accepts JPEG, PNG, WebP, GIF, BMP, TIFF.** (1 connections) — `api/routers/logo.py`
- **Delete the current NGO logo.** (1 connections) — `api/routers/logo.py`
- **NGO logo file management.** (1 connections) — `api/services/logo.py`
- **Return True if a logo file is present on disk.** (1 connections) — `api/services/logo.py`
- **Remove the logo file if it exists. Silent if absent.** (1 connections) — `api/services/logo.py`
- **Validate, normalize to PNG, and persist logo bytes.      Accepts raster formats** (1 connections) — `api/services/logo.py`
- **Open image bytes with Pillow. Raises ValueError for unsupported or corrupt input** (1 connections) — `api/services/logo.py`
- **Return a data URI for the NGO logo, or None if no logo is uploaded.** (1 connections) — `api/services/logo.py`

## Relationships

- [[005_report_prefs.py]] (2 shared connections)
- [[GET /log-entries/{id}/photos/{pid}/file]] (2 shared connections)
- [[main()]] (2 shared connections)
- [[list_pending_entries.py]] (1 shared connections)

## Source Files

- `api/routers/logo.py`
- `api/services/logo.py`

## Audit Trail

- EXTRACTED: 40 (73%)
- INFERRED: 15 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*