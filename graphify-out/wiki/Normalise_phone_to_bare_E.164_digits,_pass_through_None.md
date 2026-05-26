# Normalise phone to bare E.164 digits, pass through None.

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

- [[007_add_ngo_davcna.py]] (4 shared connections)
- [[BelPro README (English)]] (2 shared connections)
- [[volunteers.js]] (1 shared connections)
- [[settings]] (1 shared connections)
- [[Performance Testing Reference (k6)]] (1 shared connections)
- [[Serena Project Configuration]] (1 shared connections)
- [[Node.js Essentials Reference]] (1 shared connections)

## Source Files

- `api/main.py`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*