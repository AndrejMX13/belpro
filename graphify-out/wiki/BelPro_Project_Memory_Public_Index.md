# BelPro Project Memory Public Index

> 40 nodes

## Key Concepts

- **LogEntry (ORM)** (22 connections) — `api/models/log_entry.py`
- **log_entries.py** (17 connections) — `api/routers/log_entries.py`
- **path** (17 connections) — `scripts/gen_architecture_docx.js`
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
- *... and 15 more nodes in this community*

## Relationships

- [[errors.py]] (8 shared connections)
- [[Code: Procesiraj Popravek]] (6 shared connections)
- [[analytics_summary()]] (6 shared connections)
- [[005_report_prefs.py]] (4 shared connections)
- [[Evolution API (API Gateway)]] (3 shared connections)
- [[Code: Preveri Slike Stanje]] (3 shared connections)
- [[send_monthly_reports()]] (3 shared connections)
- [[API.reports.downloadHistoryPdf()]] (2 shared connections)
- [[Porocila Page - Monthly Reports Overview]] (1 shared connections)
- [[Community 414]] (1 shared connections)
- [[PDF Generated (Per Volunteer + Consolidated)]] (1 shared connections)
- [[LoginRequest (Schema)]] (1 shared connections)

## Source Files

- `api/models/log_entry.py`
- `api/models/log_entry_photo.py`
- `api/routers/log_entries.py`
- `api/schemas/log_entry.py`
- `api/schemas/volunteer.py`
- `scripts/gen_architecture_docx.js`

## Audit Trail

- EXTRACTED: 163 (81%)
- INFERRED: 39 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*