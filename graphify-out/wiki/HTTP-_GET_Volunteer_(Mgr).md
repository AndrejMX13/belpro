# HTTP: GET Volunteer (Mgr)

> 15 nodes

## Key Concepts

- **main.py** (22 connections) — `api/main.py`
- **lifespan()** (4 connections) — `api/main.py`
- **health()** (2 connections) — `api/main.py`
- **Belpro FastAPI application entry point.** (1 connections) — `api/main.py`
- **Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null.** (1 connections) — `api/main.py`
- **Health check — returns ok when the service is up.** (1 connections) — `api/main.py`
- **routers/admin** (1 connections)
- **routers/auth** (1 connections)
- **routers/analytics** (1 connections)
- **routers/log_entries** (1 connections)
- **routers/volunteers** (1 connections)
- **routers/reports** (1 connections)
- **models/log_entry** (1 connections)
- **models/manager** (1 connections)
- **models/monthly_report** (1 connections)

## Relationships

- [[004_log_entry_photos.py]] (4 shared connections)
- [[001_initial_schema.py]] (2 shared connections)
- [[monthly_reports.json]] (2 shared connections)
- [[n8n Set Node Pattern]] (1 shared connections)
- [[loadAnalytics()]] (1 shared connections)
- [[API.logo.upload()]] (1 shared connections)
- [[PATCH /log-entries/{id}]] (1 shared connections)

## Source Files

- `api/main.py`

## Audit Trail

- EXTRACTED: 39 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*