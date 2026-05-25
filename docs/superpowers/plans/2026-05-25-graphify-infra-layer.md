# Graphify Infrastructure Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Inject Docker Compose service-layer nodes and edges into `graphify-out/graph.json` via a deterministic parse script, and document when to run it.

**Architecture:** A standalone Python script (`scripts/graphify_infra.py`) parses `docker-compose.yml` with PyYAML and `nginx/nginx.conf` with regex, then patches `graph.json` in place — adding 8 service nodes and all `depends_on`, `calls`, and `proxies_to` edges. The script is idempotent. It does not regenerate the wiki or GRAPH_REPORT.md. A note in `CLAUDE.md` and a project memory entry tell future Claude sessions when to run it.

**Tech Stack:** Python 3.11+, PyYAML, stdlib `json` + `re` + `pathlib`

---

## File Structure

| File | Action | Purpose |
|---|---|---|
| `scripts/graphify_infra.py` | Create | Parses compose + nginx, patches graph.json |
| `tests/test_graphify_infra.py` | Create | Unit tests — idempotency, node/edge correctness |
| `CLAUDE.md` | Modify | Add infra-patch step to graphify workflow |
| `.claude/memory/reference_graphify_infra_script.md` | Create | Memory entry — script exists, when to run |
| `.claude/memory/MEMORY.md` | Modify | Add index entry for new memory file |

---

### Task 1: Write `scripts/graphify_infra.py` with tests

**Context:** The graph JSON format uses `"nodes"` and `"links"` keys (node_link format). Each node needs at minimum: `id`, `label`, `file_type`. Each edge needs: `source`, `target`, `relation`, `confidence`, `confidence_score`, `weight`. See existing node example: `{"id": "claude_settings_json", "label": "settings.json", "file_type": "code", "source_file": ".claude/settings.json", "source_location": "L1", "norm_label": "settings.json"}`. See existing edge example: `{"source": "a", "target": "b", "relation": "contains", "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 1.0}`.

The nginx.conf uses `set $api_upstream api:8000;` (variable upstream) rather than a bare `proxy_pass http://api:8000` — the regex must match the `set $var hostname:port` pattern.

`docker-compose.yml`'s `depends_on` can be either a list (`["postgres"]`) or a dict (`{postgres: {condition: service_healthy}}`). Handle both.

`docker-compose.yml` env vars use the `KEY: value` dict format (not `KEY=VALUE` list).

**Files:**
- Create: `scripts/graphify_infra.py`
- Create: `tests/test_graphify_infra.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_graphify_infra.py`:

