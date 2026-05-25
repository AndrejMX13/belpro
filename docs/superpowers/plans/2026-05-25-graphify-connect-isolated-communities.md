# Graphify — Connect Isolated Communities

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run targeted semantic extraction passes to connect 159 isolated graphify communities to the main graph, starting with the highest-value application code gaps.

**Architecture:** Each task dispatches one semantic subagent reading a mixed chunk of isolated files + their natural connection targets. Results are merged into `graphify-out/graph.json`, saved to the semantic cache, and committed. Final task regenerates `graph.html` and `GRAPH_REPORT.md`.

**Tech Stack:** Python, graphify 0.8.14+, networkx, `graphify-out/graph.json`, `graphify-out/cache/semantic/`

---

## Context for the executing agent

This is a graphify knowledge graph enrichment task — not a code change. No application code is modified. Each "implementation" step dispatches a subagent that reads source files and extracts semantic relationships, then merges the result into the existing graph.

**Key scripts used throughout this plan:**

### Merge script (reuse across all tasks, substitute CHUNK_FILE and OUTPUT_LABEL)

```python
# merge_chunk.py — run from project root
import json, networkx as nx
from networkx.readwrite import json_graph
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.cache import save_semantic_cache
from pathlib import Path

CHUNK_FILE = 'graphify-out/.graphify_chunk_LABEL.json'  # substitute per task

chunk = json.loads(Path(CHUNK_FILE).read_bytes().decode('utf-8-sig'))
base  = json.loads(Path('graphify-out/graph.json').read_bytes().decode('utf-8-sig'))
G     = json_graph.node_link_graph(base, edges='links')

added_nodes = 0
for n in chunk.get('nodes', []):
    nid = n.get('id') or n.get('label', '')
    if nid and nid not in G:
        G.add_node(nid, **{k: v for k, v in n.items() if k != 'id'})
        added_nodes += 1
    elif nid:
        G.nodes[nid].update({k: v for k, v in n.items() if k != 'id'})

added_edges = 0
for e in chunk.get('edges', []):
    src, tgt = e.get('source', ''), e.get('target', '')
    if src and tgt and src in G and tgt in G:
        if not G.has_edge(src, tgt):
            G.add_edge(src, tgt, **{k: v for k, v in e.items() if k not in ('source','target')})
            added_edges += 1

saved = save_semantic_cache(
    nodes=chunk.get('nodes', []),
    edges=chunk.get('edges', []),
    hyperedges=chunk.get('hyperedges', []),
    root=Path('.')
)

data = json_graph.node_link_data(G, edges='links')
Path('graphify-out/graph.json').write_text(
    json.dumps(data, ensure_ascii=False), encoding='utf-8'
)
print(f'Merged: +{added_nodes} nodes, +{added_edges} edges | {saved} files cached')
```

### Connectivity check (reuse across all tasks, substitute COMMUNITY_IDS)

```python
# check_connectivity.py — run from project root
import json, networkx as nx
from networkx.readwrite import json_graph
from collections import defaultdict
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_bytes().decode('utf-8-sig'))
G = json_graph.node_link_graph(data, edges='links')

communities = defaultdict(list)
for nid, ndata in G.nodes(data=True):
    cid = ndata.get('community')
    if cid is not None:
        communities[cid].append(nid)

ext = defaultdict(int)
for u, v in G.edges():
    cu, cv = G.nodes[u].get('community'), G.nodes[v].get('community')
    if cu is not None and cv is not None and cu != cv:
        ext[cu] += 1
        ext[cv] += 1

CHECK_IDS = [0, 3, 20, 48]  # substitute per task
for cid in CHECK_IDS:
    print(f'C{cid}: {ext[cid]} external edges ({"CONNECTED" if ext[cid] > 0 else "STILL ISOLATED"})')
```

### Graph.html regeneration (final task only)

