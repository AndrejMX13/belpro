# scripts/gen_diagrams.py

> 32 nodes

## Key Concepts

- **ops_server.py** (7 connections) — `ops/scripts/ops_server.py`
- **_Handler** (7 connections) — `ops/scripts/ops_server.py`
- **_Handler** (7 connections) — `whisper/transcribe.py`
- **write_crontab()** (5 connections) — `ops/scripts/ops_server.py`
- **.do_POST()** (5 connections) — `ops/scripts/ops_server.py`
- **._respond()** (5 connections) — `whisper/transcribe.py`
- **fetch_settings_from_db()** (4 connections) — `ops/scripts/ops_server.py`
- **._send()** (4 connections) — `ops/scripts/ops_server.py`
- **main()** (4 connections) — `ops/scripts/ops_server.py`
- **_dsn()** (3 connections) — `ops/scripts/ops_server.py`
- **report_error()** (3 connections) — `ops/scripts/ops_server.py`
- **reload_crond()** (3 connections) — `ops/scripts/ops_server.py`
- **.do_POST()** (3 connections) — `whisper/transcribe.py`
- **.do_GET()** (3 connections) — `whisper/transcribe.py`
- **BaseHTTPRequestHandler** (2 connections)
- **.do_GET()** (2 connections) — `ops/scripts/ops_server.py`
- **transcribe.py** (2 connections) — `whisper/transcribe.py`
- **.log_message()** (2 connections) — `whisper/transcribe.py`
- **.log_message()** (1 connections) — `ops/scripts/ops_server.py`
- **Convert asyncpg DATABASE_URL to a psycopg2-compatible DSN.** (1 connections) — `ops/scripts/ops_server.py`
- **POST failure to the API error log. Best-effort — never raises.** (1 connections) — `ops/scripts/ops_server.py`
- **Send SIGHUP to crond so it reloads the crontab file.** (1 connections) — `ops/scripts/ops_server.py`
- **Write a new crontab to CRONTAB_PATH and reload crond.** (1 connections) — `ops/scripts/ops_server.py`
- **Read all runtime-tunable settings from the settings table.      Returns an empty** (1 connections) — `ops/scripts/ops_server.py`
- **HTTP request handler for the ops notification server.** (1 connections) — `ops/scripts/ops_server.py`
- *... and 7 more nodes in this community*

## Relationships

- [[load_key()]] (3 shared connections)

## Source Files

- `ops/scripts/ops_server.py`
- `whisper/transcribe.py`

## Audit Trail

- EXTRACTED: 82 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*