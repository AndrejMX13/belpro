# n8n Set Node Pattern

> 13 nodes

## Key Concepts

- **n8n_workflows.py** (11 connections) — `scripts/n8n_workflows.py`
- **n8n** (6 connections) — `docker-compose.yml`
- **api_request()** (4 connections) — `scripts/n8n_workflows.py`
- **cmd_import()** (4 connections) — `scripts/n8n_workflows.py`
- **cmd_export()** (4 connections) — `scripts/n8n_workflows.py`
- **main()** (4 connections) — `scripts/n8n_workflows.py`
- **load_env()** (3 connections) — `scripts/n8n_workflows.py`
- **Parse KEY=VALUE lines from a .env file; ignore comments and blanks.** (1 connections) — `scripts/n8n_workflows.py`
- **Make an authenticated request to the n8n API.      Returns (status_code, respo** (1 connections) — `scripts/n8n_workflows.py`
- **Load each repo workflow file into n8n (upsert + activate).** (1 connections) — `scripts/n8n_workflows.py`
- **Overwrite each repo workflow file with its current definition from n8n.** (1 connections) — `scripts/n8n_workflows.py`
- **n8n REST API** (1 connections)
- **n8n/workflows/** (1 connections)

## Relationships

- [[004_log_entry_photos.py]] (2 shared connections)
- [[010_monthly_reports_unique_idx.py]] (1 shared connections)
- [[PDF Generated (Per Volunteer + Consolidated)]] (1 shared connections)
- [[loadAnalytics()]] (1 shared connections)
- [[HTTP: GET Volunteer (Mgr)]] (1 shared connections)
- [[API.logo.upload()]] (1 shared connections)
- [[PATCH /log-entries/{id}]] (1 shared connections)

## Source Files

- `docker-compose.yml`
- `scripts/n8n_workflows.py`

## Audit Trail

- EXTRACTED: 42 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*