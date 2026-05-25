---
name: graphify-html-large-graph
description: How to generate graph.html when the graph exceeds the 5000-node HTML limit — aggregated community meta-graph via node_limit=1
metadata:
  type: feedback
---

The BelPro graph (8 553 nodes) exceeds graphify's default 5 000-node HTML limit, so `graph.html` is **not generated** by the normal pipeline.

## Two workarounds

### 1. Aggregated community meta-graph (recommended)

Pass `node_limit=1` to `to_html` — any value below the actual node count triggers aggregated mode, which renders 758 community nodes instead of 8 553 individual ones. Cross-community edge counts become edge weights.

```python
import json
from networkx.readwrite import json_graph
from graphify.export import to_html
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
labels_raw = json.loads(Path('graphify-out/.graphify_labels.json').read_text(encoding='utf-8'))

import networkx as nx
G = json_graph.node_link_graph(data, edges='links')

communities = {}
for nid, ndata in G.nodes(data=True):
    cid = ndata.get('community')
    if cid is not None:
        communities.setdefault(cid, []).append(nid)

labels = {int(k): v for k, v in labels_raw.items()}
to_html(G, communities, 'graphify-out/graph.html', community_labels=labels, node_limit=1)
```

Result: `graph.html` with 758 community nodes and 563 cross-community edges — fast and navigable.

### 2. Raise the env-var limit (full graph, slow)

```powershell
$env:GRAPHIFY_VIZ_NODE_LIMIT = "10000"
```

Then re-run the pipeline. The full 8 553-node graph renders but is sluggish in the browser.

**Why:** `to_html` checks `GRAPHIFY_VIZ_NODE_LIMIT` env var (default 5 000). When `node_limit` is passed explicitly and the graph exceeds it, graphify builds the community meta-graph instead of raising `ValueError`.