```python
# regen_html.py
import json, networkx as nx
from networkx.readwrite import json_graph
from graphify.export import to_html
from pathlib import Path
from collections import Counter

data = json.loads(Path('graphify-out/graph.json').read_bytes().decode('utf-8-sig'))
G = json_graph.node_link_graph(data, edges='links')

communities = {}
for nid, ndata in G.nodes(data=True):
    cid = ndata.get('community')
    if cid is not None:
        communities.setdefault(cid, []).append(nid)

degree = dict(G.degree())
community_labels = {}
for cid, members in communities.items():
    top = max(members, key=lambda n: degree.get(n, 0))
    community_labels[cid] = G.nodes[top].get('label', top)

labels_path = Path('graphify-out/.graphify_labels.json')
if labels_path.exists():
    raw = json.loads(labels_path.read_text(encoding='utf-8'))
    for k, v in raw.items():
        if not v.startswith('Community '):
            community_labels[int(k)] = v

meta = nx.Graph()
for cid, members in communities.items():
    meta.add_node(str(cid), label=community_labels[cid], community=cid)

edge_counts = Counter()
for u, v in G.edges():
    cu = G.nodes[u].get('community')
    cv = G.nodes[v].get('community')
    if cu is not None and cv is not None and cu != cv:
        edge_counts[(min(cu, cv), max(cu, cv))] += 1

for (cu, cv), w in edge_counts.items():
    meta.add_edge(str(cu), str(cv), weight=w, relation=f'{w} links', confidence='EXTRACTED')

mc = {cid: len(members) for cid, members in communities.items()}
to_html(meta, {cid: [str(cid)] for cid in communities}, 'graphify-out/graph.html',
        community_labels=community_labels, member_counts=mc)
print(f'graph.html: {meta.number_of_nodes()} nodes, {meta.number_of_edges()} edges')
```

---

## Task 1: Connect Frontend JS ↔ Backend Routers (C0, C20, C48)

**What:** 132 nodes — the entire frontend JS layer — are completely isolated. The JS files call backend API endpoints; subagent reads both sides to extract those cross-layer edges.

**Files read by subagent (15 files):**
```
frontend/js/admin.js
frontend/js/analytics.js
frontend/js/api.js
frontend/js/documents.js
frontend/js/errors.js
frontend/js/reports.js
frontend/js/volunteers.js
api/routers/admin.py
api/routers/analytics.py
api/routers/log_entries.py
api/routers/volunteers.py
api/routers/managers.py
api/routers/reports.py
api/routers/documents.py
api/routers/errors.py
```

- [ ] **Step 1: Dispatch extraction subagent**

  Dispatch a subagent with the prompt below. Save its JSON output to `graphify-out/.graphify_chunk_p1.json`.

  ```
  You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
  Output ONLY valid JSON — no explanation, no markdown fences, no preamble.

  Files (chunk 1 of 5 — Frontend ↔ Backend):
  frontend/js/admin.js
  frontend/js/analytics.js
  frontend/js/api.js
  frontend/js/documents.js
  frontend/js/errors.js
  frontend/js/reports.js
  frontend/js/volunteers.js
  api/routers/admin.py
  api/routers/analytics.py
  api/routers/log_entries.py
  api/routers/volunteers.py
  api/routers/managers.py
  api/routers/reports.py
  api/routers/documents.py
  api/routers/errors.py

  Focus: find every place a frontend JS function calls a backend API endpoint.
  For each call: source = the JS function making the call, target = the Python route handler receiving it, relation = "calls", confidence_score = 1.0, confidence = "EXTRACTED".
  Also extract: which JS render function depends on which API response shape.
  Do NOT re-extract imports or internal JS function calls — only frontend↔backend edges.

  Rules:
  - EXTRACTED: explicit call/fetch in source (confidence_score=1.0)
  - INFERRED: implied dependency, no direct call (confidence_score 0.75–0.95)
  - confidence_score is REQUIRED on every edge

  Output schema:
  {"nodes": [...], "edges": [...], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}

  Each node: {"id": "...", "label": "...", "source_file": "...", "node_type": "function|class|concept"}
  Each edge: {"source": "...", "target": "...", "relation": "...", "confidence": "EXTRACTED|INFERRED", "confidence_score": 1.0, "source_file": "..."}
  ```

