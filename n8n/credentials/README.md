[Slovenščina](README_SL.md)

# n8n Credentials

Credential JSON files are **gitignored** and must never be committed.

## Required credentials

| Credential name | Type | Created by |
|----------------|------|------------|
| `BelPro Postgres` | PostgreSQL | `scripts/setup.sh` (automatic) |
| `BelPro API (Basic Auth)` | Basic Auth | `scripts/setup.sh` (automatic) |
| `BelPro API Internal Key` | HTTP Header Auth | `scripts/setup.sh` (automatic) |
| `BelPro Evolution API` | HTTP Header Auth | Manual (after WhatsApp setup) |
| `BelPro SMTP` | SMTP (Send Email node) | Manual (after SMTP setup) |

## Setup

`scripts/setup.sh` creates the first three credentials automatically during installation.
The remaining two require values that are not available at install time.

### Manual — BelPro Evolution API
After creating the Evolution API instance and copying its key to `.env` as `EVOLUTION_API_KEY`:
- Type: HTTP Header Auth
- Header name: `apikey`
- Value: `EVOLUTION_API_KEY` from `.env`

Then re-run: `python scripts/n8n_workflows.py import`

### Manual — BelPro SMTP
- Type: SMTP (Send Email node)
- Password: `SMTP_PASSWORD` from `.env`
- Host, port, user, and from-name: configured via the BelPro Settings UI (stored in DB)
- Works with Gmail (smtp.gmail.com:587 + App Password), Yahoo, Proton, or any SMTP server.
