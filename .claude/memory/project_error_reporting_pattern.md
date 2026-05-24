---
name: project-error-reporting-pattern
description: How to write to the error log (Dnevnik napak) from different parts of the stack — two pathways depending on caller location
metadata: 
  node_type: memory
  type: project
  originSessionId: d0df1aaf-d949-4f0a-a6a7-98526ac1d9e6
---

The `error_log` table (model: `api/models/error_log.py`) is the single destination for all operational failures. Two pathways reach it depending on where the caller runs:

**External callers (ops sidecar, n8n):** POST to `http://api:8000/api/errors` with header `X-Internal-Key: <API_SECRET_KEY>`. See `ops/scripts/backup.sh` and `ops/scripts/photo_cleanup.py` for examples.

**Internal API code:** Write an `ErrorLog` row directly via the open SQLAlchemy session — no HTTP roundtrip.

```python
from models.error_log import ErrorLog

db.add(ErrorLog(
    service="api",
    operation="send_monthly_reports",   # identifies the operation for filtering
    message="Short Slovenian label",    # shown in dashboard
    detail=detail,                      # full error string with context
))
# committed with the surrounding db.commit()
```

**Why:** code running inside the API process already has a DB session; self-calling the HTTP endpoint would add latency, require auth handling, and create a pointless network hop.

**Fields:**
- `service`: which service produced the error (`"api"`, `"ops"`, `"n8n"`)
- `operation`: which operation failed (freeform, used for filtering/display)
- `message`: short human-readable label (Slovenian, shown in Dnevnik napak)
- `detail`: full error string including recipient/context (can be None)
- `acknowledged`: defaults False; manager marks it read in the dashboard

**How to apply:** Any time API-internal code catches a delivery/processing failure that the manager should see in Dnevnik napak, add a `db.add(ErrorLog(...))` alongside the `logger.error(...)` call. Do not call `/api/errors` from within the API itself.
