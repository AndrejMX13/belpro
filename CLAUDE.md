# CLAUDE.md — Belpro

This file tells Claude Code how to work on the Belpro project. Read it before touching anything.

---

## What is this project?

Belpro (*Beleženje Prostovoljstva*) is a self-hosted system for Slovenian NGOs that automates volunteer work diaries required by law. Volunteers log work via WhatsApp voice notes and photos. A manager approves entries via WhatsApp and a web dashboard. Monthly PDF reports are generated for submission to CSD (Centre for Social Work).

Full details are in `SPEC.md`. Read it. Seriously.

---

## Project Structure

```
belpro/
├── docker-compose.yml         # All services
├── .env.example               # Config template
├── n8n/workflows/             # n8n workflow JSON exports
├── whisper/                   # Faster-Whisper HTTP service
├── api/                       # FastAPI backend + PDF generation
├── frontend/                  # Manager web dashboard (HTML/CSS/JS)
├── nginx/                     # Reverse proxy config
├── scripts/                   # setup.sh, backup.sh, restore.sh
├── docs/images/               # Project images (architecture diagrams, etc.)
└── db/                        # init.sql, Alembic migrations
```

---

## Technology Choices

| Concern | Choice | Why |
|---------|--------|-----|
| Language (scripts/API) | Python 3.11+ | Standard, good library support |
| API framework | FastAPI | Async, clean, good for small APIs |
| ORM | SQLAlchemy 2.x + Alembic | Standard Python ORM + migrations |
| Database | PostgreSQL 18.3 | Self-hosted, reliable |
| Workflow engine | n8n (self-hosted) | No-code glue, existing nodes for everything |
| Transcription | Faster-Whisper | CPU-optimised, runs locally |
| PDF | WeasyPrint | HTML→PDF, easy to template |
| EXIF | Pillow + piexif | Photo metadata extraction |
| Containerisation | Docker Compose | Simple, no Kubernetes |
| Frontend | Plain HTML + CSS + vanilla JS | No framework overhead |
| Email | n8n Gmail node | Already in stack |

**Principle:** Use existing n8n nodes first. Write custom code only when no node exists or the logic is too complex for a node. Keep it boring and maintainable.

---

## Coding Standards

### General
- Prefer explicit over clever.
- Every function/endpoint must have a docstring.
- Keep functions small and single-purpose.
- No premature optimisation.
- **ASCII-only identifiers.** Slovenian characters (č, š, ž, ć, đ) must never appear in variable names, function names, node names, file names, or any code identifiers. They are allowed exclusively in user-facing text (messages, labels, templates, PDF content). Use `c`, `s`, `z`, `c`, `d` instead.

### Python
- Type hints everywhere.
- Use Pydantic models for all request/response schemas.
- SQLAlchemy models in `api/models/`, Pydantic schemas in `api/schemas/`.
- Use `async`/`await` throughout FastAPI routes.
- Format with `black`, lint with `ruff`.
- Never commit secrets. Use environment variables via `python-dotenv`.

### n8n Workflows
- Export workflows as JSON and commit to `n8n/workflows/`.
- One workflow per logical flow (entry submission, approval, monthly reports).
- Name nodes clearly — no "Set1", "HTTP Request3" etc.
- Add sticky notes to explain non-obvious logic in workflows.
- Credentials are never committed. Document required credential names in `n8n/credentials/README.md`.

### Frontend
- Mobile-first, responsive.
- No heavy frameworks. Vanilla JS is fine.
- All API calls to the FastAPI backend, no direct DB access from frontend.
- Keep it functional and clean. This is a tool for NGO managers, not a showcase.

### SQL / Database
- All schema changes via Alembic migrations. Never edit `init.sql` after first run.
- EMŠO must be encrypted at rest. Use application-level AES-256 (via `cryptography` library) before writing to DB.
- Use UUIDs as primary keys, not serial integers.

---

## Environment Variables

All configuration via `.env`. See `.env.example` for all required variables. Key ones:

