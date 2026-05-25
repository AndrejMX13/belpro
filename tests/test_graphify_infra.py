"""
Tests for scripts/graphify_infra.py — inject Docker service topology into graph.json.
"""

import json
import sys
import textwrap
import pathlib

import pytest

# Make scripts/ importable
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import graphify_infra  # noqa: E402  (imported after sys.path manipulation)

# ---------------------------------------------------------------------------
# Minimal fixture data
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def node_ids(data):
    return {node["id"] for node in data["nodes"]}


def edge_triples(data):
    return {(e["source"], e["target"], e["relation"]) for e in data["links"]}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_service_nodes_created(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    ids = node_ids(load(g))
    assert "service_api" in ids
    assert "service_postgres" in ids
    assert "service_whisper" in ids
    assert "service_ops" in ids


def test_node_has_required_fields(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    data = load(g)
    api_node = next(node for node in data["nodes"] if node["id"] == "service_api")
    assert api_node["label"] == "api"
    assert api_node["file_type"] == "service"
    assert api_node["norm_label"] == "api"
    assert api_node["source_file"] == "docker-compose.yml"


def test_depends_on_dict_format(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    triples = edge_triples(load(g))
    assert ("service_api", "service_postgres", "depends_on") in triples


def test_depends_on_list_format(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    triples = edge_triples(load(g))
    assert ("service_ops", "service_api", "depends_on") in triples
    assert ("service_ops", "service_postgres", "depends_on") in triples


def test_env_url_calls_edges(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    triples = edge_triples(load(g))
    assert ("service_api", "service_whisper", "calls") in triples
    assert ("service_api", "service_ops", "calls") in triples


def test_nginx_proxies_to_edge(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    triples = edge_triples(load(g))
    assert ("service_frontend", "service_api", "proxies_to") in triples


def test_edges_are_extracted_confidence_1(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    data = load(g)
    for edge in data["links"]:
        assert edge["confidence"] == "EXTRACTED", f"bad confidence on {edge}"
        assert edge["confidence_score"] == 1.0, f"bad confidence_score on {edge}"


def test_idempotent_nodes(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    count_after_first = len(load(g)["nodes"])
    graphify_infra.inject(g, c, n)
    count_after_second = len(load(g)["nodes"])
    assert count_after_first == count_after_second


def test_idempotent_edges(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    count_after_first = len(load(g)["links"])
    graphify_infra.inject(g, c, n)
    count_after_second = len(load(g)["links"])
    assert count_after_first == count_after_second


def test_existing_nodes_preserved(tmp_graph):
    g, c, n = tmp_graph
    existing_graph = json.dumps({
        "nodes": [{"id": "existing_node", "label": "existing", "file_type": "code",
                   "source_file": "some.py", "source_location": "L1", "norm_label": "existing"}],
        "links": []
    })
    g.write_text(existing_graph, encoding="utf-8")
    graphify_infra.inject(g, c, n)
    ids = node_ids(load(g))
    assert "existing_node" in ids


def test_no_self_calls(tmp_graph):
    g, c, n = tmp_graph
    graphify_infra.inject(g, c, n)
    data = load(g)
    for edge in data["links"]:
        assert edge["source"] != edge["target"], f"self-call edge found: {edge}"
