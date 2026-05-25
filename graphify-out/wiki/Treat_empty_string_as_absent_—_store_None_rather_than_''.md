# Treat empty string as absent — store None rather than ''.

> 14 nodes

## Key Concepts

- **graphify_infra.py** (7 connections) — `scripts/graphify_infra.py`
- **_extract_compose_data()** (6 connections) — `scripts/graphify_infra.py`
- **_service_node_id()** (5 connections) — `scripts/graphify_infra.py`
- **_extract_nginx_edges()** (5 connections) — `scripts/graphify_infra.py`
- **_make_node()** (4 connections) — `scripts/graphify_infra.py`
- **_make_edge()** (4 connections) — `scripts/graphify_infra.py`
- **inject()** (4 connections) — `scripts/graphify_infra.py`
- **graphify_infra.py — Inject Docker service topology into graphify-out/graph.json.** (1 connections) — `scripts/graphify_infra.py`
- **Convert a Docker service name to a graph node ID.** (1 connections) — `scripts/graphify_infra.py`
- **Build a graph node dict for a Docker service.** (1 connections) — `scripts/graphify_infra.py`
- **Build a graph edge dict.** (1 connections) — `scripts/graphify_infra.py`
- **Extract service nodes and edges from a parsed docker-compose structure.      Ret** (1 connections) — `scripts/graphify_infra.py`
- **Extract proxies_to edges from nginx config.      Matches the variable-upstream p** (1 connections) — `scripts/graphify_infra.py`
- **Inject Docker service topology nodes and edges into graph.json.      Reads the t** (1 connections) — `scripts/graphify_infra.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/graphify_infra.py`

## Audit Trail

- EXTRACTED: 42 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*