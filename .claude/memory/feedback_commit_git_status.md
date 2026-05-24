---
name: feedback-commit-git-status
description: Always run git status before committing to catch untracked/modified files like graphify outputs
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7b923962-a530-4052-811d-2f8b6fe8a487
---

Always run `git status` before staging/committing AND before suggesting any git actions to the user (push, amend, tag, etc.). Graphify output files (`graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`) are modified after every `graphify update .` and must be included in the same commit as the code change.

**Why:** Skipping `git status` left graphify files uncommitted after the volunteer email removal fix — caught before push. Also suggested "ready to push" after a compact when the commits were already on the remote — caught by the user.

**How to apply:** Before any `git add <specific-file> && git commit`, run `git status` first. Before suggesting the user push, tag, or take any git action, run `git status` and `git log --oneline central/main..HEAD` to verify the actual state.
