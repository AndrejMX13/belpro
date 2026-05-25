# loadAppLog()

> 21 nodes

## Key Concepts

- **upgrade.sh** (12 connections) — `scripts/upgrade.sh`
- **rotate_emso_key.sh** (11 connections) — `scripts/rotate_emso_key.sh`
- **backup.sh** (8 connections) — `scripts/backup.sh`
- **.env** (5 connections)
- **EMSO encrypted field** (4 connections)
- **docker-compose.yml** (3 connections)
- **api/scripts/rotate_emso_key.py** (3 connections)
- **Alembic migrations** (2 connections)
- **/app/photos (volume)** (2 connections)
- **info()** (1 connections) — `scripts/rotate_emso_key.sh`
- **ok()** (1 connections) — `scripts/rotate_emso_key.sh`
- **warn()** (1 connections) — `scripts/rotate_emso_key.sh`
- **heading()** (1 connections) — `scripts/rotate_emso_key.sh`
- **die()** (1 connections) — `scripts/rotate_emso_key.sh`
- **info()** (1 connections) — `scripts/upgrade.sh`
- **ok()** (1 connections) — `scripts/upgrade.sh`
- **warn()** (1 connections) — `scripts/upgrade.sh`
- **heading()** (1 connections) — `scripts/upgrade.sh`
- **die()** (1 connections) — `scripts/upgrade.sh`
- **get_env()** (1 connections) — `scripts/upgrade.sh`
- **backups/** (1 connections)

## Relationships

- [[005_report_prefs.py]] (10 shared connections)
- [[merge_ast_semantic.py]] (1 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (1 shared connections)

## Source Files

- `scripts/backup.sh`
- `scripts/rotate_emso_key.sh`
- `scripts/upgrade.sh`

## Audit Trail

- EXTRACTED: 62 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*