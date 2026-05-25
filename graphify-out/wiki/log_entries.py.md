# log_entries.py

> 18 nodes · cohesion 0.12

## Key Concepts

- **log_entries.py** (17 connections) — `api/routers/log_entries.py`
- **update_log_entry()** (10 connections) — `api/routers/log_entries.py`
- **upload_photo_base64()** (10 connections) — `api/routers/log_entries.py`
- **upload_photo()** (9 connections) — `api/routers/log_entries.py`
- **delete_log_entry()** (7 connections) — `api/routers/log_entries.py`
- **_extract_exif()** (4 connections) — `api/routers/log_entries.py`
- **get_photo_file()** (4 connections) — `api/routers/log_entries.py`
- **delete_photo()** (4 connections) — `api/routers/log_entries.py`
- **get_photo_limit()** (2 connections) — `api/routers/log_entries.py`
- **Log entries CRUD router — volunteer work diary entries.** (1 connections) — `api/routers/log_entries.py`
- **Extract timestamp and GPS from image EXIF. All best-effort — never raises.** (1 connections) — `api/routers/log_entries.py`
- **Return the configured maximum photos per log entry. Used by n8n workflows.** (1 connections) — `api/routers/log_entries.py`
- **Update activity_description, hours, location, and/or work_date. Blocked once app** (1 connections) — `api/routers/log_entries.py`
- **Upload a photo for a log entry. Blocked if entry is approved.** (1 connections) — `api/routers/log_entries.py`
- **Upload a photo from a base64-encoded string. Used by n8n workflows.** (1 connections) — `api/routers/log_entries.py`
- **Serve a photo file with authentication.** (1 connections) — `api/routers/log_entries.py`
- **Delete a photo. Blocked if entry is approved.** (1 connections) — `api/routers/log_entries.py`
- **Delete a pending_volunteer or pending_manager log entry and its associated photo** (1 connections) — `api/routers/log_entries.py`

## Relationships

- [[Volunteer (ORM)]] (16 shared connections)
- [[Manager WhatsApp Approval Implementation Plan]] (4 shared connections)
- [[str]] (4 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (3 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (2 shared connections)
- [[Base]] (2 shared connections)
- [[path]] (2 shared connections)
- [[GET /api/log-entries (list_log_entries)]] (1 shared connections)
- [[get_log_entry()]] (1 shared connections)
- [[PATCH /api/log-entries/{id}/notify (notify_log_entry)]] (1 shared connections)
- [[Manager WhatsApp Approval Workflow Design]] (1 shared connections)
- [[PhotoBase64Request (Schema)]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`

## Audit Trail

- EXTRACTED: 66 (87%)
- INFERRED: 10 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*