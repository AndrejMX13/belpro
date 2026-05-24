[Slovenščina](SPEC_SL.md)

# Belpro — System Specification
*Beleženje Prostovoljstva* — Digital Volunteer Diary for Slovenian NGOs

---

## 1. Project Overview

Belpro is a self-hosted, single-tenant, AI-assisted system that automates the *Dnevnik prostovoljskega dela* (Volunteer Work Diary) required by Slovenian law for recipients of the *Dodatek za delovno aktivnost* (Work Activity Allowance).

Each NGO runs its own independent Belpro instance. Volunteers interact exclusively via WhatsApp. The NGO manager uses a web dashboard. No SaaS, no shared infrastructure.

### Legal Context
- Governed by *Zakon o prostovoljstvu* and ZVOP-2/GDPR.
- Each volunteer must have a signed *Dogovor o prostovoljstvu* (Volunteer Agreement) with the NGO.
- Monthly proof of activity (*potrdilo*) must be submitted to the local CSD by end of month, or by the 8th of the following month at the latest.
- If a volunteer has a signed agreement, they are considered "work active" for 60–128 hours/month regardless of exact hours logged. The diary is an audit trail, not a strict hour counter.

---

## 2. Architecture Overview

![BelPro Architecture](docs/images/architecture.svg)

### Components

| Component | Technology | Role |
|-----------|-----------|------|
| Messaging interface | WhatsApp via Evolution API | Volunteer interaction |
| Workflow engine | n8n (self-hosted) | All business logic orchestration |
| Transcription | Faster-Whisper (CPU, local) | Voice note → text |
| Database | PostgreSQL (self-hosted) | All persistent data |
| Dashboard | FastAPI + HTML/JS/CSS (nginx) | Manager web UI |
| Email | Generic SMTP (n8n Send Email node) | Monthly PDFs, notifications |
| PDF generation | Python (WeasyPrint) | Monthly summary documents |
| Containerisation | Docker Compose | All services |
| Ops sidecar | Alpine/Python (Docker) | Automated backup, photo cleanup, error reporting |

**Design principle:** Use existing n8n nodes and standard services wherever possible. Custom code only where no node exists.

---

## 3. Data Model

### `volunteers`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| first_name | VARCHAR | Used in informal WhatsApp messages |
| last_name | VARCHAR | Used in formal documents and PDFs |
| street | VARCHAR | Street name and house number |
| postal_code | VARCHAR(4) | Slovenian 4-digit postal code |
| city | VARCHAR | |
| emso | TEXT | EMŠO — AES-256-GCM encrypted at rest (base64-encoded ciphertext) |
| emso_hash | VARCHAR(64) | HMAC-SHA256 of plaintext EMŠO — deterministic, used for uniqueness enforcement; nullable |
| phone | VARCHAR | WhatsApp number (international format, unique) |
| email | VARCHAR | For monthly PDF delivery |
| registered_at | TIMESTAMP | |
| active | BOOLEAN | Soft delete / deactivation |
| report_whatsapp | BOOLEAN | Send monthly PDF to volunteer via WhatsApp; default FALSE |
| report_email | BOOLEAN | Send monthly PDF to volunteer via email; default TRUE |
| manager_id | FK → managers | |

### `managers`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| first_name | VARCHAR | |
| last_name | VARCHAR | |
| phone | VARCHAR | WhatsApp number (unique) |
| email | VARCHAR | (unique) |
| ngo_name | VARCHAR | Name of the NGO |
| ngo_street | VARCHAR | Street name and house number |
| ngo_postal_code | VARCHAR(4) | Slovenian 4-digit postal code |
| ngo_city | VARCHAR | |
| ngo_davcna | VARCHAR(8) | Slovenian tax number (davčna številka); nullable |
| password_hash | TEXT | scrypt hash; nullable until first setup via UI |
| report_whatsapp | BOOLEAN | Manager receives consolidated report via WhatsApp; default FALSE |
| report_email | BOOLEAN | Manager receives consolidated report via email; default TRUE |
| default_report_whatsapp | BOOLEAN | Default WhatsApp flag applied to newly registered volunteers; default FALSE |
| default_report_email | BOOLEAN | Default email flag applied to newly registered volunteers; default TRUE |
| ngo_whatsapp_phone | VARCHAR(30) | Dedicated bot phone number linked to Evolution API; digits-only, no `+` prefix (nullable). Seeded from `NGO_WHATSAPP_PHONE` in `.env` on first boot; auto-synced from Evolution API when connected. |
| smtp_host | VARCHAR | SMTP server hostname, e.g. smtp.gmail.com (nullable, set via UI) |
| smtp_port | INTEGER | SMTP port, default 587 (nullable, set via UI) |
| smtp_user | VARCHAR | SMTP login / from-address (nullable, set via UI) |
| smtp_from_name | VARCHAR | Display name for outgoing emails (nullable, set via UI) |
| evolution_api_admin_url | VARCHAR | URL of Evolution API admin UI used for the settings link (nullable) |
| created_at | TIMESTAMP | |

