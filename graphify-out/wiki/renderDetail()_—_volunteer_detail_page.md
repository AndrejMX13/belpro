# renderDetail() — volunteer detail page

> 27 nodes · cohesion 0.08

## Key Concepts

- **renderDetail() — volunteer detail page** (6 connections) — `frontend/js/volunteers.js`
- **renderList() — volunteers page** (5 connections) — `frontend/js/volunteers.js`
- **renderAdmin() — admin page** (4 connections) — `frontend/js/admin.js`
- **GET /volunteers** (4 connections) — `api/routers/volunteers.py`
- **GET /volunteers/{id}** (4 connections) — `api/routers/volunteers.py`
- **loadVolunteers()** (3 connections) — `frontend/js/volunteers.js`
- **loadHealthWidget()** (3 connections) — `frontend/js/errors.js`
- **GET /admin/settings** (3 connections) — `api/routers/admin.py`
- **API.volunteers.list()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.get()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.activate()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.deactivate()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.update()** (2 connections) — `frontend/js/api.js`
- **API.volunteers.delete()** (2 connections) — `frontend/js/api.js`
- **API.logEntries.create()** (2 connections) — `frontend/js/api.js`
- **API.admin.getSettings()** (2 connections) — `frontend/js/api.js`
- **API.admin.updateSettings()** (2 connections) — `frontend/js/api.js`
- **DELETE /volunteers/{id}** (2 connections) — `api/routers/volunteers.py`
- **PATCH /volunteers/{id}** (2 connections) — `api/routers/volunteers.py`
- **POST /log-entries** (2 connections) — `api/routers/log_entries.py`
- **PATCH /admin/settings** (2 connections) — `api/routers/admin.py`
- **VolunteerListResponse shape (items[], total)** (2 connections) — `api/routers/volunteers.py`
- **VolunteerDetailResponse shape (emso_masked, log_entries[], hours_this_month)** (2 connections) — `api/routers/volunteers.py`
- **AdminSettingsResponse shape (max_photos_per_entry, photo_retention_days, session_duration_hours, report_auto_day, report_auto_period, report_auto_hour, backup_hour, photo_cleanup_hour, backup_retention_days)** (2 connections) — `api/routers/admin.py`
- **API.health.detailed()** (1 connections) — `frontend/js/api.js`
- *... and 2 more nodes in this community*

## Relationships

- [[volunteers.js]] (9 shared connections)

## Source Files

- `api/routers/admin.py`
- `api/routers/log_entries.py`
- `api/routers/volunteers.py`
- `frontend/js/admin.js`
- `frontend/js/api.js`
- `frontend/js/errors.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 65 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*