- [ ] **Step 2: Verify subagent output**

  ```python
  import json
  from pathlib import Path
  d = json.loads(Path('graphify-out/.graphify_chunk_p1.json').read_bytes().decode('utf-8-sig'))
  print(f'nodes={len(d["nodes"])}, edges={len(d["edges"])}')
  assert len(d['edges']) > 10, 'Expected >10 cross-layer edges'
  ```

- [ ] **Step 3: Merge into graph.json and save to cache**

  Run the merge script (from Context section above) with `CHUNK_FILE = 'graphify-out/.graphify_chunk_p1.json'`.

- [ ] **Step 4: Verify connectivity**

  Run the connectivity check with `CHECK_IDS = [0, 20, 48]`. All three should show `CONNECTED`.

- [ ] **Step 5: Commit**

  ```
  git status
  git add graphify-out/.graphify_chunk_p1.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: connect frontend JS to backend routers in graphify — graphify update"
  ```

---

## Task 2: Connect ORM Models ↔ Pydantic Schemas (C3)

**What:** 51 nodes covering all `api/models/` and `api/schemas/` and `api/services/` are isolated. These define the data layer and should connect to routers and to each other.

**Files read by subagent (17 files):**
```
api/models/app_setting.py
api/models/base.py
api/models/error_log.py
api/models/log_entry.py
api/models/log_entry_photo.py
api/models/manager.py
api/models/monthly_report.py
api/models/volunteer.py
api/schemas/admin.py
api/schemas/analytics.py
api/schemas/error_log.py
api/schemas/log_entry.py
api/schemas/manager.py
api/schemas/report.py
api/schemas/volunteer.py
api/routers/log_entries.py
api/routers/volunteers.py
```

- [ ] **Step 1: Dispatch extraction subagent**

  Dispatch a subagent with the prompt below. Save output to `graphify-out/.graphify_chunk_p2.json`.

  ```
  You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
  Output ONLY valid JSON — no explanation, no markdown fences, no preamble.

  Files (chunk 2 of 5 — Models ↔ Schemas):
  api/models/app_setting.py
  api/models/base.py
  api/models/error_log.py
  api/models/log_entry.py
  api/models/log_entry_photo.py
  api/models/manager.py
  api/models/monthly_report.py
  api/models/volunteer.py
  api/schemas/admin.py
  api/schemas/analytics.py
  api/schemas/error_log.py
  api/schemas/log_entry.py
  api/schemas/manager.py
  api/schemas/report.py
  api/schemas/volunteer.py
  api/routers/log_entries.py
  api/routers/volunteers.py

  Focus: find every ORM model field that maps to a Pydantic schema field (model→schema),
  every schema used as a route response or body (schema→router), and every service that
  reads/writes an ORM model. These are the cross-layer edges that are currently missing.

  Rules:
  - EXTRACTED: explicit type annotation, import, or SQLAlchemy column reference (confidence_score=1.0)
  - INFERRED: same field name in model and schema, no explicit reference (confidence_score=0.85)
  - confidence_score is REQUIRED on every edge

  Output schema:
  {"nodes": [...], "edges": [...], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
  ```

- [ ] **Step 2: Verify subagent output**

  ```python
  import json
  from pathlib import Path
  d = json.loads(Path('graphify-out/.graphify_chunk_p2.json').read_bytes().decode('utf-8-sig'))
  print(f'nodes={len(d["nodes"])}, edges={len(d["edges"])}')
  assert len(d['edges']) > 15, 'Expected >15 model↔schema edges'
  ```

- [ ] **Step 3: Merge into graph.json and save to cache**

  Run merge script with `CHUNK_FILE = 'graphify-out/.graphify_chunk_p2.json'`.

- [ ] **Step 4: Verify connectivity**

  Run connectivity check with `CHECK_IDS = [3]`. Should show `CONNECTED`.

- [ ] **Step 5: Commit**

  ```
  git status
  git add graphify-out/.graphify_chunk_p2.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: connect ORM models and schemas in graphify — graphify update"
  ```

---

## Task 3: Connect Services ↔ Routers + monthly_reports.json (C4)

**What:** `api/services/` are isolated from the routers that call them. Also `monthly_reports.json` n8n workflow (C4, 46 nodes) is isolated from the reports router.

