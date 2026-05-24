---
name: feedback-n8n-workflow-edits
description: Edit n8n workflow JSON directly on disk + import via script; never pass full workflow JSON through subagents or n8n-mcp update_full_workflow
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8584cb2b-0bd7-46dc-812c-4e2c852fb6d6
---

For n8n workflow changes, edit `n8n/workflows/*.json` directly with targeted grep + Edit tool, then push with `python scripts/n8n_workflows.py import`. Re-export after import to capture n8n normalisation, then commit all three workflow files together.

**Why:** The volunteer_entry workflow JSON is enormous. Passing it through subagents or n8n-mcp update_full_workflow fills context and fails. Direct file editing with surgical old_string/new_string is fast and reliable.

**How to apply:** Always use this approach for workflow node additions. Use grep to find node IDs, positions, and connection blocks. Only read the specific line ranges needed. Validate JSON with `python -c "import json; json.load(open(...))"` before importing.
