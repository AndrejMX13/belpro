# 005_report_prefs.py

> 20 nodes

## Key Concepts

- **setup.sh** (23 connections) — `scripts/setup.sh`
- **api** (13 connections) — `docker-compose.yml`
- **postgres** (11 connections) — `docker-compose.yml`
- **evolution-api** (8 connections) — `docker-compose.yml`
- **whisper** (5 connections) — `docker-compose.yml`
- **warn()** (2 connections) — `scripts/setup.sh`
- **prompt_password()** (2 connections) — `scripts/setup.sh`
- **ops** (2 connections) — `docker-compose.yml`
- **info()** (1 connections) — `scripts/setup.sh`
- **ok()** (1 connections) — `scripts/setup.sh`
- **heading()** (1 connections) — `scripts/setup.sh`
- **die()** (1 connections) — `scripts/setup.sh`
- **gen_hex32()** (1 connections) — `scripts/setup.sh`
- **gen_b64_key()** (1 connections) — `scripts/setup.sh`
- **gen_hex24()** (1 connections) — `scripts/setup.sh`
- **set_env()** (1 connections) — `scripts/setup.sh`
- **get_env()** (1 connections) — `scripts/setup.sh`
- **.env.example** (1 connections)
- **redis** (1 connections) — `docker-compose.yml`
- **frontend** (1 connections) — `docker-compose.yml`

## Relationships

- [[loadAppLog()]] (10 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (4 shared connections)
- [[008_add_manager_notified_at.py]] (4 shared connections)
- [[Code Reviewer Skill]] (3 shared connections)
- [[merge_ast_semantic.py]] (2 shared connections)
- [[API.logo.delete()]] (2 shared connections)
- [[report_pdf.py]] (2 shared connections)
- [[POST /log-entries/{id}/photos]] (1 shared connections)

## Source Files

- `docker-compose.yml`
- `scripts/setup.sh`

## Audit Trail

- EXTRACTED: 78 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*