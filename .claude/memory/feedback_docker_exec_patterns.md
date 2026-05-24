---
name: docker-exec-and-shell-tool-patterns
description: Shell tool choice and pytest path patterns for docker compose commands in this project
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65bc1a57-ac1d-4937-b8b2-7563068bcf34
---

**Rule 1: Use Bash tool for all docker compose commands.**
VS Code is opened from a WSL2 terminal (`code .` from `/mnt/d/Andrej/vsCode-workspace/BelPro`), so the Bash tool runs in WSL2 bash with full access to `/mnt/d/`. The PowerShell workaround is no longer needed.

**Why:** WSL2 terminal switch completed 2026-05-12. Previously the Bash tool lacked the `/mnt/d/` mount; that issue no longer exists.

**How to apply:** Use Bash tool for `docker compose` and all other commands. PowerShell tool only if explicitly needed for Windows-specific operations.

---

**Rule 2: pytest path inside the container is `tests/`, not `api/tests/`.**
`docker compose exec api pytest api/tests/` returns "file or directory not found" because the container WORKDIR is `/app` and the tests are copied there as `tests/` (from `api/tests/` on the host).

**Why:** The Dockerfile does `COPY . .` from `api/` context, so `api/tests/` on host → `tests/` inside container.

**How to apply:** Always run `docker compose exec api pytest tests/ -v` (no `api/` prefix).
