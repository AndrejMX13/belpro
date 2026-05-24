---
name: reference-graphify-recovery
description: Recovery script order when graphify subagents write results to notifications instead of disk
metadata: 
  node_type: memory
  type: reference
  originSessionId: d0df1aaf-d949-4f0a-a6a7-98526ac1d9e6
---

When graphify subagents return results via task notifications instead of writing chunk files to disk, run these scripts from the project root in order instead of re-running extraction:

1. `scripts/graphify/check_cache.py` — which files are cached vs need extraction
2. `scripts/graphify/merge_semantic.py` — merge cached + new semantic results into `.graphify_semantic.json`
3. `scripts/graphify/merge_ast_semantic.py` — merge AST + semantic into `.graphify_extract.json`
4. `scripts/graphify/build_graph.py` — build graph, cluster, generate GRAPH_REPORT.md + graph.json

Each script operates on `.graphify_*.json` temp files in the project root. Outputs go to `graphify-out/`.