### `log_entries`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| volunteer_id | FK → volunteers | |
| work_date | DATE | Date of the work, not submission |
| activity_description | TEXT | Cleaned/normalised text |
| raw_transcript | TEXT | Original Whisper output |
| hours | NUMERIC(4,1) | Extracted from transcript |
| location | VARCHAR | Extracted or inferred |
| status | ENUM | `pending_volunteer`, `pending_manager`, `approved`, `rejected` |
| volunteer_confirmed_at | TIMESTAMP | |
| manager_approved_at | TIMESTAMP | |
| manager_notified_at | TIMESTAMP | When manager was last notified; only one entry set at a time |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | Maintained by DB trigger `trg_entries_updated_at` |

Photos are stored in a separate `log_entry_photos` table (see below) — multiple photos per entry are supported.

### `log_entry_photos`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| log_entry_id | FK → log_entries | CASCADE DELETE |
| photo_path | VARCHAR(500) | Relative path to stored photo |
| photo_exif_timestamp | TIMESTAMP | Extracted from photo EXIF (nullable) |
| photo_exif_lat | NUMERIC(10,7) | GPS latitude from EXIF (nullable) |
| photo_exif_lon | NUMERIC(10,7) | GPS longitude from EXIF (nullable) |
| uploaded_at | TIMESTAMP | |

### `monthly_reports`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| volunteer_id | FK | nullable (NULL = consolidated manager report) |
| period_year | INT | |
| period_month | INT | |
| pdf_path | VARCHAR | |
| generated_at | TIMESTAMP | |
| sent_at | TIMESTAMP | nullable |

### `settings`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| name | TEXT | Setting key (unique, not null) |
| type | TEXT | Value type hint: `'int'`, `'bool'`, `'text'`, `'json'` |
| value | TEXT | Stored value (nullable — falls back to env default when absent) |

Seeded on first migration with the following rows (all runtime-tunable via the Administracija page):

| Name | Default | Description |
|------|---------|-------------|
| `max_photos_per_entry` | `5` | Maximum photos a volunteer may attach per entry |
| `photo_retention_days` | `730` | Days to keep stored photos before cleanup |
| `session_duration_hours` | `24` | Manager session cookie lifetime |
| `report_auto_day` | `28` | Day of month (1–28) the auto-report cron fires |
| `report_auto_period` | `current` | Report period: `current` or `previous` month |
| `report_auto_hour` | `7` | Hour (0–23) the auto-report cron fires |
| `backup_hour` | `2` | Hour (0–23) the nightly backup cron fires |
| `photo_cleanup_hour` | `3` | Hour (0–23) the nightly photo cleanup cron fires |
| `backup_retention_days` | `30` | Days to keep backup archives |

All values live in the DB (DB-first, env-fallback via `AppSettings` service). See `GET/PATCH /api/admin/settings`.

### `error_log`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | gen_random_uuid() |
| service | TEXT | Service name that recorded the error (e.g. `ops/backup`) |
| operation | TEXT | Operation within the service (e.g. `pg_dump`) |
| message | TEXT | Short human-readable error description |
| detail | TEXT | Optional additional context (nullable) |
| acknowledged | BOOLEAN | Default false; toggled by manager via dashboard |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() |

Written by internal services (ops sidecar scripts) via `POST /api/errors` authenticated with `X-Internal-Key: {API_SECRET_KEY}`. Unacknowledged error count shown as a nav badge on the Dnevnik napak page.

---

## 4. WhatsApp Flow (Volunteer)

### 4.1 Submitting an entry

