# errors.py

> 39 nodes

## Key Concepts

- **LogEntry (ORM)** (22 connections) — `api/models/log_entry.py`
- **log_entries.py** (17 connections) — `api/routers/log_entries.py`
- **EntryStatus (Enum)** (15 connections) — `api/models/log_entry.py`
- **LogEntryResponse (Schema)** (11 connections) — `api/schemas/log_entry.py`
- **upload_photo_base64()** (10 connections) — `api/routers/log_entries.py`
- **upload_photo()** (9 connections) — `api/routers/log_entries.py`
- **create_log_entry()** (8 connections) — `api/routers/log_entries.py`
- **LogEntryPhoto (ORM)** (8 connections) — `api/models/log_entry_photo.py`
- **list_log_entries()** (7 connections) — `api/routers/log_entries.py`
- **delete_log_entry()** (7 connections) — `api/routers/log_entries.py`
- **approve_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **reject_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **notify_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **confirm_log_entry()** (6 connections) — `api/routers/log_entries.py`
- **get_log_entry()** (5 connections) — `api/routers/log_entries.py`
- **_extract_exif()** (4 connections) — `api/routers/log_entries.py`
- **get_photo_file()** (4 connections) — `api/routers/log_entries.py`
- **delete_photo()** (4 connections) — `api/routers/log_entries.py`
- **PhotoResponse (Schema)** (4 connections) — `api/schemas/log_entry.py`
- **LogEntryCreate (Schema)** (3 connections) — `api/schemas/log_entry.py`
- **LogEntryBrief (Schema)** (3 connections) — `api/schemas/volunteer.py`
- **get_photo_limit()** (2 connections) — `api/routers/log_entries.py`
- **LogEntryListResponse (Schema)** (2 connections) — `api/schemas/log_entry.py`
- **Log entries CRUD router — volunteer work diary entries.** (1 connections) — `api/routers/log_entries.py`
- **Extract timestamp and GPS from image EXIF. All best-effort — never raises.** (1 connections) — `api/routers/log_entries.py`
- *... and 14 more nodes in this community*

## Relationships

- [[log_entries.py]] (8 shared connections)
- [[API.auth.logout()]] (6 shared connections)
- [[Volunteer (ORM)]] (5 shared connections)
- [[load_key()]] (4 shared connections)
- [[renderDetail() — volunteer detail page]] (3 shared connections)
- [[VolunteerUpdate]] (3 shared connections)
- [[scripts/setup.sh]] (3 shared connections)
- [[ops_server.py]] (2 shared connections)
- [[test_app_settings.py]] (1 shared connections)

## Source Files

- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/routers/log_entries.py`
- `api/schemas/log_entry.py`
- `api/schemas/volunteer.py`

## Audit Trail

- EXTRACTED: 162 (88%)
- INFERRED: 23 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*