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
| PDF generation | Python (WeasyPrint or ReportLab) | Monthly summary documents |
| Containerisation | Docker Compose | All services |

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
| ngo_whatsapp_phone | VARCHAR(30) | Dedicated bot phone number linked to Evolution API (nullable) |
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

### 4.3 Sent-message visibility on linked phone

All messages the bot sends via Evolution API are sent *from* the instance's WhatsApp number and therefore appear in that number's chat history on any linked phone. This is WhatsApp protocol behavior — unavoidable when using a phone-linked API. The instance should use a dedicated phone number, not the manager's personal phone.

### 4.4 Volunteer language
- Slovenian only (all bot messages in Slovenian).
- Whisper configured for `sl` (Slovenian) language hint, with fallback to auto-detect.
- Dialect normalisation handled by the n8n AI node (Claude / OpenAI call) that cleans the transcript.

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

#### 5.6 Settings
- Manager profile (first name, last name, phone, email, NGO name, NGO address)
- Password change
- Manager report channel: checkboxes controlling whether the manager receives the consolidated monthly report via WhatsApp and/or email
- Global volunteer report defaults: checkboxes that set the initial `report_whatsapp` / `report_email` values for newly registered volunteers
- SMTP configuration (host, port, user, from-name editable in UI; password stays in `.env`; works with Gmail, Yahoo, Proton, or any SMTP server)
- Volunteer agreement template (text, used in PDF header) *(planned)*

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
│   │   └── analytics.py               # Aggregated analytics summary endpoint
│   ├── models/                        # SQLAlchemy ORM models
│   ├── schemas/                       # Pydantic request/response schemas (analytics.py, volunteers.py, …)
│   ├── services/
│   │   ├── report_pdf.py              # WeasyPrint PDF generation
│   │   ├── encryption.py              # AES-256-GCM EMŠO encrypt/decrypt/hash
│   │   └── password.py                # bcrypt password hashing
│   └── db/
│       └── migrations/                # Alembic migrations (versions/ subdir; current head: 006_whatsapp_and_smtp_config)
│
├── frontend/
│   ├── index.html                     # Single-page app (client-side routing)
│   ├── css/
│   │   └── main.css
│   └── js/
│       ├── api.js                     # Centralised fetch wrapper / API base URL
│       ├── volunteers.js              # Volunteers, approvals, log, settings views; client-side router
│       ├── reports.js                 # Reports view
│       └── analytics.js              # Analytics page (charts via Chart.js v4 CDN)
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
- Services: `postgres`, `n8n`, `whisper`, `api`, `frontend` (nginx), `evolution-api`.
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

### `load_env.ps1`
Loads all variables from `.env` into the current PowerShell session. Run once per session before using the other scripts.

```
. .\scripts\load_env.ps1
```

### `switch_manager_phone.ps1`
Toggles the manager's phone number in the database between a real number and a dummy number.

```
.\scripts\switch_manager_phone.ps1 volunteer   # set manager phone to dummy → your phone acts as volunteer
.\scripts\switch_manager_phone.ps1 manager     # set manager phone to real → your phone acts as manager
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
# 7. Reply Approve/Odori in WhatsApp → flow completes
# 8. Switch back for the next volunteer test:
.\scripts\switch_manager_phone.ps1 volunteer
```

### Manual trigger nodes in n8n

The testing workflow relies on two manual trigger nodes in the n8n workflows:

| Workflow | Node Name | What it does |
|----------|-----------|--------------|
| **BelPro — Vnos Prostovoljcev** | `Manual: Poslji Obvestilo Upravljalcu` | Sends the manager approval notification for pending entries |
| **BelPro — Odobritev Upravljalca** | `Manual Trigger` | Fires the manager approval flow (simulates manager replying to the notification) |

---

## 13. Automated Test Suite

A pytest-based regression safety net for the FastAPI backend. Scope: all API endpoints, happy path + key error cases. n8n workflow tests are excluded (structural changes pending).

### Infrastructure

- **Test database:** `belpro_test` — a second database on the existing `postgres` Docker container, reachable at `localhost:5432` from WSL2. Production `DATABASE_URL` is never touched.
- **Configuration:** `api/.env.test` (gitignored) points pytest at `belpro_test` and supplies test-only secrets.
- **Isolation:** Every test runs inside a SQLAlchemy SAVEPOINT. All writes are rolled back on teardown — no data leaks between tests.
- **No mocks, ever.** All tests hit a real PostgreSQL database.

### Running

```bash
# From the api/ directory on the WSL2 host (not inside the container):
cd api
python -m pytest tests/ -v
```

Requires the `postgres` Docker container to be running and `belpro_test` to exist (created automatically on first run by the session-scoped engine fixture).

### Test files

| File | Coverage |
|------|----------|
| `tests/test_health.py` | `GET /api/health` |
| `tests/test_managers.py` | Manager profile, single-manager constraint, auth |
| `tests/test_volunteers.py` | Full volunteers CRUD, deactivate/activate, EMŠO duplicate detection |
| `tests/test_log_entries.py` | Full log entries CRUD, status machine (approve/reject/confirm), photo validation |
| `tests/test_reports.py` | Report generation, PDF content-type, 404 on unknown volunteer |
| `tests/test_analytics.py` | Summary shape, approved-only hour counts, 6-point monthly trend |

### Backup/restore smoke test

`scripts/test_backup_restore.sh` — run manually, not part of the default pytest suite. Seeds known data, runs `backup.sh`, drops the `belpro` database, restores via `restore.sh`, and asserts the seeded records are present.