```
Volunteer sends:
  - Voice note (required)         → Faster-Whisper transcribes
  - Photo (optional)              → EXIF extracted, stored
  - Text message (alternative)    → Used directly

n8n extracts from transcript:
  - activity_description
  - hours (look for "uro", "uri", "ure", "ur" etc.)
  - work_date (look for "danes", "včeraj", day names, explicit dates)
  - location (if mentioned)

n8n sends volunteer a confirmation message:
  ┌─────────────────────────────────────────┐
  │ Potrdite vnos:                          │
  │                                         │
  │ 📅 Datum: 12. 5. 2025                   │
  │ 🕐 Ure: 3                               │
  │ 📍 Kraj: Dom starejših Trnovo           │
  │ 📝 Aktivnost: Pomoč pri kosilu          │
  │                                         │
  │ [✅ Potrdi] [✏️ Popravi] [❌ Prekliči] │
  └─────────────────────────────────────────┘

If volunteer confirms → entry moves to `pending_manager`
If volunteer selects Popravi → bot asks them to re-send the entry as text.
  The volunteer may correct as many times as needed. No limit.
If volunteer selects Prekliči → entry is discarded, volunteer notified.

Manager receives WhatsApp notification:
  ┌─────────────────────────────────────────┐
  │ Nov vnos čaka na odobritev:             │
  │                                         │
  │ 👤 Ime Priimek                          │
  │ 📅 12. 5. 2025 — 3 ure                 │
  │ 📝 Pomoč pri kosilu, Dom starejših      │
  │                                         │
  │ [✅ Odobri]  [❌ Zavrni]               │
  └─────────────────────────────────────────┘

Manager approves → entry status `approved`, volunteer notified
Manager rejects  → entry status `rejected`, volunteer notified with
                   a note that manager will contact them via WhatsApp
```

### 4.2 Missing photo
- Photo is optional, not required.
- If photo is present, EXIF data (timestamp, GPS) is extracted and stored.
- Manager sees photo flag in approval notification.
- Manager decides whether to approve without photo.
- No automated re-prompting for missing photos.
- **WhatsApp EXIF stripping:** WhatsApp re-encodes images before delivery, removing all EXIF metadata. Photos sent via WhatsApp will have no GPS or timestamp in the DB. EXIF is preserved only when a photo is uploaded directly through the manager dashboard. The extraction and display code is in place; it activates automatically if data is present.

### 4.3 Sent-message visibility on linked phone

All messages the bot sends via Evolution API are sent *from* the instance's WhatsApp number and therefore appear in that number's chat history on any linked phone. This is WhatsApp protocol behavior — unavoidable when using a phone-linked API. The instance should use a dedicated phone number, not the manager's personal phone.

### 4.4 Volunteer language
- Slovenian only (all bot messages in Slovenian).
- Whisper configured for `sl` (Slovenian) language hint, with fallback to auto-detect.
- Transcript parsing (date, hours, location, activity) is handled by pattern matching in the n8n code node. No LLM normalisation step is implemented.

### 4.5 Whisper concurrency — design decision

The Whisper service runs as a single-threaded HTTP server (Python `HTTPServer`). Concurrent transcription requests serialise — one runs, the rest wait in the OS TCP accept queue. This is a deliberate trade-off:

- **Why single worker:** each worker loads its own model instance (~6 GB RAM for `large-v3`). Multiple workers multiply RAM linearly and risk OOM on typical VPS hardware — a harder failure mode than latency.
- **Acceptable for single-NGO use:** realistic burst load is 2–4 simultaneous voice notes at end of shift. Worst-case wait is a few minutes; the volunteer still receives a response.
- **If concurrency becomes a real problem:** the correct fix is a Redis-backed task queue with a single transcription worker, not `--workers N` on uvicorn. That enhancement is deferred to post-1.0 and will only be implemented if an actual deployment reports it as a problem.

---

## 5. Manager Dashboard (Web UI)

Served by nginx, backed by FastAPI. Mobile-friendly responsive design. Accessible from phone or desktop browser.

### Pages / Views

