# Belpro — Code Style & Conventions

## Python
- Type hints everywhere
- Docstring on every function/endpoint (CLAUDE.md requirement)
- Pydantic models for all request/response schemas
- SQLAlchemy models → `api/models/`
- Pydantic schemas → `api/schemas/`
- `async`/`await` throughout FastAPI routes
- Format: `black`, lint: `ruff`
- No secrets in code — env vars via `python-dotenv`
- UUID primary keys (not serial integers)

## EMŠO handling
- Always encrypt before DB write (AES-256, `cryptography` lib)
- Never log EMŠO
- Mask last 3 digits in volunteer-facing PDFs
- Full EMŠO only in manager consolidated report

## Entry status flow (one-way only)
`pending_volunteer` → `pending_manager` → `approved` | `rejected`

## Database changes
- Always via Alembic migrations
- Never edit `db/init.sql` after first run

## Frontend
- Mobile-first, responsive
- No JS frameworks — vanilla only
- All data via FastAPI, never direct DB

## n8n workflows
- Export JSON to `n8n/workflows/`
- One file per logical flow
- No "Set1" / "HTTP Request3" node names
- Sticky notes for non-obvious logic
- Never commit credentials
