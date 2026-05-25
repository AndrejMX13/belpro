# graphify semantic rebuild

## Problem

`graphify-out/graph.json` has 8 553 nodes and 758 communities but **zero semantic extraction** — every build so far was AST-only (Python imports/calls). Cross-layer connections are missing: frontend ↔ backend, WhatsApp flows ↔ approval handlers, n8n workflows ↔ API endpoints. The community meta-graph looks disconnected because of this.

## What to run

From the project root in PowerShell or Git Bash — a **full rebuild**, not `--update`:

```
/graphify .
```

This will:
- AST-extract 133 code files (fast, free)
- Semantically extract 212 docs + 5 papers + 19 images (~11 subagent chunks in parallel, 1–2 min)
- Rebuild graph, cluster, write GRAPH_REPORT.md

**Skip or ignore Step 5 (LLM community labelling)** — we label communities from the graph itself instead (see script below). With 758 communities the LLM step is unreliable and produces "Community N" placeholders anyway.

## After the rebuild — step 1: generate community labels from graph data

Run this before generating graph.html. It labels each community by its highest-degree member and saves the result so GRAPH_REPORT.md and graph.html both use real names.

```python
import json
import networkx as nx
from networkx.readwrite import json_graph
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
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

# Save for graph.html step
Path('graphify-out/.graphify_labels.json').write_text(
    json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False),
    encoding='utf-8'
)
print(f'Labels written for {len(labels)} communities')
print('Sample:', list(labels.items())[:5])
```

## After the rebuild — step 2: regenerate graph.html

The graph will exceed the 5 000-node HTML limit. Run this script to produce the aggregated community meta-graph with solid edges and top-node labels:

```python
import json
import networkx as nx
from networkx.readwrite import json_graph
from graphify.export import to_html
from pathlib import Path
from collections import Counter

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
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

# Override with real labels from Step 5 if available
labels_path = Path('graphify-out/.graphify_labels.json')
if labels_path.exists():
    raw = json.loads(labels_path.read_text(encoding='utf-8'))
    for k, v in raw.items():
        if not v.startswith('Community '):   # skip placeholders
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

meta_communities = {cid: [str(cid)] for cid in communities}
mc = {cid: len(members) for cid, members in communities.items()}

to_html(meta, meta_communities, 'graphify-out/graph.html',
        community_labels=community_labels, member_counts=mc)
print(f'graph.html: {meta.number_of_nodes()} community nodes, {meta.number_of_edges()} edges')
```

## Commit format

```
chore: full graphify semantic rebuild — graphify update

First semantic extraction pass: 212 docs + 5 papers + 19 images.
Adds cross-layer edges (frontend↔backend, n8n↔API, WhatsApp flows↔approval).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