#### 5.1 Volunteers
- List of all volunteers (first name, last name, phone, email, active status, total hours this month)
- Filters: active / inactive / all, registration date range, city
- Sorting: by any column (name, hours, registration date)
- Add new volunteer form (first name, last name, street, postal code, city, EMŠO, phone, email, report channel checkboxes)
- Per-volunteer report channel toggles: WhatsApp and/or email (editable inline; defaults come from manager's global defaults)
- Per-volunteer inline editing of contact fields: first name + last name (one edit zone), phone, email — each with its own pencil toggle and Save/Cancel; EMŠO and registration date are read-only
- Deactivate volunteer (soft delete)
- View individual volunteer history

#### 5.2 Pending Approvals
- List of all entries with status `pending_manager`
- Each entry shows: volunteer name, date, hours, activity, location, photo thumbnail (if present)
- Approve / Reject buttons (triggers n8n webhook → WhatsApp notification to volunteer)

#### 5.3 Log / History
- Full searchable list of all entries (filterable by volunteer, month, status, location name)
- Location filter is a free-text search against the `location` field — useful for seeing all hours logged at a specific site across any date range
- Date range filter independent of calendar month
- Export filtered results to CSV

#### 5.4 Analytics
Served by `GET /api/analytics/summary` (auth: manager). Optional `year`/`month` query params; defaults to current calendar month. All counts and hour totals are scoped to the selected month.

- KPI tiles: total approved hours, active volunteer count, entries pending / approved / rejected, volunteers with no entries that month
- Hours per volunteer — horizontal bar chart; only volunteers with at least one entry (any status) in the selected month are shown
- Hours per location — vertical bar chart (approved entries only, non-empty location)
- Monthly trend — line chart covering the 6 calendar months ending at the selected month
- Year / month selector to navigate to any past period
- Print-friendly layout (`@media print` hides nav, filters, and export button)
- Export underlying data to CSV (BOM-prefixed for correct Excel UTF-8 rendering)

Charts rendered client-side with **Chart.js v4** (CDN, no build step).

#### 5.5 Reports
- Generate monthly PDF reports on demand (per volunteer or consolidated)
- View previously generated PDFs
- Trigger email send manually if needed
- **Arhiv poročil** — collapsible section listing all previously generated PDFs across all periods, with download links; toggled inline on the same page

#### 5.6 Settings
- Manager profile (first name, last name, phone, email, NGO name, NGO address)
- Password change
- Manager report channel: checkboxes controlling whether the manager receives the consolidated monthly report via WhatsApp and/or email
- Global volunteer report defaults: checkboxes that set the initial `report_whatsapp` / `report_email` values for newly registered volunteers
- SMTP configuration (host, port, user, from-name editable in UI; password stays in `.env`; works with Gmail, Yahoo, Proton, or any SMTP server)
- WhatsApp bot phone number — read-only when Evolution API is connected (number and state synced live from Evolution API on every settings page load; auto-written to DB and `.env` on change). Editable only when disconnected.
- Volunteer agreement template (text, used in PDF header) *(planned)*

#### 5.7 Administracija (System Administration)
Runtime-tunable operational settings. Changes take effect immediately without a container restart.

- **Največje število fotografij na vnos** (`max_photos_per_entry`) — maximum photos a volunteer may attach to a single entry; enforced at the API level on upload
- **Hranjenje fotografij (dni)** (`photo_retention_days`) — retention window for stored photos; used by the scheduled cleanup job
- **Trajanje seje (ure)** (`session_duration_hours`) — manager session cookie lifetime
- **Dan samodejnega pošiljanja poročil** (`report_auto_day`, 1–28) — day of month the auto-report cron fires
- **Obdobje poročila** (`report_auto_period`) — `current` (tekoči mesec) or `previous` (prejšnji mesec)
- **Ura samodejnega pošiljanja poročil** (`report_auto_hour`, 0–23) — hour the auto-report cron fires
- **Ura varnostnega kopiranja** (`backup_hour`, 0–23) — hour the nightly backup cron fires
- **Ura čiščenja fotografij** (`photo_cleanup_hour`, 0–23) — hour the nightly photo cleanup cron fires
- **Hranjenje varnostnih kopij (dni)** (`backup_retention_days`) — how long backup archives are kept; passed as CLI argument to `backup.sh`

All values are stored in the `settings` table via the `AppSettings` service and exposed through `GET/PATCH /api/admin/settings`. Changes take effect immediately: the API POSTs a `POST /reconfigure` to the ops notification server (port 9000), which regenerates the crontab and reloads crond — no container restart needed. The service falls back to env defaults when a DB row is absent.

The page also shows a **live system health widget** — a summary of all service states (PostgreSQL response time, Whisper, n8n, WhatsApp connection, disk free space, last heartbeat entry) refreshed every 30 seconds via `GET /api/health/detailed`. The `/api/health` endpoint remains separate (simple up/down, used by Docker healthcheck) and is never blocked by the detailed check.

#### 5.8 Dnevnik napak (App Log)

Operational error log — errors recorded by background services (ops sidecar backup, photo cleanup) and any other service using the `POST /api/errors` internal endpoint.

- Default view: unacknowledged errors only; toggled via checkbox to show all
- Per-row **Potrdi** button marks an error as acknowledged (`PATCH /api/errors/{id}/acknowledge`)
- Nav badge on the Dnevnik napak link shows the unacknowledged count; hidden when zero; refreshed every 60 seconds
- Errors written via `POST /api/errors` (internal key auth); read and acknowledged via `GET/PATCH /api/errors` (manager auth)

---

## 6. Monthly PDF Reports

### 6.1 Volunteer PDF (per person)
Generated for each volunteer. Intended to be printable and submitted to CSD.

Contents:
- NGO name, address, logo placeholder
- Volunteer name, address, EMŠO (last 3 digits masked in display copy)
- Month and year
- Table: Date | Activity | Hours | Location | Status
- Total hours
- Footer: Manager signature line, stamp placeholder, date

Format: A4, clean/minimal, Slovenian. Matches the structure of the CSD *potrdilo* as closely as possible so the volunteer needs only to sign.

### 6.2 Manager Consolidated PDF
One document for the manager covering all volunteers for the month.

Contents:
- Summary table: Volunteer | Total hours | Entries | Status
- Per-volunteer section with their entry details
- Generated timestamp

### 6.3 Delivery
- **Automated:** Cron job triggers on the 28th of each month. Generates all PDFs. Sends volunteer PDF to volunteer email (with consent). Sends consolidated PDF to manager email.
- **Manual:** Manager can trigger generation and download/send at any time from the dashboard.
- **Print:** PDFs available for download/print at NGO office.

---

## 7. Email

- n8n Send Email (SMTP) node used for all outgoing email.
- Works with **any** SMTP provider. The system is provider-agnostic — configuration lives in the Settings UI. Examples:
  - **Gmail:** smtp.gmail.com:587 with an [App Password](https://myaccount.google.com/apppasswords)
  - **Yahoo Mail:** smtp.mail.yahoo.com:587
  - **Proton Mail:** Proton Mail Bridge (local SMTP)
  - **Institutional / self-hosted:** any standards-compliant SMTP server
- SMTP host, port, login, and from-name are configured via the Settings UI and stored in the `managers` table. The password stays in `.env` as `SMTP_PASSWORD`.
- Emails sent: monthly PDF delivery, entry approval/rejection notifications (optional fallback if WhatsApp fails).

---

## 8. GDPR & Privacy

- EMŠO validated at entry using the mod-11 checksum algorithm (weights 7,6,5,4,3,2,7,6,5,4,3,2; remainder of 1 is rejected as no valid check digit exists). Invalid EMŠO is rejected at the API level before encryption or storage.
- EMŠO stored encrypted at rest (PostgreSQL column encryption or application-level AES-256).
- Photos stored locally on the server, not in cloud storage.
- Photo EXIF data (timestamp, GPS) retained as audit trail.
- Faces must not appear in photos (enforced by policy in volunteer agreement, not technically).
- Data retained as long as required by CSD/IRSD inspection requirements.
- No third-party data sharing except official audit.
- Volunteer consent for email delivery of monthly PDF captured in volunteer agreement.

---

## 9. Project Structure

```
belpro/
├── docker-compose.yml
├── .env.example
├── README.md
├── SPEC.md
├── CLAUDE.md
│
├── n8n/
│   ├── workflows/
│   │   ├── volunteer_entry.json       # Main WhatsApp → entry flow
│   │   ├── manager_approval.json      # Approval flow
│   │   └── monthly_reports.json       # Cron → PDF → email
│   └── credentials/                   # Gitignored, example provided

> **Canonical workflow source:** `n8n/workflows/` is the source of truth for all workflow definitions.
> On a fresh install, load them into n8n with `./scripts/n8n_workflows.py import`.
> After editing a workflow in the n8n UI, export with `./scripts/n8n_workflows.py export` and commit the result.
│
├── whisper/
│   ├── Dockerfile
│   └── transcribe.py                  # Thin HTTP wrapper around Faster-Whisper
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                        # FastAPI app entry point
│   ├── core/
│   │   ├── auth.py                    # HTTP Basic Auth dependency
│   │   └── settings.py                # Pydantic BaseSettings (env vars)
│   ├── routers/
│   │   ├── volunteers.py
│   │   ├── log_entries.py             # Entries + photo upload/EXIF inline
│   │   ├── managers.py                # Manager profile + password setup
│   │   ├── reports.py
│   │   ├── analytics.py               # Aggregated analytics summary endpoint
│   │   ├── admin.py                   # GET/PATCH /api/admin/settings
│   │   └── errors.py                  # POST /api/errors (internal key), GET/PATCH /api/errors (manager)
│   ├── models/                        # SQLAlchemy ORM models
│   │   ├── app_setting.py             # AppSetting ORM model (settings table)
│   │   └── error_log.py               # ErrorLog ORM model (error_log table)
│   ├── schemas/                       # Pydantic request/response schemas (analytics.py, volunteers.py, …)
│   ├── services/
│   │   ├── report_pdf.py              # WeasyPrint PDF generation
│   │   ├── encryption.py              # AES-256-GCM EMŠO encrypt/decrypt/hash
│   │   ├── password.py                # bcrypt password hashing
│   │   └── app_settings.py            # AppSettings: DB-first, env-fallback config authority
│   └── db/
│       └── migrations/                # Alembic migrations (versions/ subdir; current head: 013_error_log_table)
│
├── frontend/
│   ├── index.html                     # Single-page app (client-side routing)
│   ├── css/
│   │   └── main.css
│   └── js/
│       ├── api.js                     # Centralised fetch wrapper / API base URL
│       ├── volunteers.js              # Volunteers, approvals, log, settings views; client-side router
│       ├── reports.js                 # Reports view (includes Arhiv poročil archive section)
│       ├── analytics.js              # Analytics page (charts via Chart.js v4 CDN)
│       ├── admin.js                   # Administracija page (runtime settings + health widget)
│       └── errors.js                  # Health widget, Dnevnik napak page, nav badge
│
├── ops/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── entrypoint.sh
│   ├── crontab
│   └── scripts/
│       ├── backup.sh                  # DB + photo backup; reports failures via POST /api/errors
│       └── photo_cleanup.py           # Deletes photos past retention window; reports failures via POST /api/errors
│
├── nginx/
│   └── nginx.conf
│
├── scripts/
│   ├── setup.sh                       # Initial setup wizard
│   ├── backup.sh                      # DB + photo backup
│   ├── restore.sh
│   ├── list_pending_entries.py        # Print pending entries as JSON for n8n manual trigger
│   └── switch_manager_phone.ps1      # Toggle manager phone between real/dummy for testing
│
└── db/
    └── init.sql                       # Initial schema
```

---

## 10. Deployment

- Single Docker Compose stack.
- Target: any Linux host (local dev machine, VPS, on-premise server).
- **Local development:** Windows 10 with WSL2 + Docker Desktop. All `docker compose` commands and shell scripts run inside WSL2 (Ubuntu). Do not assume native Windows paths or tooling.
- Services: `postgres`, `n8n`, `whisper`, `api`, `frontend` (nginx), `evolution-api`, `ops`.
- The `ops` sidecar (Alpine/Python) runs three components: (1) a daily DB + photo backup, (2) a nightly photo cleanup job, and (3) `ops_server.py` — a lightweight HTTP server on port 9000 that receives `POST /reconfigure` from the API and regenerates the crontab (including backup hour, cleanup hour, report schedule, and retention period) without a container restart. All cron schedule settings are configurable from the Administracija page. Job failures are reported via `POST /api/errors` and appear in the Dnevnik napak dashboard page.
- All configuration via `.env` file.
- `setup.sh` guides initial configuration (manager credentials, Gmail, WhatsApp number linking).
- No Kubernetes, no cloud-specific dependencies.

---

## 11. Out of Scope (v1)

- Multi-tenant / SaaS mode
- Multiple managers per NGO
- Non-Slovenian language support
- Mobile native app
- Integration with IRSD / government systems
- Automatic face detection in photos
- Volunteer self-registration via WhatsApp

---

## 12. Testing Utilities

Two scripts in `scripts/` reduce the phone count needed for end-to-end testing from three to two (or one, with a dual-SIM phone).

**Without these scripts,** testing the full flow requires three WhatsApp numbers:
1. A dedicated phone running Evolution API (the bot) — always separate
2. A volunteer phone to send messages
3. A manager phone to receive approval notifications

**With these scripts,** the volunteer and manager roles can share a single phone (and SIM), cutting the requirement to two phones total. If your phone supports dual SIM, you can go down to one — the second SIM runs the bot, the first SIM handles both volunteer and manager roles.

### `load_env.ps1` / `load_env.sh`
Loads all variables from `.env` into the current shell session. Run once per session before using the other scripts.

PowerShell (Windows):
```
. .\scripts\load_env.ps1
```
Bash (Linux / WSL2):
```bash
source scripts/load_env.sh
```

### `switch_manager_phone.ps1` / `switch_manager_phone.sh`
Toggles the manager's phone number in the database between a real number and a dummy number.

PowerShell (Windows):
```
.\scripts\switch_manager_phone.ps1 volunteer   # set manager phone to dummy → your phone acts as volunteer
.\scripts\switch_manager_phone.ps1 manager     # set manager phone to real → your phone acts as manager
```
Bash (Linux / WSL2):
```bash
bash scripts/switch_manager_phone.sh volunteer
bash scripts/switch_manager_phone.sh manager
```

Uses environment variables `TEST_MANAGER_PHONE` (your real number) and `TEST_VOLUNTEER_PHONE` (a dummy placeholder), plus `MANAGER_PASSWORD` for API auth. See `.env.example` for configuration.

When the manager phone is set to the dummy number, the manager approval notification goes nowhere, and you can test the volunteer flow in isolation. When switched back, your phone receives manager notifications.

### `list_pending_entries.py`
Prints all `pending_manager` entries as JSON objects ready to paste into the n8n manual trigger node.

```
python scripts/list_pending_entries.py          # entries not yet notified
python scripts/list_pending_entries.py --all    # include already-notified entries
```

Requires `MANAGER_PASSWORD` in the environment. Reads from the FastAPI backend at `BELPRO_API_URL` (defaults to `http://localhost:8100/api`).

### Typical testing workflow

PowerShell (Windows):
```
# 0. Load environment variables (once per session):
. .\scripts\load_env.ps1
# 1. Volunteer sends a voice note via WhatsApp → n8n processes it
# 2. Volunteer confirms (Potrdi) → entry moves to pending_manager
# 3. Dump the pending entry:
python scripts/list_pending_entries.py
# 4. Copy the JSON output into the n8n manual trigger node
# 5. Execute the n8n manual trigger → manager approval message sends
# 6. Switch phone to manager mode to receive the notification:
.\scripts\switch_manager_phone.ps1 manager
# 7. Reply Approve/Odobri in WhatsApp → flow completes
# 8. Switch back for the next volunteer test:
.\scripts\switch_manager_phone.ps1 volunteer
```
Bash (Linux / WSL2):
```bash
# 0. Load environment variables (once per session):
source scripts/load_env.sh
# 1–5. same as above
# 6. Switch phone to manager mode:
bash scripts/switch_manager_phone.sh manager
# 7. Reply Odobri in WhatsApp → flow completes
# 8. Switch back:
bash scripts/switch_manager_phone.sh volunteer
```

### Manual trigger nodes in n8n

The testing workflow relies on two manual trigger nodes in the n8n workflows:

| Workflow | Node Name | What it does |
|----------|-----------|--------------|
| **BelPro — Vnos Prostovoljcev** | `Manual: Poslji Obvestilo Upravljalcu` | Sends the manager approval notification for pending entries |
| **BelPro — Odobritev Upravljalca** | `Manual Trigger` | Fires the manager approval flow (simulates manager replying to the notification) |

---

## 13. Automated Test Suite

A pytest-based regression safety net for the FastAPI backend. Scope: all API endpoints, happy path + key error cases. End-to-end n8n workflow tests live in Section 14.

### Infrastructure

- **Test database:** `belpro_test` — a second database on the existing `postgres` Docker container. Production `DATABASE_URL` is never touched.
- **Migration test database:** `belpro_test_migrations` — a third database used exclusively by the migration roundtrip test; created by `db/create_extra_dbs.sh` on first container start.
- **Configuration:** `api/.env.test` (gitignored) points pytest at `belpro_test` and supplies test-only secrets, including `DATABASE_URL_MIGRATIONS`.
- **Isolation:** Every test runs inside a SQLAlchemy SAVEPOINT. All writes are rolled back on teardown — no data leaks between tests.
- **No mocks, ever.** All tests hit a real PostgreSQL database.

### Running

```bash
docker compose exec api pytest tests/ -v
docker compose exec api pytest tests/ --cov=. --cov-report=term-missing -q
```

### Test files

| File | Coverage |
|------|----------|
| `tests/test_health.py` | `GET /api/health` |
| `tests/test_managers.py` | Manager profile, single-manager constraint, auth, password change |
| `tests/test_volunteers.py` | Full volunteers CRUD, deactivate/activate, EMŠO duplicate detection, EMŠO encrypted at rest |
| `tests/test_log_entries.py` | Full log entries CRUD, status machine (approve/reject/confirm), photo validation, 409 on invalid status transitions |
| `tests/test_reports.py` | Report generation, PDF content-type, 404 on unknown volunteer |
| `tests/test_analytics.py` | Summary shape, approved-only hour counts, 6-point monthly trend, rejected hours excluded |
| `tests/test_app_settings.py` | `settings` table seeding, `AppSettings` service unit tests, `GET/PATCH /api/admin/settings`, route-level enforcement (photo limit, session cookie), base64 photo upload |
| `tests/test_errors.py` | `POST /api/errors` (internal key auth), `GET /api/errors` with unacknowledged filter, `PATCH /api/errors/{id}/acknowledge`, unacknowledged count |
| `tests/test_migrations.py` | Alembic migration roundtrip: `stamp base` → `upgrade head` → `downgrade -1` → `upgrade head` on isolated DB |

### Backup/restore smoke test

`scripts/test_backup_restore.sh` — run manually, not part of the default pytest suite. Seeds known data, runs `backup.sh`, drops the `belpro` database, restores via `restore.sh`, and asserts the seeded records are present.

---

## 14. Workflow Integration Tests

A separate pytest suite that drives the `volunteer_entry` n8n workflow end-to-end. Unlike the API tests (which use in-process ASGITransport against a test DB), these tests run against the **full live Docker stack** — real n8n, real Evolution API, real PostgreSQL — by posting WhatsApp-shaped HTTP payloads to the n8n webhook and asserting DB state via the FastAPI API.

### Prerequisites

- `docker compose up -d` (full stack running)
- `volunteer_entry` workflow is **active** in n8n (not in test/listen mode)
- `MANAGER_PASSWORD` set in `.env`
- A real WhatsApp number reachable via the Evolution instance (test phone numbers used in payloads will receive real messages)

### Running

```powershell
# From the project root on the Windows host:
python -m pytest tests/workflow/ -v
```

### Test files

| File | Purpose |
|------|---------|
| `tests/workflow/conftest.py` | Session-scoped `api_client`/`n8n_client` (httpx); function-scoped `test_volunteer` fixture with direct-SQL teardown |
| `tests/workflow/helpers.py` | WhatsApp payload builders (`make_text_payload`, `make_response_payload`), `post_to_webhook`, polling utilities |
| `tests/workflow/test_volunteer_entry.py` | 6 integration scenarios (see below) |
| `tests/workflow/test_photo_upload.py` | Direct API tests for photo upload endpoint (bypasses n8n) |

### Scenarios

| Test | What it covers |
|------|---------------|
| `test_happy_path_text_confirm` | Volunteer sends text entry → confirms ("1") → entry reaches `pending_manager` |
| `test_edit_path` | Volunteer sends text → edits ("2") → sends corrected text → confirms → original entry deleted, corrected entry reaches `pending_manager` |
| `test_cancel_path` | Volunteer sends text → cancels ("4") → entry deleted from DB |
| `test_add_photos_then_confirm` | Volunteer chooses "Dodaj slike" ("3") → confirms ("1") — entry reaches `pending_manager` without a photo |
| `test_add_photos_then_cancel` | Volunteer chooses "Dodaj slike" ("3") → cancels ("4") from photo sub-menu — entry deleted |
| `test_unknown_volunteer_creates_no_entry` | Message from unregistered phone → no log entry created |

### Design notes

- **No mocking.** Evolution sends real WhatsApp messages; the DB is the real production database. Use a dedicated test phone number.
- **Polling, not fixed waits.** Each turn polls the FastAPI API until the expected DB state appears, with a 20 s timeout. A 2 s inter-turn sleep is applied between conversation turns to let n8n persist static-data state after creating the DB row (n8n writes state after the HTTP call returns).
- **Teardown via direct SQL.** `DELETE /api/volunteers/{id}` blocks if any log entries exist; `DELETE /api/log-entries/{id}` only accepts `pending_volunteer` entries. The fixture cleans up via `docker compose exec postgres psql` to bypass API restrictions.
- **Audio path not covered.** Whisper transcription tests require a real audio file and significant latency. Test separately when working on the transcription service.
