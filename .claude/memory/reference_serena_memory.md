---
name: reference-serena-memory
description: Serena memory directory is empty by design — all memories migrated to Claude Code memory system
metadata: 
  node_type: memory
  type: reference
  originSessionId: d0df1aaf-d949-4f0a-a6a7-98526ac1d9e6
---

Serena's memory directory exists but is intentionally empty. All project memories were migrated from Serena's store into the Claude Code file-based memory system (`~/.claude/projects/.../memory/`).

The empty directory is kept deliberately to prevent errors when Serena's CRUD tools attempt to access it.

**How to apply:** Currently, the Claude Code memory system holds all project knowledge. Serena memory tools may become relevant again in the future — don't treat them as permanently off-limits, just check whether anything is stored there before relying on them.