**Files read by subagent (12 files):**
```
api/services/app_settings.py
api/services/consent_pdf.py
api/services/email.py
api/services/encryption.py
api/services/evolution.py
api/services/logo.py
api/services/report_pdf.py
api/services/report_storage.py
api/routers/admin.py
api/routers/reports.py
api/routers/documents.py
n8n/workflows/monthly_reports.json
```

- [ ] **Step 1: Dispatch extraction subagent**

  Dispatch a subagent with the prompt below. Save output to `graphify-out/.graphify_chunk_p3.json`.

  ```
  You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
  Output ONLY valid JSON — no explanation, no markdown fences, no preamble.

  Files (chunk 3 of 5 — Services ↔ Routers + n8n monthly reports):
  api/services/app_settings.py
  api/services/consent_pdf.py
  api/services/email.py
  api/services/encryption.py
  api/services/evolution.py
  api/services/logo.py
  api/services/report_pdf.py
  api/services/report_storage.py
  api/routers/admin.py
  api/routers/reports.py
  api/routers/documents.py
  n8n/workflows/monthly_reports.json

  Focus: find every router function that calls a service function (router→service edges),
  every service that depends on another service, and every n8n HTTP node that calls a
  FastAPI endpoint (n8n→API edges). These cross-layer edges are currently missing.

  Rules:
  - EXTRACTED: explicit import + function call (confidence_score=1.0)
  - INFERRED: implied dependency, same operation name (confidence_score=0.85)
  - confidence_score is REQUIRED on every edge

  Output schema:
  {"nodes": [...], "edges": [...], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
  ```

- [ ] **Step 2: Verify subagent output**

  ```python
  import json
  from pathlib import Path
  d = json.loads(Path('graphify-out/.graphify_chunk_p3.json').read_bytes().decode('utf-8-sig'))
  print(f'nodes={len(d["nodes"])}, edges={len(d["edges"])}')
  assert len(d['edges']) > 10, 'Expected >10 service↔router edges'
  ```

- [ ] **Step 3: Merge into graph.json and save to cache**

  Run merge script with `CHUNK_FILE = 'graphify-out/.graphify_chunk_p3.json'`.

- [ ] **Step 4: Verify connectivity**

  Run connectivity check with `CHECK_IDS = [4]`. Should show `CONNECTED`.

- [ ] **Step 5: Commit**

  ```
  git status
  git add graphify-out/.graphify_chunk_p3.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: connect services, routers, and monthly_reports.json in graphify — graphify update"
  ```

---

## Task 4: Connect Design Docs ↔ Implementation (C10, C15, C79)

**What:** ~73 nodes of spec and design documents reference implemented features but have no edges to the code. This task adds those reference edges.

**Files read by subagent (~14 files):**
```
docs/superpowers/specs/2026-05-07-manager-approval-design.md
docs/superpowers/specs/2026-05-09-test-suite-design.md
docs/superpowers/specs/2026-05-09-log-entry-location-edit-design.md
docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md
docs/superpowers/specs/2026-05-20-gdpr-consent-design.md
docs/superpowers/specs/2026-05-20-settings-table-design.md
docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md
docs/superpowers/plans/2026-05-07-manager-approval.md
docs/superpowers/plans/2026-05-09-log-entry-location-edit.md
n8n/workflows/manager_approval.json
api/routers/log_entries.py
api/routers/admin.py
api/routers/auth.py
api/services/app_settings.py
```

