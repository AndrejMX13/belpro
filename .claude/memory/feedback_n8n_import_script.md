---
name: feedback-n8n-import-script
description: "CRITICAL — always use scripts/n8n_workflows.py import after editing n8n workflow JSONs; this was skipped repeatedly causing wasted sessions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8584cb2b-0bd7-46dc-812c-4e2c852fb6d6
---

After editing any workflow JSON in `n8n/workflows/`, always import via:

```bash
python scripts/n8n_workflows.py import
```

This does upsert + activate via the n8n API in one shot, reads `N8N_API_KEY` from `.env`, and handles all three workflows at once.

**Why:** This was skipped repeatedly across multiple sessions, causing wasted debugging time. `docker compose exec n8n n8n import:workflow` deactivates the workflow and requires a separate activation step; it also needs the internal container path. The purpose-built script does upsert + activate in one shot and is the only correct way to apply workflow changes.

**How to apply:** Any time a workflow JSON in `n8n/workflows/` is modified — whether by hand, via n8n-mcp, or by a subagent — run the import script immediately before testing. Do not skip it, do not assume n8n picked up the change automatically.
