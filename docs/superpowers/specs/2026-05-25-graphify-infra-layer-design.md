# Graphify Infrastructure Layer Design

**Date:** 2026-05-25
**Status:** Approved

---

## Goal

Inject BelPro's service-layer architecture into `graphify-out/graph.json` so that the eight Docker Compose services, their inter-service HTTP calls, startup dependencies, and nginx proxy routing are visible in the knowledge graph alongside the existing code-layer nodes.

---

## Background

The current graph (2338 nodes, 3452 edges, 283 communities) captures code-level relationships well but has no nodes for the runtime services defined in `docker-compose.yml`. The "Docker Compose" community in the graph is built entirely from prose mentions in `CLAUDE.md`, `SPEC.md`, and `README.md` — not from the compose file itself. Redis has no graph presence at all. The nginx proxy chain and inter-service HTTP calls (`api → whisper`, `api → ops`, `api → evolution-api`) are invisible.

---

## Approach

Parse `docker-compose.yml` and `nginx/nginx.conf` **programmatically** (PyYAML + regex), not via LLM extraction. Config files are structured data — deterministic parsing gives EXTRACTED edges at confidence 1.0 with no hallucination risk.

The script patches `graph.json` in place. It does **not** regenerate the wiki or GRAPH_REPORT.md — those remain manual steps run after patching.

---

## Script

**Location:** `scripts/graphify_infra.py`

**Inputs:**
- `docker-compose.yml` (PyYAML)
- `nginx/nginx.conf` (regex — `proxy_pass` directives)
- `graphify-out/graph.json` (read + patch in place)

**Outputs:**
- `graphify-out/graph.json` (patched, idempotent)

### Node schema

One node per Docker Compose service:

```json
{
  "id": "service_api",
  "label": "api",
  "file_type": "service",
  "image": "custom build (./api)",
  "ports": ["8100:8000"],
  "internal_url": "http://api:8000"
}
```

`internal_url` is populated only when an env var in another service explicitly references it (e.g. `WHISPER_SERVICE_URL: http://whisper:8001`). For services with no such env var reference (e.g. `service_postgres`), the field is omitted rather than guessed.

```
```

Services and their IDs:

| Compose service | Node ID |
|---|---|
| `postgres` | `service_postgres` |
| `redis` | `service_redis` |
| `n8n` | `service_n8n` |
| `whisper` | `service_whisper` |
| `api` | `service_api` |
| `ops` | `service_ops` |
| `frontend` (nginx) | `service_frontend` |
| `evolution-api` | `service_evolution_api` |

### Edge schema

All edges: `type: EXTRACTED`, `confidence_score: 1.0`.

**From `depends_on:` blocks:**

| Source | Relation | Target |
|---|---|---|
| `service_n8n` | `depends_on` | `service_postgres` |
| `service_api` | `depends_on` | `service_postgres` |
| `service_api` | `depends_on` | `service_whisper` |
| `service_ops` | `depends_on` | `service_api` |
| `service_ops` | `depends_on` | `service_postgres` |
| `service_frontend` | `depends_on` | `service_api` |
| `service_evolution_api` | `depends_on` | `service_postgres` |
| `service_evolution_api` | `depends_on` | `service_redis` |

**From env var URLs (inter-service HTTP calls):**

| Source | Relation | Target | Env var |
|---|---|---|---|
| `service_api` | `calls` | `service_whisper` | `WHISPER_SERVICE_URL` |
| `service_api` | `calls` | `service_evolution_api` | `EVOLUTION_API_URL` |
| `service_api` | `calls` | `service_ops` | `OPS_URL` |

**From nginx `proxy_pass`:**

| Source | Relation | Target |
|---|---|---|
| `service_frontend` | `proxies_to` | `service_api` |

### Idempotency

Before inserting any node or edge, the script checks existing IDs (for nodes) and existing `source + target + relation` triples (for edges). Duplicates are skipped silently. Running the script twice produces identical output.

---

## Memo — when to run

Add to `CLAUDE.md` graphify workflow section (between "Locate" and "Maintain" steps):

> **Infrastructure patch:** After any change to `docker-compose.yml` or `nginx/nginx.conf`, run `python scripts/graphify_infra.py` to patch `graph.json`. Run this before `graphify update .` or any wiki/report regeneration.

Add to project public memory (`docs/.claude/memory/`) as a reference memory entry indexed in `MEMORY.md`.

---

## Out of scope

### ISS-A: Frontend → API call map

The JS `fetch()` calls in `frontend/` are not linked to the FastAPI endpoints they hit. Closing this gap requires either JS AST analysis or a targeted semantic extraction pass. Deferred pre-release.

### ISS-B: Evolution → n8n webhook registration

How Evolution API is configured to POST webhook events to n8n is a runtime concern — set via Evolution API at deploy time, not captured in any committed source file. No script can extract it deterministically. Deferred pre-release.

---

## Sequence

1. Write `scripts/graphify_infra.py`
2. Run it: `python scripts/graphify_infra.py` — verify 8 new nodes + expected edges in `graph.json`
3. Update `CLAUDE.md` graphify workflow section
4. Add project memory entry
5. Commit all three artifacts together

---

## Success criteria

- `graph.json` contains 8 `service_*` nodes with correct `file_type: "service"`
- All `depends_on`, `calls`, and `proxies_to` edges present with `confidence_score: 1.0`
- Script is idempotent: running it twice produces no duplicates
- `CLAUDE.md` references the script in the graphify workflow
- Project memory entry indexed in `MEMORY.md`
