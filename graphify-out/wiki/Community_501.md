# Community 501

> 7 nodes

## Key Concepts

- **main()** (6 connections) — `ops/scripts/photo_cleanup.py`
- **photo_cleanup.py** (3 connections) — `ops/scripts/photo_cleanup.py`
- **report_error()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **dsn_from_url()** (3 connections) — `ops/scripts/photo_cleanup.py`
- **POST failure to the API error log.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **Convert asyncpg DATABASE_URL to psycopg2 DSN.** (1 connections) — `ops/scripts/photo_cleanup.py`
- **Query approved entries older than retention cutoff, delete their photos and DB r** (1 connections) — `ops/scripts/photo_cleanup.py`

## Relationships

- [[005_report_prefs.py]] (1 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)

## Source Files

- `ops/scripts/photo_cleanup.py`

## Audit Trail

- EXTRACTED: 16 (89%)
- INFERRED: 2 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*