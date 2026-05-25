"""Rebuild the graphify wiki from the current graph.json and community labels."""

import json
from pathlib import Path

import networkx as nx
from graphify.wiki import to_wiki

out = Path("graphify-out")

data = json.loads((out / "graph.json").read_text(encoding="utf-8"))
G = nx.node_link_graph(data, edges="links")

labels = {
    int(k): v
    for k, v in json.loads(
        (out / ".graphify_labels.json").read_text(encoding="utf-8")
    ).items()
}

communities: dict[int, list] = {}
for node, attrs in G.nodes(data=True):
    cid = attrs.get("community")
    if cid is not None:
        communities.setdefault(int(cid), []).append(node)

count = to_wiki(G, communities, out / "wiki", community_labels=labels)
print(f"Wiki rebuilt: {count} articles written")
