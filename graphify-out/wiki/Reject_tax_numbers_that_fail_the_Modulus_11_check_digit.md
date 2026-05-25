# Reject tax numbers that fail the Modulus 11 check digit.

> 14 nodes

## Key Concepts

- **main.py** (22 connections) — `api/main.py`
- **health()** (3 connections) — `api/main.py`
- **Belpro FastAPI application entry point.** (1 connections) — `api/main.py`
- **Health check — returns ok when the service is up.** (1 connections) — `api/main.py`
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

- [[005_report_prefs.py]] (4 shared connections)
- [[GET /api/log-entries (list_log_entries)]] (2 shared connections)
- [[volunteers.js]] (1 shared connections)
- [[merge_ast_semantic.py]] (1 shared connections)
- [[loadAppLog()]] (1 shared connections)
- [[008_add_manager_notified_at.py]] (1 shared connections)
- [[API.logo.delete()]] (1 shared connections)

## Source Files

- `api/main.py`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*