```python
"""Tests for scripts/graphify_infra.py — service-layer graph injection."""
import json
import sys
import pathlib
import textwrap
import pytest

# Make scripts/ importable
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import graphify_infra as gi


MINIMAL_GRAPH = json.dumps({"nodes": [], "links": []})

MINIMAL_COMPOSE = textwrap.dedent("""\
    services:
      api:
        build: ./api
        ports:
          - "8100:8000"
        environment:
          WHISPER_SERVICE_URL: http://whisper:8001
          OPS_URL: http://ops:9000
        depends_on:
          postgres:
            condition: service_healthy
      postgres:
        image: postgres:18.3
      whisper:
        build: ./whisper
      ops:
        build: ./ops
        depends_on:
          - api
          - postgres
""")

MINIMAL_NGINX = textwrap.dedent("""\
    server {
        location /api/ {
            set $api_upstream api:8000;
            proxy_pass http://$api_upstream;
        }
    }
""")


@pytest.fixture
def tmp_graph(tmp_path):
    g = tmp_path / "graph.json"
    g.write_text(MINIMAL_GRAPH, encoding="utf-8")
    c = tmp_path / "docker-compose.yml"
    c.write_text(MINIMAL_COMPOSE, encoding="utf-8")
    n = tmp_path / "nginx.conf"
    n.write_text(MINIMAL_NGINX, encoding="utf-8")
    return g, c, n


def load(graph_path):
    return json.loads(graph_path.read_text(encoding="utf-8"))


def test_service_nodes_created(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    ids = {node["id"] for node in data["nodes"]}
    assert "service_api" in ids
    assert "service_postgres" in ids
    assert "service_whisper" in ids
    assert "service_ops" in ids


def test_node_has_required_fields(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    api_node = next(node for node in data["nodes"] if node["id"] == "service_api")
    assert api_node["label"] == "api"
    assert api_node["file_type"] == "service"
    assert api_node["norm_label"] == "api"
    assert api_node["source_file"] == "docker-compose.yml"


def test_depends_on_dict_format(tmp_graph):
    """depends_on: {postgres: {condition: ...}} format is handled."""
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    edges = {(e["source"], e["target"], e["relation"]) for e in data["links"]}
    assert ("service_api", "service_postgres", "depends_on") in edges


def test_depends_on_list_format(tmp_graph):
    """depends_on: [api, postgres] list format is handled."""
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    edges = {(e["source"], e["target"], e["relation"]) for e in data["links"]}
    assert ("service_ops", "service_api", "depends_on") in edges
    assert ("service_ops", "service_postgres", "depends_on") in edges


def test_env_url_calls_edges(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    edges = {(e["source"], e["target"], e["relation"]) for e in data["links"]}
    assert ("service_api", "service_whisper", "calls") in edges
    assert ("service_api", "service_ops", "calls") in edges


def test_nginx_proxies_to_edge(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    edges = {(e["source"], e["target"], e["relation"]) for e in data["links"]}
    assert ("service_frontend", "service_api", "proxies_to") in edges


def test_edges_are_extracted_confidence_1(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    for edge in data["links"]:
        assert edge["confidence"] == "EXTRACTED"
        assert edge["confidence_score"] == 1.0


def test_idempotent_nodes(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    count_after_first = len(load(g)["nodes"])
    gi.inject(g, c, n)
    count_after_second = len(load(g)["nodes"])
    assert count_after_first == count_after_second


def test_idempotent_edges(tmp_graph):
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    count_after_first = len(load(g)["links"])
    gi.inject(g, c, n)
    count_after_second = len(load(g)["links"])
    assert count_after_first == count_after_second


def test_existing_nodes_preserved(tmp_graph):
    """Pre-existing nodes in graph.json are not removed."""
    g, c, n = tmp_graph
    existing = {"nodes": [{"id": "existing_node", "label": "x", "file_type": "code"}], "links": []}
    g.write_text(json.dumps(existing), encoding="utf-8")
    gi.inject(g, c, n)
    data = load(g)
    ids = {node["id"] for node in data["nodes"]}
    assert "existing_node" in ids


def test_no_self_calls(tmp_graph):
    """No service generates a calls edge to itself."""
    g, c, n = tmp_graph
    gi.inject(g, c, n)
    data = load(g)
    for edge in data["links"]:
        assert edge["source"] != edge["target"]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /d/Andrej/vsCode-workspace/BelPro
python -m pytest tests/test_graphify_infra.py -v 2>&1 | head -30
```

Expected: `ModuleNotFoundError: No module named 'graphify_infra'`

- [ ] **Step 3: Install PyYAML if not present**

```bash
python -m pip show pyyaml || python -m pip install pyyaml
```

- [ ] **Step 4: Write `scripts/graphify_infra.py`**

