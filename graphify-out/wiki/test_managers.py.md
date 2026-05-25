# test_managers.py

> 32 nodes

## Key Concepts

- **renderLogEntryDetail()** (18 connections) — `frontend/js/volunteers.js`
- **route()** (14 connections) — `frontend/js/volunteers.js`
- **renderDetail()** (14 connections) — `frontend/js/volunteers.js`
- **renderDetail() — volunteer detail page** (6 connections) — `frontend/js/volunteers.js`
- **GET /volunteers/{id}** (4 connections) — `api/routers/volunteers.py`
- **fmtHours()** (3 connections) — `frontend/js/volunteers.js`
- **fmtDatetime()** (3 connections) — `frontend/js/volunteers.js`
- **PATCH /log-entries/{id}/approve** (3 connections) — `api/routers/log_entries.py`
- **PATCH /log-entries/{id}/reject** (3 connections) — `api/routers/log_entries.py`
- **revokePhotoUrls()** (2 connections) — `frontend/js/volunteers.js`
- **API.volunteers.get()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.update()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.delete()** (2 connections) — `frontend/js/api.js`
- **API.logEntries.create()** (2 connections) — `frontend/js/api.js`
- **DELETE /volunteers/{id}** (2 connections) — `api/routers/volunteers.py`
- **PATCH /volunteers/{id}** (2 connections) — `api/routers/volunteers.py`
- **POST /log-entries** (2 connections) — `api/routers/log_entries.py`
- **GET /log-entries/{id}** (2 connections) — `api/routers/log_entries.py`
- **PATCH /log-entries/{id}** (2 connections) — `api/routers/log_entries.py`
- **DELETE /log-entries/{id}** (2 connections) — `api/routers/log_entries.py`
- **POST /log-entries/{id}/photos** (2 connections) — `api/routers/log_entries.py`
- **GET /log-entries/{id}/photos/{pid}/file** (2 connections) — `api/routers/log_entries.py`
- **DELETE /log-entries/{id}/photos/{pid}** (2 connections) — `api/routers/log_entries.py`
- **VolunteerDetailResponse shape (emso_masked, log_entries[], hours_this_month)** (2 connections) — `api/routers/volunteers.py`
- **API.logEntries.get()** (1 connections) — `frontend/js/api.js`
- *... and 7 more nodes in this community*

## Relationships

- [[make_text_payload()]] (21 shared connections)
- [[loadReports()]] (3 shared connections)
- [[__init__.py]] (2 shared connections)
- [[Community 358]] (1 shared connections)
- [[Day of month (1–28) on which monthly reports are auto-sent.]] (1 shared connections)
- [[001_initial_schema.py]] (1 shared connections)
- [[API.health.basic()]] (1 shared connections)

## Source Files

- `api/routers/log_entries.py`
- `api/routers/volunteers.py`
- `frontend/js/api.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 99 (93%)
- INFERRED: 7 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*