- [ ] **Step 1: Dispatch extraction subagent**

  Dispatch a subagent with the prompt below. Save output to `graphify-out/.graphify_chunk_p4.json`.

  ```
  You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
  Output ONLY valid JSON — no explanation, no markdown fences, no preamble.

  Files (chunk 4 of 5 — Design docs ↔ Implementation):
  docs/superpowers/specs/2026-05-07-manager-approval-design.md
  docs/superpowers/specs/2026-05-09-test-suite-design.md
  docs/superpowers/specs/2026-05-09-log-entry-location-edit-design.md
  docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md
  docs/superpowers/specs/2026-05-20-gdpr-consent-design.md
  docs/superpowers/specs/2026-05-20-settings-table-design.md
  docs/superpowers/specs/2026-05-21-auto-monthly-reports-design.md
  docs/superpowers/plans/2026-05-07-manager-approval.md
  docs/superpowers/plans/2026-05-09-log-entry-location-edit.md
  n8n/workflows/manager_approval.json
  api/routers/log_entries.py
  api/routers/admin.py
  api/routers/auth.py
  api/services/app_settings.py

  Focus: for each design doc, find the code or workflow that implements what it describes.
  Create IMPLEMENTS or SPECIFIES edges between spec/plan nodes and their implementation.
  Also find cases where a plan mentions a specific API endpoint or function by name.

  Rules:
  - EXTRACTED: spec explicitly names a function/endpoint that exists in the listed files (confidence_score=1.0)
  - INFERRED: spec describes behavior that maps to an implementation (confidence_score=0.85)
  - confidence_score is REQUIRED on every edge

  Output schema:
  {"nodes": [...], "edges": [...], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
  ```

- [ ] **Step 2: Verify subagent output**

  ```python
  import json
  from pathlib import Path
  d = json.loads(Path('graphify-out/.graphify_chunk_p4.json').read_bytes().decode('utf-8-sig'))
  print(f'nodes={len(d["nodes"])}, edges={len(d["edges"])}')
  assert len(d['edges']) > 5, 'Expected >5 spec↔implementation edges'
  ```

- [ ] **Step 3: Merge into graph.json and save to cache**

  Run merge script with `CHUNK_FILE = 'graphify-out/.graphify_chunk_p4.json'`.

- [ ] **Step 4: Verify connectivity**

  Run connectivity check with `CHECK_IDS = [10, 15, 79]`. All should show `CONNECTED`.

- [ ] **Step 5: Commit**

  ```
  git status
  git add graphify-out/.graphify_chunk_p4.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: connect design docs to implementation in graphify — graphify update"
  ```

---

## Task 5: Connect Ops Scripts (C54, C55, C69, C77, C90, C100)

**What:** `scripts/*.sh`, `scripts/n8n_workflows.py`, `scripts/gen_diagrams.py` are all isolated. These connect to the workflows, API, and architecture they support.

**Files read by subagent (10 files):**
```
scripts/gen_diagrams.py
scripts/gen_diagrams_sl.py
scripts/setup.sh
scripts/upgrade.sh
scripts/rotate_emso_key.sh
scripts/n8n_workflows.py
scripts/backup.sh
api/main.py
n8n/workflows/volunteer_entry.json
n8n/workflows/manager_approval.json
```

- [ ] **Step 1: Dispatch extraction subagent**

  Dispatch a subagent with the prompt below. Save output to `graphify-out/.graphify_chunk_p5.json`.

  ```
  You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
  Output ONLY valid JSON — no explanation, no markdown fences, no preamble.

  Files (chunk 5 of 5 — Ops scripts):
  scripts/gen_diagrams.py
  scripts/gen_diagrams_sl.py
  scripts/setup.sh
  scripts/upgrade.sh
  scripts/rotate_emso_key.sh
  scripts/n8n_workflows.py
  scripts/backup.sh
  api/main.py
  n8n/workflows/volunteer_entry.json
  n8n/workflows/manager_approval.json

  Focus: what does each script operate on? setup.sh starts which services? upgrade.sh
  touches which components? n8n_workflows.py imports/exports which workflow files?
  gen_diagrams.py generates diagrams of what architecture? rotate_emso_key.sh rotates
  which encrypted field? Find the connections between scripts and the system components
  they manage.

  Rules:
  - EXTRACTED: script explicitly names a file, service, or component (confidence_score=1.0)
  - INFERRED: script's purpose implies a dependency (confidence_score=0.75)
  - confidence_score is REQUIRED on every edge

  Output schema:
  {"nodes": [...], "edges": [...], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
  ```

- [ ] **Step 2: Verify subagent output**

  ```python
  import json
  from pathlib import Path
  d = json.loads(Path('graphify-out/.graphify_chunk_p5.json').read_bytes().decode('utf-8-sig'))
  print(f'nodes={len(d["nodes"])}, edges={len(d["edges"])}')
  assert len(d['edges']) > 5, 'Expected >5 script↔component edges'
  ```

