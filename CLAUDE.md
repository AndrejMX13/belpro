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
WHISPER_MODEL=medium       # or large-v3 if resources allow
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
3. **Volunteer confirmation dialog has three buttons:** Potrdi, Popravi, Prekliči. No limit on correction attempts — the volunteer may re-submit as many times as needed before confirming. Prekliči discards the entry entirely.
4. **Manager is singular.** One manager per instance. No multi-user auth needed for v1.
5. **Monthly report deadline:** 28th of each month (cron), covering the current month. Manager can trigger manually at any time.
6. **Slovenian only.** All WhatsApp bot messages in Slovenian. Whisper language hint: `sl`.
7. **EMŠO is sensitive.** Encrypt before storing. Never log it. Mask last 3 digits in any PDF that a volunteer receives (the manager consolidated report may show full EMŠO if legally required).
8. **Single-tenant.** There is no concept of multiple NGOs in one instance. Every deployment is one NGO.
9. **Name fields:** Use `first_name` in informal WhatsApp messages to volunteers. Use `first_name + last_name` in formal documents, PDFs, and the manager dashboard.
10. **Address fields:** `street` (name + house number), `postal_code` (4-digit Slovenian), `city`. Never a single freetext address field.

---

## Local Development

**Environment:** Windows 10 + WSL2 (Ubuntu) + Docker Desktop. All shell commands, scripts, and paths assume WSL2 Linux context. Do not use Windows-style paths (`C:\...`). Docker Compose runs via WSL2 terminal.

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
# FastAPI docs: http://localhost:8000/docs
# n8n:         http://localhost:5678
# Evolution API: http://localhost:8080
```

---

## Adding a New Feature

1. Check `SPEC.md` first — if the feature isn't there, discuss before building.
2. Write or update the Alembic migration if the DB changes.
3. Add/update Pydantic schemas before writing route logic.
4. Update the relevant n8n workflow JSON if the flow changes.
5. Keep `SPEC.md` up to date if behaviour changes materially.

---

## What NOT to do

- Do not build multi-tenant features. Out of scope for v1.
- Do not add a frontend JavaScript framework (React, Vue, etc.) — plain JS only.
- Do not store photos in cloud storage. Local filesystem only.
- Do not add non-Slovenian language support.
- Do not expose EMŠO in logs, API responses to frontend, or volunteer-facing PDFs (beyond partial masking).
- Do not use `root` user in Docker containers.
- Do not skip Alembic migrations for schema changes.
