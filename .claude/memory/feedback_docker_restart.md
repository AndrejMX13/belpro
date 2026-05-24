---
name: docker compose restart vs rebuild
description: docker compose restart does NOT pick up code changes — must rebuild
type: feedback
originSessionId: 4be1c125-bd42-44b7-ad30-6b7c75405ac0
---
Always use `docker compose up -d --build <service>` after editing ANY files in the api/ directory — including tests — NOT `docker compose restart`.

**Why:** `restart` reuses the existing image layer — ALL source files (production code AND test files) are baked in at build time via `COPY . .` in the Dockerfile. Changes to `tests/conftest.py`, `tests/test_*.py`, etc. are invisible until the image is rebuilt. This caused a 6-session logo deletion mystery: every "fix" to `_clean_logo` was silently ignored because the container kept running the original fixture. The systematic debugger confirmed this via a `Path.unlink()` interceptor — the log file was never created because conftest.py changes hadn't been rebuilt in.

**How to apply:** Any time you edit files in `api/` (production or test), rebuild with `docker compose up -d --build api` before running tests. This is non-negotiable — without it, you are testing old code.
