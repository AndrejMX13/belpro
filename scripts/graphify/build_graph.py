import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate

extract = json.loads(Path('.graphify_extract.json').read_text())
detect = json.loads(Path('.graphify_incremental.json').read_text())

graph = build_from_json(extract)
print(f'Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges')

communities = cluster(graph)
print(f'Clusters: {len(communities)} communities')

scores = score_all(graph, communities)

degree = dict(graph.degree())
community_labels = {}
for cid, node_ids in communities.items():
    top_node = max(node_ids, key=lambda n: degree.get(n, 0))
    node_label = graph.nodes[top_node].get('label', top_node)
    community_labels[cid] = node_label

gods = god_nodes(graph)
surprises = surprising_connections(graph, communities)
questions = suggest_questions(graph, communities, community_labels)

detection_result = {
    'total_files': detect.get('new_total', detect.get('total_files', 0)),
    'total_words': detect.get('total_words', 0),
    'warning': detect.get('warning', ''),
    'communities': [{'id': cid, 'label': community_labels[cid], 'size': len(node_ids)}
                    for cid, node_ids in communities.items()],
}

token_cost = {
    'input': extract.get('input_tokens', 0),
    'output': extract.get('output_tokens', 0),
}

report = generate(
    graph, communities, scores, community_labels,
    gods, surprises, detection_result, token_cost,
    root=str(Path.cwd()),
    suggested_questions=questions
)
Path('graphify-out/GRAPH_REPORT.md').write_text(report, encoding='utf-8')
print(f'Report written to graphify-out/GRAPH_REPORT.md')

graph_data = {
    'nodes': [{'id': n, **graph.nodes[n]} for n in graph.nodes()],
    'edges': [{'source': u, 'target': v, **graph.edges[u, v]} for u, v in graph.edges()],
}
Path('graphify-out/graph.json').write_text(json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'graph.json written ({len(graph_data["nodes"])} nodes, {len(graph_data["edges"])} edges)')
