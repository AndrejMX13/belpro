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

```
Volunteer (WhatsApp)
        │
        ▼
Evolution API  ──────────────────────────────┐
        │                                    │
        ▼                                    │
  n8n Workflow ◄── Faster-Whisper (local)    │
        │                                    │
        ├──► PostgreSQL (self-hosted)         │
        │                                    │
        ├──► FastAPI + Web Dashboard ◄────────┘
        │
        └──► Gmail (SMTP/OAuth) for email delivery
```

### Components

| Component | Technology | Role |
|-----------|-----------|------|
| Messaging interface | WhatsApp via Evolution API | Volunteer interaction |
| Workflow engine | n8n (self-hosted) | All business logic orchestration |
| Transcription | Faster-Whisper (CPU, local) | Voice note → text |
| Database | PostgreSQL (self-hosted) | All persistent data |
| Dashboard | FastAPI + HTML/JS/CSS (nginx) | Manager web UI |
| Email | Gmail (n8n Gmail node) | Monthly PDFs, notifications |
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
| emso | VARCHAR(13) | EMŠO — encrypted at rest |
| phone | VARCHAR | WhatsApp number (international format) |
| email | VARCHAR | For monthly PDF delivery |
| registered_at | TIMESTAMP | |
| active | BOOLEAN | Soft delete / deactivation |
| manager_id | FK → managers | |

### `managers`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| name | VARCHAR | |
| phone | VARCHAR | WhatsApp number |
| email | VARCHAR | |
| ngo_name | VARCHAR | Name of the NGO |
| ngo_address | TEXT | |

### `log_entries`
| Field | Type | Notes |
|-------|------|-------|
| id | UUID PK | |
| volunteer_id | FK → volunteers | |
| entry_date | DATE | Date of the work, not submission |
| activity_description | TEXT | Cleaned/normalised text |
| raw_transcript | TEXT | Original Whisper output |
| hours | NUMERIC(4,1) | Extracted from transcript |
| location | VARCHAR | Extracted or inferred |
| status | ENUM | `pending_volunteer`, `pending_manager`, `approved`, `rejected` |
| photo_path | VARCHAR | Relative path to stored photo (nullable) |
| photo_exif_timestamp | TIMESTAMP | Extracted from photo EXIF (nullable) |
| photo_exif_location | POINT | GPS from EXIF (nullable) |
| volunteer_confirmed_at | TIMESTAMP | |
| manager_approved_at | TIMESTAMP | |
| created_at | TIMESTAMP | |

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
  - entry_date (look for "danes", "včeraj", day names, explicit dates)
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

### 4.3 Volunteer language
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
- Add new volunteer form (first name, last name, street, postal code, city, EMŠO, phone, email)
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
- Total hours logged this month (all volunteers)
- Hours per volunteer (bar chart)
- Monthly trend (line chart, last 6 months)
- Hours per location (bar chart) — useful for site-level reporting
- Number of active volunteers
- Entries pending / approved / rejected counts
- Export any chart/view to PDF (print-friendly layout)
- Export underlying data to CSV or XLSX

#### 5.5 Reports
- Generate monthly PDF reports on demand (per volunteer or consolidated)
- View previously generated PDFs
- Trigger email send manually if needed

#### 5.6 Settings
- Manager profile (name, phone, email, NGO name/address)
- Gmail SMTP configuration (or OAuth token setup)
- Volunteer agreement template (text, used in PDF header)

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

- n8n Gmail node used for all outgoing email.
- NGO configures Gmail account (or SMTP credentials) during setup.
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
│   ├── routers/
│   │   ├── volunteers.py
│   │   ├── entries.py
│   │   ├── reports.py
│   │   ├── analytics.py
│   │   └── settings.py
│   ├── models/                        # SQLAlchemy models
│   ├── schemas/                       # Pydantic schemas
│   ├── services/
│   │   ├── pdf_generator.py           # WeasyPrint PDF generation
│   │   └── exif_extractor.py          # Photo EXIF parsing
│   └── db/
│       └── migrations/                # Alembic migrations
│
├── frontend/
│   ├── index.html                     # Single-page app or simple MPA
│   ├── css/
│   ├── js/
│   └── templates/                     # Jinja2 or plain HTML templates
│
├── nginx/
│   └── nginx.conf
│
├── scripts/
│   ├── setup.sh                       # Initial setup wizard
│   ├── backup.sh                      # DB + photo backup
│   └── restore.sh
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
