# Belpro — Tech Stack

| Layer | Technology |
|-------|-----------|
| Containerisation | Docker Compose (all services) |
| Database | PostgreSQL 18.3 |
| Workflow engine | n8n (self-hosted, port 5678) |
| WhatsApp gateway | Evolution API (port 8180 host / 8080 container) |
| Transcription | Faster-Whisper CPU (internal port 8001) |
| API backend | FastAPI + SQLAlchemy 2.x + asyncpg + Alembic |
| PDF generation | WeasyPrint (HTML→PDF) |
| EXIF extraction | Pillow + piexif |
| Frontend | Plain HTML + CSS + vanilla JS (served by nginx port 80) |
| Email | n8n Gmail node |
| In-memory queue | Redis 7 (for Evolution API) |

**Port map (host:container):**
- nginx dashboard: 80:80
- n8n: 5678:5678
- FastAPI: 8100:8000
- Evolution API: 8180:8080
- Whisper: internal only (8001)

**Python version:** 3.11+
**Async driver:** asyncpg (postgresql+asyncpg://)
