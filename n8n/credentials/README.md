[Slovenščina](README_SL.md)

# n8n Credentials

Credential JSON files are **gitignored** and must never be committed.

## Required credentials

| Credential name | Type | Used by |
|----------------|------|---------|
| `BelPro Postgres` | PostgreSQL | All DB nodes |
| `BelPro SMTP` | SMTP (Send Email node) | Monthly PDF delivery, notifications |
| `BelPro Evolution API` | HTTP Header Auth | WhatsApp send nodes |
| `BelPro API (Basic Auth)` | Basic Auth | All FastAPI backend calls (almost every node) |
| `BelPro API Internal Key` | HTTP Header Auth | Error handler workflow (`error_handler.json`) |

## Setup

After starting the stack (`docker compose up -d`), open n8n at
http://localhost:5678 and create each credential manually under
**Settings → Credentials → New Credential**.

- **PostgreSQL:** host `postgres`, port `5432`, database `belpro`,
  user/password from `.env`
- **SMTP:** use the Send Email node credential. Host, port, user, and from-name
  are set via the BelPro Settings UI (stored in DB). Password from `SMTP_PASSWORD`
  in `.env`. Works with Gmail (smtp.gmail.com:587 + App Password), Yahoo, Proton,
  or any SMTP server.
- **Evolution API:** Header `apikey: <EVOLUTION_API_KEY from .env>`
- **BelPro API (Basic Auth):** username = `admin`, password = `MANAGER_PASSWORD` from `.env`.
- **BelPro API Internal Key:** Header name `X-Internal-Key`, value = `API_SECRET_KEY` from `.env`.
