# 012_settings_table.py

> 19 nodes

## Key Concepts

- **ops_server.py** (7 connections) — `ops/scripts/ops_server.py`
- **_Handler** (7 connections) — `ops/scripts/ops_server.py`
- **write_crontab()** (5 connections) — `ops/scripts/ops_server.py`
- **.do_POST()** (5 connections) — `ops/scripts/ops_server.py`
- **fetch_settings_from_db()** (4 connections) — `ops/scripts/ops_server.py`
- **._send()** (4 connections) — `ops/scripts/ops_server.py`
- **main()** (4 connections) — `ops/scripts/ops_server.py`
- **_dsn()** (3 connections) — `ops/scripts/ops_server.py`
- **report_error()** (3 connections) — `ops/scripts/ops_server.py`
- **reload_crond()** (3 connections) — `ops/scripts/ops_server.py`
- **.do_GET()** (2 connections) — `ops/scripts/ops_server.py`
- **.log_message()** (1 connections) — `ops/scripts/ops_server.py`
- **Convert asyncpg DATABASE_URL to a psycopg2-compatible DSN.** (1 connections) — `ops/scripts/ops_server.py`
- **POST failure to the API error log. Best-effort — never raises.** (1 connections) — `ops/scripts/ops_server.py`
- **Send SIGHUP to crond so it reloads the crontab file.** (1 connections) — `ops/scripts/ops_server.py`
- **Write a new crontab to CRONTAB_PATH and reload crond.** (1 connections) — `ops/scripts/ops_server.py`
- **Read all runtime-tunable settings from the settings table.      Returns an empty** (1 connections) — `ops/scripts/ops_server.py`
- **HTTP request handler for the ops notification server.** (1 connections) — `ops/scripts/ops_server.py`
- **Sync crontab with DB settings, then start the notification server.** (1 connections) — `ops/scripts/ops_server.py`

## Relationships

- [[005_report_prefs.py]] (2 shared connections)
- [[n8n Code Node Pattern]] (1 shared connections)

## Source Files

- `ops/scripts/ops_server.py`

## Audit Trail

- EXTRACTED: 53 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*