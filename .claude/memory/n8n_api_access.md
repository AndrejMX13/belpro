---
name: n8n-api-access
description: n8n has separate internal (/rest/) and public (/api/v1/) API surfaces with different auth
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5e3ac5db-cd9e-4fd5-a92c-87d9a93aacce
---

n8n has TWO API surfaces:

- **`/rest/`** — Internal UI API. Uses cookie-based session auth (login via `/rest/login` with email+password). `X-N8N-API-KEY` header returns 401 on this path.
- **`/api/v1/`** — Public REST API. Uses `X-N8N-API-KEY` header with a JWT generated in Settings → n8n API. This is the correct path for programmatic access.

The MCP tools (n8n-mcp) use `/api/v1/` internally.

To export from the host when the API key doesn't work externally (potential IP/host restriction): run a Node.js script inside the n8n container via `docker compose exec -T n8n node -e "..."` calling `localhost:5678/api/v1/...`, write to `/tmp/`, then `docker compose cp n8n:/tmp/file.json <host-path>`.

The `./n8n/workflows` volume is mounted `:ro` — n8n cannot write exports there directly from inside the container.
