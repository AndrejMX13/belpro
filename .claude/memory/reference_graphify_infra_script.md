---
name: reference-graphify-infra-script
description: graphify_infra.py patches graph.json with Docker service topology — when and why to run it
metadata:
  type: reference
---

`scripts/graphify_infra.py` injects Docker Compose service nodes and inter-service edges into `graphify-out/graph.json`.

Run it after any change to `docker-compose.yml` or `nginx/nginx.conf`, before `graphify update .` or wiki/report regeneration.

**What it adds:** 8 `file_type: "service"` nodes (one per Docker service), plus `depends_on`, `calls`, and `proxies_to` edges extracted from compose `depends_on` blocks, env var URLs, and nginx `proxy_pass` directives. All edges are `EXTRACTED` at `confidence_score: 1.0`.

**Idempotent:** safe to run multiple times — skips existing nodes and edges.

**How to apply:** When docker-compose.yml or nginx/nginx.conf changes, run `python scripts/graphify_infra.py` and commit the updated graph.json alongside the config change.
