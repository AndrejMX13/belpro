# Belpro — Beleženje Prostovoljstva

Self-hosted system for Slovenian NGOs that automates the *Dnevnik prostovoljskega dela* (Volunteer Work Diary) required by Slovenian law for volunteers receiving the Work Activity Allowance (*Dodatek za delovno aktivnost*).

Volunteers log work via **WhatsApp** (voice notes, photos, or text). A manager reviews and approves entries via WhatsApp and a web dashboard. Monthly PDF reports are generated automatically for submission to the local CSD (Centre for Social Work).

---

## How it works

```
Volunteer (WhatsApp)
        │
        ▼
Evolution API  ──────────────────────────────┐
        │                                    │
        ▼                                    │
  n8n Workflow ◄── Faster-Whisper (local)    │
        │                                    │
        ├──► PostgreSQL                       │
        │                                    │
        ├──► FastAPI + Web Dashboard ◄────────┘
        │
        └──► Gmail (monthly PDFs, notifications)
```

1. Volunteer sends a voice note, photo, or text message to the NGO's WhatsApp number.
2. n8n transcribes audio via Faster-Whisper (local, CPU, Slovenian), extracts date/hours/location/activity, and sends the volunteer a confirmation summary with Potrdi / Popravi / Prekliči buttons.
3. On confirmation, the entry moves to `pending_manager` and the manager gets a WhatsApp notification with Approve / Reject buttons.
4. On the 28th of each month, PDFs are generated automatically and emailed — one per volunteer (for CSD submission) and a consolidated one to the manager.

---

## Stack

| Service | Technology | Port |
|---------|-----------|------|
| Database | PostgreSQL 18 | internal |
| Workflow engine | n8n | 5678 |
| Speech-to-text | Faster-Whisper (CPU) | internal |
| Backend API | FastAPI | 8100 |
| Manager dashboard | nginx + HTML/JS/CSS | 80 |
| WhatsApp gateway | Evolution API | 8180 |
| Cache/queue | Redis 7 | internal |

---

## Requirements

- Docker and Docker Compose (v2)
- 2 CPU cores, 4 GB RAM minimum (Whisper `medium` model)
- 8 GB RAM recommended for `large-v3` Whisper model
- A dedicated WhatsApp phone number (prepaid SIM is fine — never use a personal number)
- A Gmail account with an App Password for outgoing email

**Local development:** Windows 10 with WSL2 + Docker Desktop. All commands below run inside WSL2 (Ubuntu).

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/belpro.git
cd belpro
```

### 2. Create and configure the environment file

```bash
cp .env.example .env
```

Edit `.env` and fill in every value. Key ones to generate:

```bash
# EMSO encryption key (32 bytes, base64url)
python3 -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"

# API secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Evolution API key
python3 -c "import secrets; print(secrets.token_hex(24))"
```

Minimum required values in `.env`:

| Variable | Description |
|----------|-------------|
| `POSTGRES_PASSWORD` | Strong password for PostgreSQL |
| `DATABASE_URL` | Must match `POSTGRES_USER` / `POSTGRES_PASSWORD` |
| `EMSO_ENCRYPTION_KEY` | Generated above — keep safe, losing it makes EMŠO unreadable |
| `API_SECRET_KEY` | Generated above |
| `MANAGER_PASSWORD` | Initial dashboard login password |
| `N8N_BASIC_AUTH_USER` | n8n UI login username |
| `N8N_BASIC_AUTH_PASSWORD` | n8n UI login password |
| `N8N_WEBHOOK_URL` | `http://localhost:5678/` for local; public URL if remote |
| `EVOLUTION_API_KEY` | Generated above |
| `GMAIL_ADDRESS` | Dedicated NGO Gmail address |
| `GMAIL_APP_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) (not your account password) |

### 3. Start all services

```bash
docker compose up -d
```

First startup takes several minutes — Faster-Whisper downloads the model (~1.5 GB for `medium`).

Check that all services are healthy:

```bash
docker compose ps
```

All services should show `running` or `healthy`. If `whisper` takes longer, that is normal during the first model download.

### 4. Run database migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Log in to the dashboard

Open **http://localhost:80** in a browser.

- Username: `admin` (fixed)
- Password: the value of `MANAGER_PASSWORD` from your `.env`

After logging in, go to **Settings** to set the manager name, phone number, NGO name, and address. These appear on generated PDFs.

---

## WhatsApp setup

### 6. Link the WhatsApp number

Open the Evolution API manager at **http://localhost:8180**.

1. Log in with your `EVOLUTION_API_KEY`.
2. Create an instance named `belpro` (must match `EVOLUTION_INSTANCE_NAME` in `.env`).
3. Scan the QR code with the dedicated WhatsApp phone.

The instance status should change to `open` (connected). The phone must stay connected for the bot to receive messages.

### 7. Configure n8n workflows

Open n8n at **http://localhost:5678** and log in with `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD`.

1. Import the workflow files from `n8n/workflows/` (one per logical flow).
2. Set up credentials as documented in `n8n/credentials/README.md`.
3. Generate an n8n API key under **Settings → API**, and add it to `.env` as `N8N_API_KEY`.
4. Activate all workflows.

---

## Access points

| URL | What |
|-----|------|
| http://localhost:80 | Manager dashboard |
| http://localhost:8100/docs | FastAPI Swagger UI |
| http://localhost:5678 | n8n workflow editor |
| http://localhost:8180 | Evolution API (WhatsApp gateway) |

---

## Maintenance

### Backup

```bash
bash scripts/backup.sh
```

Backs up the PostgreSQL database and stored photos/PDFs.

### Restore

```bash
bash scripts/restore.sh <backup-file>
```

### Tail logs

```bash
docker compose logs -f
docker compose logs -f api
docker compose logs -f n8n
```

### Rebuild a service after code changes

```bash
docker compose up -d --build api
docker compose up -d --build whisper
```

### Reset a forgotten dashboard password

If you changed the password via the dashboard Settings page and forgot it:

```bash
docker compose exec postgres psql -U belpro -d belpro \
  -c "UPDATE managers SET password_hash = NULL;"
```

This clears the stored hash and falls back to `MANAGER_PASSWORD` in `.env` on next login.

---

## Security notes

- **EMŠO** (national ID number) is encrypted at rest using AES-256. Never log it, never expose it in API responses to the frontend.
- Photos are stored locally — never in cloud storage.
- The `EMSO_ENCRYPTION_KEY` must be backed up separately. Losing it makes all stored EMŠO values unreadable.
- Use a dedicated Gmail account and App Password, not a personal account.
- Never use a personal WhatsApp number — Evolution API takes over the session.
- `.env` is gitignored and must never be committed.

---

## Project layout

```
belpro/
├── docker-compose.yml
├── .env.example
├── n8n/workflows/          # n8n workflow JSON exports (committed)
├── whisper/                # Faster-Whisper HTTP wrapper
├── api/                    # FastAPI backend + PDF generation
├── frontend/               # Manager dashboard (HTML/CSS/JS)
├── nginx/                  # Reverse proxy config
├── scripts/                # setup.sh, backup.sh, restore.sh
└── db/                     # init.sql + Alembic migrations
```

Full system specification: [SPEC.md](SPEC.md)

---

## Out of scope (v1)

- Multi-tenant / SaaS mode
- Multiple managers per NGO
- Non-Slovenian language support
- Mobile native app
- Integration with IRSD / government systems