```
# PostgreSQL
POSTGRES_DB=belpro
POSTGRES_USER=belpro
POSTGRES_PASSWORD=...
DATABASE_URL=postgresql+asyncpg://...

# Encryption
EMSO_ENCRYPTION_KEY=...   # 32-byte key, base64 encoded

# n8n
N8N_BASIC_AUTH_USER=...
N8N_BASIC_AUTH_PASSWORD=...

# Evolution API (WhatsApp)
EVOLUTION_API_KEY=...
EVOLUTION_INSTANCE_NAME=...

# Whisper
WHISPER_MODEL=large-v3     # recommended; medium if RAM is limited
WHISPER_LANGUAGE=sl

# FastAPI
API_SECRET_KEY=...
MANAGER_PASSWORD=...       # Simple single-manager auth for now

# Gmail
GMAIL_ADDRESS=...
GMAIL_APP_PASSWORD=...     # Or OAuth token path
```

---

## Key Business Rules (encode these correctly)

1. **Entry statuses flow one way:** `pending_volunteer` → `pending_manager` → `approved` or `rejected`. Never backwards.
2. **Photo is optional.** Never block an entry because there's no photo. Manager decides.
3. **Volunteer confirmation dialog has four options:** 1 Potrdi, 2 Popravi, 3 Dodaj slike, 4 Prekliči. No limit on correction attempts — the volunteer may re-submit as many times as needed before confirming. Prekliči discards the entry entirely. "Dodaj slike" enters a photo sub-mode (1 Potrdi, 3 Več slik, 4 Prekliči).
4. **Manager is singular.** One manager per instance. No multi-user auth needed for v1.
5. **Monthly report deadline:** 28th of each month (cron), covering the current month. Manager can trigger manually at any time.
6. **Slovenian only.** All WhatsApp bot messages in Slovenian. Whisper language hint: `sl`.
7. **EMŠO is sensitive.** Encrypt before storing. Never log it. Mask last 3 digits in any PDF that a volunteer receives (the manager consolidated report may show full EMŠO if legally required).
8. **Single-tenant.** There is no concept of multiple NGOs in one instance. Every deployment is one NGO.
9. **Name fields:** Use `first_name` in informal WhatsApp messages to volunteers. Use `first_name + last_name` in formal documents, PDFs, and the manager dashboard.
10. **Address fields:** `street` (name + house number), `postal_code` (4-digit Slovenian), `city`. Never a single freetext address field.

---

## Local Development

**Environment:** Windows 10 + WSL2 (Ubuntu) + Docker Desktop. Docker Compose runs via Docker Desktop (WSL2 backend).

**Python on the host:** Python 3.14 is installed on Windows. Use `python` (not `python3`) in all scripts, commands, and shebangs — `python3` resolves via a shim but `python` is the canonical command. Docker containers use their own Python environment.

```bash
# Copy and fill in environment
cp .env.example .env

# Start all services
docker compose up -d

# Run DB migrations
docker compose exec api alembic upgrade head

# Tail logs
docker compose logs -f

# Access points:
# Dashboard:   http://localhost:80
# FastAPI docs: http://localhost:8100/docs
# n8n:         http://localhost:5678
# Evolution API: http://localhost:8180
```

---

## Tooling & Shell Conventions

- **Use the Bash tool for all commands** including `docker compose`. The Bash tool runs Git Bash (MINGW64), not WSL2. VS Code runs as a Windows-local app; the working directory is `/d/Andrej/vsCode-workspace/BelPro` (Git Bash path format).
- **Path format:** Git Bash uses `/c/` and `/d/` drive prefixes — not Windows backslashes, not `/mnt/`. Example: `C:\Users\Andrej` → `/c/Users/Andrej`.
- **WSL2 bash** is installed but not usable as the Bash tool shell. For one-off WSL2 commands use PowerShell: `wsl bash -c 'command'`.
- **Rebuild after code changes:** `docker compose up -d --build <svc>` — never `docker compose restart`, which skips the build.
- **pytest path inside the API container:** `docker compose exec api pytest tests/ -v` — the path is `tests/`, not `api/tests/`. The Dockerfile uses `api/` as build context, so `api/tests/` on the host becomes `tests/` at `/app/tests/` inside the container.
- **Git remote is named `central`**, not `origin`. Use `git push central <branch>`.
- **AI-assisted commits** must include a `Co-Authored-By` trailer. Use the actual model from session context:
  - Anthropic model (Claude): `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` (substitute the actual model name)
  - Third-party or unknown model: `Co-Authored-By: AI Assistant <noreply@ai>`