```python
#!/usr/bin/env python
"""Inject Docker Compose service-layer nodes and edges into graphify-out/graph.json.

Run after any change to docker-compose.yml or nginx/nginx.conf, before
graphify update . or wiki/report regeneration. Idempotent — safe to run twice.

Usage:
  python scripts/graphify_infra.py
"""

import json
import pathlib
import re

import yaml

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
GRAPH_FILE = PROJECT_DIR / "graphify-out" / "graph.json"
COMPOSE_FILE = PROJECT_DIR / "docker-compose.yml"
NGINX_FILE = PROJECT_DIR / "nginx" / "nginx.conf"


def _node_id(service_name: str) -> str:
    return f"service_{service_name.replace('-', '_')}"


def _build_service_nodes(services: dict) -> list[dict]:
    nodes = []
    for name, svc in services.items():
        image = svc.get("image") or f"custom build (./{name})"
        node: dict = {
            "id": _node_id(name),
            "label": name,
            "norm_label": name,
            "file_type": "service",
            "source_file": "docker-compose.yml",
            "source_location": f"services.{name}",
            "image": image,
        }
        ports = svc.get("ports")
        if ports:
            node["ports"] = [str(p) for p in ports]
        nodes.append(node)
    return nodes


def _depends_on_edges(services: dict) -> list[dict]:
    edges = []
    for svc_name, svc in services.items():
        depends = svc.get("depends_on") or []
        if isinstance(depends, dict):
            targets = list(depends.keys())
        else:
            targets = list(depends)
        for dep in targets:
            edges.append({
                "source": _node_id(svc_name),
                "target": _node_id(dep),
                "relation": "depends_on",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "weight": 1.0,
                "source_file": "docker-compose.yml",
                "source_location": f"services.{svc_name}.depends_on",
            })
    return edges


def _env_url_edges(services: dict) -> list[dict]:
    """Extract inter-service HTTP call edges from env var URL values."""
    service_names = set(services.keys())
    url_pattern = re.compile(r"http://([a-z0-9_-]+):\d+")
    edges = []
    seen: set[tuple] = set()

    for svc_name, svc in services.items():
        env = svc.get("environment") or {}
        if isinstance(env, list):
            env = dict(item.split("=", 1) for item in env if "=" in item)

        for key, value in env.items():
            if not isinstance(value, str):
                continue
            m = url_pattern.search(value)
            if not m:
                continue
            hostname = m.group(1)
            if hostname not in service_names or hostname == svc_name:
                continue
            triple = (_node_id(svc_name), _node_id(hostname), "calls")
            if triple in seen:
                continue
            seen.add(triple)
            edges.append({
                "source": _node_id(svc_name),
                "target": _node_id(hostname),
                "relation": "calls",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "weight": 1.0,
                "source_file": "docker-compose.yml",
                "source_location": f"services.{svc_name}.environment.{key}",
            })
    return edges


def _nginx_edges(nginx_conf: str, services: dict) -> list[dict]:
    """Extract proxies_to edges from nginx set $var hostname:port directives."""
    service_names = set(services.keys())
    # matches: set $any_var_name  hostname:port
    pattern = re.compile(r"set\s+\$\w+\s+([a-z0-9_-]+):\d+")
    edges = []
    seen_targets: set[str] = set()

    for m in pattern.finditer(nginx_conf):
        hostname = m.group(1)
        if hostname not in service_names:
            continue
        target_id = _node_id(hostname)
        if target_id in seen_targets:
            continue
        seen_targets.add(target_id)
        edges.append({
            "source": _node_id("frontend"),
            "target": target_id,
            "relation": "proxies_to",
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
            "weight": 1.0,
            "source_file": "nginx/nginx.conf",
            "source_location": "proxy_pass",
        })
    return edges


def inject(
    graph_file: pathlib.Path,
    compose_file: pathlib.Path,
    nginx_file: pathlib.Path,
) -> dict:
    """Patch graph_file in place with service nodes and edges. Returns counts."""
    data = json.loads(graph_file.read_bytes().decode("utf-8-sig"))
    compose = yaml.safe_load(compose_file.read_text(encoding="utf-8"))
    services: dict = compose.get("services", {})
    nginx_conf = nginx_file.read_text(encoding="utf-8")

    existing_ids = {n["id"] for n in data["nodes"]}
    new_nodes = [
        node for node in _build_service_nodes(services)
        if node["id"] not in existing_ids
    ]

    existing_edge_keys = {
        (e["source"], e["target"], e["relation"])
        for e in data["links"]
    }
    candidate_edges = (
        _depends_on_edges(services)
        + _env_url_edges(services)
        + _nginx_edges(nginx_conf, services)
    )
    new_edges = []
    for edge in candidate_edges:
        key = (edge["source"], edge["target"], edge["relation"])
        if key not in existing_edge_keys:
            new_edges.append(edge)
            existing_edge_keys.add(key)

    data["nodes"].extend(new_nodes)
    data["links"].extend(new_edges)
    graph_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {"nodes_added": len(new_nodes), "edges_added": len(new_edges)}


if __name__ == "__main__":
    result = inject(GRAPH_FILE, COMPOSE_FILE, NGINX_FILE)
    print(
        f"graphify_infra: injected {result['nodes_added']} nodes, "
        f"{result['edges_added']} edges → {GRAPH_FILE}"
    )
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest tests/test_graphify_infra.py -v
```

Expected: all 11 tests PASS

- [ ] **Step 6: Commit script and tests**

```bash
git add scripts/graphify_infra.py tests/test_graphify_infra.py
git status
git commit -m "feat: add graphify_infra.py — inject Docker service topology into graph.json"
```

---

### Task 2: Run the script on the real graph and verify

**Context:** The real `graphify-out/graph.json` has 2338 nodes and 3452 edges. After injection it should have 2346 nodes (8 added) and around 3467+ edges. The script must be run from the project root. `graph.json` is encoded UTF-8 with BOM — the script handles this via `read_bytes().decode("utf-8-sig")`.

**Files:**
- Modify: `graphify-out/graph.json` (patched in place)

- [ ] **Step 1: Run the script**

```bash
cd /d/Andrej/vsCode-workspace/BelPro
python scripts/graphify_infra.py
```

Expected output (exact counts may vary by a node or two if any service node already exists):
```
graphify_infra: injected 8 nodes, 15 edges → graphify-out/graph.json
```

- [ ] **Step 2: Verify node count increased by 8**

