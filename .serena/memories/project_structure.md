# Belpro — Project Structure

```
belpro/
├── docker-compose.yml         # All 7 services
├── .env.example               # Config template (never commit .env)
├── SPEC.md                    # Full system specification — read first
├── CLAUDE.md                  # Project coding instructions
├── db/
│   ├── init.sql               # Initial schema (run once by postgres container)
│   └── create_extra_dbs.sh    # Creates 'evolution' DB at init time
├── whisper/
│   ├── Dockerfile
│   └── transcribe.py          # HTTP wrapper around Faster-Whisper
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                # FastAPI entry point
│   ├── routers/               # Route modules per domain
│   ├── models/                # SQLAlchemy ORM models
│   ├── schemas/               # Pydantic request/response schemas
│   ├── services/              # Business logic (pdf_generator, exif_extractor)
│   └── db/migrations/         # Alembic migration files
├── frontend/
│   └── index.html             # Manager dashboard SPA
├── nginx/
│   └── nginx.conf             # Reverse proxy config
├── n8n/
│   ├── workflows/             # Exported n8n workflow JSONs
│   └── credentials/README.md
└── scripts/
    ├── setup.sh
    ├── backup.sh
    └── restore.sh
```

## Data model summary
- `managers` — one per instance, NGO profile
- `volunteers` — FK→managers, EMŠO encrypted
- `log_entries` — FK→volunteers, status enum, optional photo
- `monthly_reports` — FK→volunteers (null = consolidated)