- [ ] **Step 3: Merge into graph.json and save to cache**

  Run merge script with `CHUNK_FILE = 'graphify-out/.graphify_chunk_p5.json'`.

- [ ] **Step 4: Verify connectivity**

  Run connectivity check with `CHECK_IDS = [54, 55, 69, 77, 90, 100]`. All should show `CONNECTED`.

- [ ] **Step 5: Commit**

  ```
  git status
  git add graphify-out/.graphify_chunk_p5.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: connect ops scripts in graphify — graphify update"
  ```

---

## Task 6: Regenerate graph.html and GRAPH_REPORT.md

**What:** After all extraction passes, regenerate the visual outputs and report to reflect the improved graph.

- [ ] **Step 1: Count remaining isolated communities**

  ```python
  import json, networkx as nx
  from networkx.readwrite import json_graph
  from collections import defaultdict
  from pathlib import Path

  data = json.loads(Path('graphify-out/graph.json').read_bytes().decode('utf-8-sig'))
  G = json_graph.node_link_graph(data, edges='links')
  communities = defaultdict(list)
  for nid, ndata in G.nodes(data=True):
      cid = ndata.get('community')
      if cid is not None:
          communities[cid].append(nid)
  ext = defaultdict(int)
  for u, v in G.edges():
      cu, cv = G.nodes[u].get('community'), G.nodes[v].get('community')
      if cu is not None and cv is not None and cu != cv:
          ext[cu] += 1; ext[cv] += 1
  isolated = [cid for cid in communities if ext[cid] == 0]
  print(f'Isolated communities remaining: {len(isolated)} / {len(communities)}')
  ```

- [ ] **Step 2: Regenerate .graphify_labels.json**

  ```python
  import json, networkx as nx
  from networkx.readwrite import json_graph
  from pathlib import Path

  data = json.loads(Path('graphify-out/graph.json').read_bytes().decode('utf-8-sig'))
  G = json_graph.node_link_graph(data, edges='links')
  communities = {}
  for nid, ndata in G.nodes(data=True):
      cid = ndata.get('community')
      if cid is not None:
          communities.setdefault(cid, []).append(nid)
  degree = dict(G.degree())
  labels = {}
  for cid, members in communities.items():
      top = max(members, key=lambda n: degree.get(n, 0))
      labels[cid] = G.nodes[top].get('label', top)
  Path('graphify-out/.graphify_labels.json').write_text(
      json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False), encoding='utf-8')
  print(f'Labels written for {len(labels)} communities')
  ```

- [ ] **Step 3: Regenerate graph.html**

  Run the `regen_html.py` script from the Context section above.

  Expected output: `graph.html: N community nodes, M edges` where M > 248 (the previous count).

- [ ] **Step 4: Regenerate GRAPH_REPORT.md**

  ```powershell
  $py = Get-Content graphify-out\.graphify_python
  @'
  from graphify.analyze import god_nodes, surprising_connections, suggest_questions
  from graphify.report import generate
  from graphify.build import build_from_json
  import json
  from pathlib import Path
  from networkx.readwrite import json_graph

  data = json.loads(Path("graphify-out/graph.json").read_bytes().decode("utf-8-sig"))

  import networkx as nx
  G = json_graph.node_link_graph(data, edges="links")
  communities = {}
  for nid, ndata in G.nodes(data=True):
      cid = ndata.get("community")
      if cid is not None:
          communities.setdefault(cid, []).append(nid)

  labels_raw = json.loads(Path("graphify-out/.graphify_labels.json").read_text(encoding="utf-8"))
  labels = {int(k): v for k, v in labels_raw.items()}

  generate(G, communities, "graphify-out/GRAPH_REPORT.md", community_labels=labels, path=".")
  print("GRAPH_REPORT.md written")
  '@ | python
  ```

- [ ] **Step 5: Final commit**

  ```
  git status
  git add graphify-out/graph.html graphify-out/GRAPH_REPORT.md graphify-out/.graphify_labels.json graphify-out/graph.json graphify-out/cache/
  git commit -m "chore: regenerate graph.html and GRAPH_REPORT after isolated community passes — graphify update"
  ```
