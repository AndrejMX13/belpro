---
name: Use graphify for file location before grep/Serena
description: Always read graphify-out/wiki/index.md first to locate files; only use grep or Serena after orientation
type: feedback
originSessionId: 76a454b6-285f-40e8-8f89-c8ccb7ebb548
---
Always start with `graphify-out/wiki/index.md` when looking for which file handles a feature or route. From the index, drill into the relevant community page to get the exact file. Only then use Serena `find_symbol` or `grep` for precise symbol lookup within that file.

**Why:** Graphify answers "which file?" at near-zero token cost. Jumping straight to grep or Serena pulls file content into context before knowing where to look — wasteful on tokens and context window.

**How to apply:** Any time the task starts with "find the file responsible for X" or "where is route/feature/model Y" — open the graphify wiki first, not grep or Serena.