- **Serena `replace_symbol_body` corrupts decorated functions and module-level strings.** Use the Edit tool for all in-place code edits instead.

### Known packaging pins

These must be explicit in `requirements.txt` — transitive resolution gets them wrong:

- `email-validator` — required alongside `pydantic[email]`; omitting it causes an import error at runtime.
- `pydyf==0.10.0` — required alongside `weasyprint==62.3`; a newer `pydyf` breaks PDF generation silently.

---

## Adding a New Feature

1. Check `SPEC.md` first — if the feature isn't there, discuss before building.
2. Write or update the Alembic migration if the DB changes.
3. Add/update Pydantic schemas before writing route logic.
4. Update the relevant n8n workflow JSON if the flow changes.
5. Keep `SPEC.md` up to date if behaviour changes materially.

---

## n8n Workflows
- All workflow creation and validation must use n8n-mcp tools — never write workflow JSON by hand
- Before working on any n8n workflow, read the n8n skills in .claude/skills/
- n8n API connection is configured in .mcp.json (URL: http://localhost:5678, key added after first container run)
- Workflows are exported as JSON and committed to n8n/workflows/ — one file per logical flow

---

## Project Memory

This project uses a persistent memory system at `~/.claude/projects/<project>/memory/`. `MEMORY.md` is an index automatically loaded into every conversation, but individual memory files must be consulted actively.

- **At the start of every session**, read `MEMORY.md` and the relevant individual memory files before taking any action. This is not optional — the same rule as graphify orientation.
- **When patterns recur**, write them to memory — feedback (corrections/confirmations), project state, and user preferences. Link related memories with `[[name]]`.
- **Never write code patterns, file paths, or architecture to memory** — those are derivable from the codebase. Memory is for behavioral feedback, project decisions, and user context.
- **After every session that modifies code**, run `graphify update .`.

---

## What NOT to do

- **Don't start with `glob` or `grep` for discovery.** If `graphify-out/wiki/index.md` exists, read it first to identify relevant communities and files. Once you know the target area, use Serena `find_symbol` for code or `grep` for non-code assets (logs, config, raw text). Use `grep` only for targeted lookups once you know the file area — never as a substitute for orientation.
- Do not build multi-tenant features. Out of scope for v1.
- Do not add a frontend JavaScript framework (React, Vue, etc.) — plain JS only.
- Do not store photos in cloud storage. Local filesystem only.
- Do not add non-Slovenian language support.
- Do not expose EMŠO in logs, API responses to frontend, or volunteer-facing PDFs (beyond partial masking).
- Do not use `root` user in Docker containers.
- Do not skip Alembic migrations for schema changes.

## graphify & serena

This project uses a Graphify knowledge graph (`graphify-out/`) for orientation and Serena for precise symbol navigation. Think of them as complementary, not competing:

| Tool | Best for | Not for |
|------|----------|---------|
| **Graphify wiki** (`graphify-out/wiki/index.md`) | "Which parts of the codebase handle X?" — identifies relevant communities and files in seconds | Understanding logic, reading actual code |
| **Graphify report** (`graphify-out/GRAPH_REPORT.md`) | God nodes, surprising connections, architectural overview | Finding specific function definitions |
| **Serena** (`find_symbol`, `find_referencing_symbols`) | "Where is X defined?", "Who calls Y?", precise symbol navigation | High-level orientation, architectural mapping |

### Workflow

1. **Orient** — If `graphify-out/wiki/index.md` exists, read it first to identify which communities are relevant to your question. This tells you *where* to look, not what the code does.
2. **Locate** — Use Serena `find_symbol` to find specific functions, classes, or methods within the identified files, or `find_referencing_symbols` to trace callers.
3. **Read** — Read the actual source files to understand logic. The graph tells you which files matter; it does not replace reading them.
4. **Maintain** — After modifying code files, run `graphify update .` to keep the graph current (AST-only, no API cost).