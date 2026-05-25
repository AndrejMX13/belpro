"""
graphify_infra.py — Inject Docker service topology into graphify-out/graph.json.

Parses docker-compose.yml and nginx/nginx.conf to extract service nodes and
inter-service edges (depends_on, env-URL calls, nginx proxy_pass), then patches
the graph.json used by the Graphify knowledge graph.

Usage (standalone):
    python scripts/graphify_infra.py

The script is also importable as a module; the main entry point is inject().
"""

import json
import pathlib
import re
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Default paths (resolved relative to this script's location)
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPTS_DIR.parent

GRAPH_FILE = _PROJECT_ROOT / "graphify-out" / "graph.json"
COMPOSE_FILE = _PROJECT_ROOT / "docker-compose.yml"
NGINX_FILE = _PROJECT_ROOT / "nginx" / "nginx.conf"

# ---------------------------------------------------------------------------
# Regex: match `set $<varname> <hostname>:<port>` in nginx config
# ---------------------------------------------------------------------------
_NGINX_UPSTREAM_RE = re.compile(r"set\s+\$\w+\s+(\w[\w-]*):\d+")

# ---------------------------------------------------------------------------
# The Docker service name that corresponds to the nginx container.
# Used as the source node in proxies_to edges extracted from nginx.conf.
# ---------------------------------------------------------------------------
_NGINX_SERVICE_NAME = "frontend"

# ---------------------------------------------------------------------------
# Regex: match http(s)://hostname:port  OR  http(s)://hostname  in env values
# ---------------------------------------------------------------------------
_ENV_URL_RE = re.compile(r"https?://([a-zA-Z][a-zA-Z0-9_-]*)(?::\d+)?")


def _service_node_id(name: str) -> str:
    """Convert a Docker service name to a graph node ID."""
    return f"service_{name.replace('-', '_')}"


def _make_node(name: str, svc: dict[str, Any]) -> dict[str, Any]:
    """Build a graph node dict for a Docker service."""
    node: dict[str, Any] = {
        "id": _service_node_id(name),
        "label": name,
        "norm_label": name,
        "file_type": "service",
        "source_file": "docker-compose.yml",
        "source_location": f"services.{name}",
        "image": svc.get("image") or f"custom build (./{name})",
    }
    if "ports" in svc:
        node["ports"] = svc["ports"]
    return node


def _make_edge(
    source: str,
    target: str,
    relation: str,
    source_file: str,
    source_location: str,
) -> dict[str, Any]:
    """Build a graph edge dict."""
    return {
        "source": source,
        "target": target,
        "relation": relation,
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "weight": 1.0,
        "source_file": source_file,
        "source_location": source_location,
    }


def _extract_compose_data(
    compose: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Extract service nodes and edges from a parsed docker-compose structure.

    Returns (nodes, edges).
    """
    services: dict[str, Any] = compose.get("services", {})
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for name, svc in services.items():
        if svc is None:
            svc = {}
        nodes.append(_make_node(name, svc))
        src_id = _service_node_id(name)

        # ── depends_on edges ──────────────────────────────────────────────
        depends_on = svc.get("depends_on")
        if depends_on:
            if isinstance(depends_on, dict):
                deps = list(depends_on.keys())
            else:
                # list format
                deps = list(depends_on)
            for dep in deps:
                tgt_id = _service_node_id(dep)
                if src_id != tgt_id:
                    edges.append(
                        _make_edge(
                            src_id,
                            tgt_id,
                            "depends_on",
                            "docker-compose.yml",
                            f"services.{name}.depends_on",
                        )
                    )

        # ── env-URL call edges ────────────────────────────────────────────
        environment = svc.get("environment") or {}
        if isinstance(environment, list):
            # KEY=value list format — convert to dict
            env_dict: dict[str, str] = {}
            for item in environment:
                if "=" in item:
                    k, _, v = item.partition("=")
                    env_dict[k] = v
            environment = env_dict

        for env_key, env_val in environment.items():
            if not isinstance(env_val, str):
                continue
            for match in _ENV_URL_RE.finditer(env_val):
                hostname = match.group(1)
                # Only create an edge if hostname matches a known service
                if hostname in services and hostname != name:
                    tgt_id = _service_node_id(hostname)
                    edges.append(
                        _make_edge(
                            src_id,
                            tgt_id,
                            "calls",
                            "docker-compose.yml",
                            f"services.{name}.environment.{env_key}",
                        )
                    )

    return nodes, edges


def _extract_nginx_edges(nginx_text: str, known_services: set[str]) -> list[dict[str, Any]]:
    """
    Extract proxies_to edges from nginx config.

    Matches the variable-upstream pattern:  set $<var> <hostname>:<port>
    Source is always ``service_{_NGINX_SERVICE_NAME}`` (the nginx container).
    Only emits an edge when the resolved hostname is present in ``known_services``
    to avoid dangling edges pointing at non-existent nodes.
    """
    src_id = f"service_{_NGINX_SERVICE_NAME}"
    edges: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in _NGINX_UPSTREAM_RE.finditer(nginx_text):
        hostname = match.group(1)
        if hostname not in known_services:
            continue
        tgt_id = _service_node_id(hostname)
        if tgt_id not in seen:
            seen.add(tgt_id)
            edges.append(
                _make_edge(
                    src_id,
                    tgt_id,
                    "proxies_to",
                    "nginx/nginx.conf",
                    "server.location.proxy_pass",
                )
            )
    return edges


def inject(
    graph_file: pathlib.Path,
    compose_file: pathlib.Path,
    nginx_file: pathlib.Path,
) -> dict[str, int]:
    """
    Inject Docker service topology nodes and edges into graph.json.

    Reads the three source files, patches graph.json in place (idempotent),
    and returns a summary dict with keys 'nodes_added' and 'edges_added'.
    """
    if not graph_file.exists():
        print(f"ERROR: graph.json not found at {graph_file}. Run 'graphify update .' first.")
        raise SystemExit(1)

    # Read graph (UTF-8 with optional BOM)
    raw = graph_file.read_bytes().decode("utf-8-sig")
    graph: dict[str, Any] = json.loads(raw)
    existing_nodes: list[dict[str, Any]] = graph.setdefault("nodes", [])
    existing_edges: list[dict[str, Any]] = graph.setdefault("links", [])

    # Build lookup sets for idempotency
    existing_node_ids: set[str] = {n["id"] for n in existing_nodes}
    existing_edge_triples: set[tuple[str, str, str]] = {
        (e["source"], e["target"], e["relation"]) for e in existing_edges
    }

    # Parse compose
    compose_text = compose_file.read_text(encoding="utf-8")
    compose = yaml.safe_load(compose_text)
    services: dict[str, Any] = (compose or {}).get("services", {})
    new_nodes, compose_edges = _extract_compose_data(compose)

    # Parse nginx
    nginx_text = nginx_file.read_text(encoding="utf-8")
    nginx_edges = _extract_nginx_edges(nginx_text, set(services.keys()))

    all_edges = compose_edges + nginx_edges

    # Build a lookup from node ID to index for in-place patching
    node_index: dict[str, int] = {n["id"]: i for i, n in enumerate(existing_nodes)}

    # Inject nodes (append new, patch skeleton nodes in place)
    nodes_added = 0
    nodes_patched = 0
    for node in new_nodes:
        nid = node["id"]
        if nid not in existing_node_ids:
            existing_nodes.append(node)
            existing_node_ids.add(nid)
            node_index[nid] = len(existing_nodes) - 1
            nodes_added += 1
        elif existing_nodes[node_index[nid]].get("file_type") != "service":
            # Skeleton node exists but lacks service typing — patch in place
            existing_nodes[node_index[nid]].update(node)
            nodes_patched += 1
        # else: already a fully-typed service node — skip (idempotent)

    # Inject edges (skip self-loops and duplicates)
    edges_added = 0
    for edge in all_edges:
        if edge["source"] == edge["target"]:
            continue
        triple = (edge["source"], edge["target"], edge["relation"])
        if triple not in existing_edge_triples:
            existing_edges.append(edge)
            existing_edge_triples.add(triple)
            edges_added += 1

    # Write back (UTF-8, no BOM — standard for JSON)
    graph_file.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {"nodes_added": nodes_added, "nodes_patched": nodes_patched, "edges_added": edges_added}
    print(
        f"graphify_infra: injected {result['nodes_added']} nodes, "
        f"patched {result['nodes_patched']} existing, "
        f"{result['edges_added']} edges -> {graph_file}"
    )
    return result


if __name__ == "__main__":
    inject(GRAPH_FILE, COMPOSE_FILE, NGINX_FILE)