```bash
python3 -c "
import json
data = json.loads(open('graphify-out/graph.json', encoding='utf-8-sig').read())
nodes = [n for n in data['nodes'] if n.get('file_type') == 'service']
print(f'Service nodes ({len(nodes)}):')
for n in nodes:
    print(f'  {n[\"id\"]} — {n[\"label\"]} ({n.get(\"image\",\"\")[:40]})')
"
```

Expected: 8 service nodes listed.

- [ ] **Step 3: Verify key edges exist**

```bash
python3 -c "
import json
data = json.loads(open('graphify-out/graph.json', encoding='utf-8-sig').read())
service_edges = [e for e in data['links'] if e['source'].startswith('service_') or e['target'].startswith('service_')]
print(f'Service edges ({len(service_edges)}):')
for e in sorted(service_edges, key=lambda x: x['relation']):
    print(f'  {e[\"source\"]} --{e[\"relation\"]}--> {e[\"target\"]}')
"
```

Expected edges visible:
- `service_api --calls--> service_whisper`
- `service_api --calls--> service_evolution_api`
- `service_api --calls--> service_ops`
- `service_api --depends_on--> service_postgres`
- `service_api --depends_on--> service_whisper`
- `service_ops --depends_on--> service_api`
- `service_ops --depends_on--> service_postgres`
- `service_frontend --depends_on--> service_api`
- `service_frontend --proxies_to--> service_api`
- `service_evolution_api --depends_on--> service_postgres`
- `service_evolution_api --depends_on--> service_redis`
- `service_n8n --depends_on--> service_postgres`

- [ ] **Step 4: Verify idempotency on real graph**

```bash
python scripts/graphify_infra.py
```

Expected output:
```
graphify_infra: injected 0 nodes, 0 edges → graphify-out/graph.json
```

- [ ] **Step 5: Commit the patched graph**

```bash
git status
git add graphify-out/graph.json
git commit -m "feat: inject service topology into graphify graph (8 nodes, ~15 edges)"
```

---

### Task 3: Update CLAUDE.md and add memory entry

**Context:** The graphify workflow in `CLAUDE.md` currently has 4 numbered steps (Orient, Locate, Read, Maintain) starting at line ~266. Add a new step **between Read (3) and Maintain (4)** — call it step 3.5 or renumber. The public project memory index is at `.claude/memory/MEMORY.md` — add one line to it. The memory file itself goes in `.claude/memory/reference_graphify_infra_script.md`.

**Files:**
- Modify: `CLAUDE.md` (graphify workflow section, ~line 266)
- Create: `.claude/memory/reference_graphify_infra_script.md`
- Modify: `.claude/memory/MEMORY.md`

- [ ] **Step 1: Update CLAUDE.md graphify workflow**

Find the `### Workflow` section in `CLAUDE.md`. It currently reads:

```markdown
1. **Orient** — Read `graphify-out/wiki/index.md` ...
2. **Locate** — Use Serena `find_symbol` ...
3. **Read** — Read the actual source files ...
4. **Maintain** — After modifying code files, run `graphify update .` ...
```

Replace it with:

```markdown
1. **Orient** — Read `graphify-out/wiki/index.md` to find the community most relevant to your task. Each community article lists its member nodes and links to connected communities.
2. **Locate** — Use Serena `find_symbol` to find specific functions, classes, or methods within the identified files, or `find_referencing_symbols` to trace callers.
3. **Read** — Read the actual source files to understand logic. The graph tells you which files matter; it does not replace reading them.
4. **Infrastructure patch** — After any change to `docker-compose.yml` or `nginx/nginx.conf`, run `python scripts/graphify_infra.py` to patch `graph.json`. Do this before `graphify update .` or any wiki/report regeneration. Script: `scripts/graphify_infra.py`.
5. **Maintain** — After modifying code files, run `graphify update .` to keep the graph current (AST-only, no API cost). Cross-layer semantic edges are preserved in the committed cache (`graphify-out/cache/`) and survive full rebuilds.
```

- [ ] **Step 2: Create `.claude/memory/reference_graphify_infra_script.md`**

```markdown
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

**How to apply:** When docker-compose.yml or nginx/nginx.conf changes, remind user to run `python scripts/graphify_infra.py` and commit the updated graph.json alongside the config change.
```

- [ ] **Step 3: Add index entry to `.claude/memory/MEMORY.md`**

Add this line under the `## Tooling — graphify` section:

```markdown
- [graphify infra script](reference_graphify_infra_script.md) — scripts/graphify_infra.py patches graph.json with Docker service topology; run after compose/nginx changes
```

- [ ] **Step 4: Commit**

```bash
git status
git add CLAUDE.md .claude/memory/reference_graphify_infra_script.md .claude/memory/MEMORY.md
git commit -m "docs: document graphify_infra.py in CLAUDE.md workflow and project memory"
```
