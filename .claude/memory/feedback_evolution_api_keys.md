---
name: Evolution API key distinction
description: AUTHENTICATION_API_KEY and EVOLUTION_API_KEY are different keys — do not treat them as the same value
type: feedback
originSessionId: 122e40c2-5d71-438d-a439-5da1da6d07c3
---
Do NOT assume `AUTHENTICATION_API_KEY` and `EVOLUTION_API_KEY` are the same value.

- `AUTHENTICATION_API_KEY`: global key that secures the Evolution API server itself. You choose/generate this before starting the container. Used to log into the manager dashboard at `:8180/manager/` and make admin API calls.
- `EVOLUTION_API_KEY`: instance-level key generated inside Evolution API when creating a specific instance (e.g. `belpro`). Copied from the instance detail page after the instance is created. Used by the FastAPI backend to make calls scoped to that instance.

**Why:** Past sessions assumed these were the same and set them to equal values, causing connection issues.

**How to apply:** Always describe them as separate variables with separate sources whenever editing `.env.example`, `README.md`, or any documentation.
