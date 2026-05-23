# Community 46

> 14 nodes · cohesion 0.18

## Key Concepts

- **Base** (11 connections) — `api/models/base.py`
- **Base** (7 connections)
- **ErrorLog** (7 connections) — `api/models/error_log.py`
- **LogEntry** (7 connections) — `api/models/log_entry.py`
- **Manager** (7 connections) — `api/models/manager.py`
- **AppSetting** (6 connections) — `api/models/app_setting.py`
- **create_log_entry()** (3 connections) — `api/routers/log_entries.py`
- **DeclarativeBase** (1 connections)
- **One row per named setting. All values stored as TEXT.** (1 connections) — `api/models/app_setting.py`
- **Declarative base — import and subclass in every model.** (1 connections) — `api/models/base.py`
- **One row per operational failure. Written by API, n8n, and ops sidecar.** (1 connections) — `api/models/error_log.py`
- **Individual work diary entry submitted by a volunteer.** (1 connections) — `api/models/log_entry.py`
- **NGO manager.  Single row expected per deployment.** (1 connections) — `api/models/manager.py`
- **Create a new log entry.  Volunteer must exist and be active.** (1 connections) — `api/routers/log_entries.py`

## Relationships

- [[Community 38]] (9 shared connections)
- [[Community 33]] (4 shared connections)
- [[Community 13]] (2 shared connections)
- [[Community 50]] (2 shared connections)
- [[Community 23]] (1 shared connections)
- [[Community 57]] (1 shared connections)
- [[Community 69]] (1 shared connections)
- [[Community 55]] (1 shared connections)
- [[Community 61]] (1 shared connections)
- [[Community 11]] (1 shared connections)

## Source Files

- `api/models/app_setting.py`
- `api/models/base.py`
- `api/models/error_log.py`
- `api/models/log_entry.py`
- `api/models/manager.py`
- `api/routers/log_entries.py`

## Audit Trail

- EXTRACTED: 31 (56%)
- INFERRED: 24 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*