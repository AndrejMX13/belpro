# Graph Report - .  (2026-05-07)

## Corpus Check
- 79 files · ~95,591 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 736 nodes · 1720 edges · 67 communities detected
- Extraction: 51% EXTRACTED · 49% INFERRED · 0% AMBIGUOUS · INFERRED: 838 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_API Data Models & Schemas|API Data Models & Schemas]]
- [[_COMMUNITY_Business Rules & Configuration|Business Rules & Configuration]]
- [[_COMMUNITY_Frontend Dashboard JS|Frontend Dashboard JS]]
- [[_COMMUNITY_System Architecture Diagrams|System Architecture Diagrams]]
- [[_COMMUNITY_Analytics Engine|Analytics Engine]]
- [[_COMMUNITY_BelPro Core Concepts|BelPro Core Concepts]]
- [[_COMMUNITY_Graphify Community Map|Graphify Community Map]]
- [[_COMMUNITY_Architecture Documentation|Architecture Documentation]]
- [[_COMMUNITY_API Request Handlers|API Request Handlers]]
- [[_COMMUNITY_PDF Report Generation|PDF Report Generation]]
- [[_COMMUNITY_Encryption & Volunteer CRUD|Encryption & Volunteer CRUD]]
- [[_COMMUNITY_Architecture DOCX Generator|Architecture DOCX Generator]]
- [[_COMMUNITY_Migration Config & Settings|Migration Config & Settings]]
- [[_COMMUNITY_Diagram Generator (EN)|Diagram Generator (EN)]]
- [[_COMMUNITY_Diagram Generator (SL)|Diagram Generator (SL)]]
- [[_COMMUNITY_ORM Database Models|ORM Database Models]]
- [[_COMMUNITY_Knowledge Graph Tools|Knowledge Graph Tools]]
- [[_COMMUNITY_API Entry Point|API Entry Point]]
- [[_COMMUNITY_Initial Schema Migration|Initial Schema Migration]]
- [[_COMMUNITY_Log Entry Photos Migration|Log Entry Photos Migration]]
- [[_COMMUNITY_Report Prefs Migration|Report Prefs Migration]]
- [[_COMMUNITY_WhatsApp & SMTP Migration|WhatsApp & SMTP Migration]]
- [[_COMMUNITY_NGO Davcna Migration|NGO Davcna Migration]]
- [[_COMMUNITY_API Authentication|API Authentication]]
- [[_COMMUNITY_Database Session|Database Session]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 109 edges
2. `Volunteer` - 73 edges
3. `LogEntry` - 67 edges
4. `Manager` - 57 edges
5. `LogEntryPhoto` - 35 edges
6. `Settings` - 33 edges
7. `GRAPH_REPORT.md Knowledge Graph Report` - 33 edges
8. `$()` - 31 edges
9. `LogEntryListResponse` - 29 edges
10. `LogEntryCreate` - 28 edges

## Surprising Connections (you probably didn't know these)
- `Docker Compose Orkestracija` --semantically_similar_to--> `Docker Compose Orchestration`  [INFERRED] [semantically similar]
  Belpro_Arhitektura_SL.pdf → Belpro_Architecture.pdf
- `FastAPI Zaledni API` --semantically_similar_to--> `FastAPI Backend API`  [INFERRED] [semantically similar]
  Belpro_Arhitektura_SL.pdf → Belpro_Architecture.pdf
- `n8n Delotokovni Pogon` --semantically_similar_to--> `n8n Workflow Engine`  [INFERRED] [semantically similar]
  Belpro_Arhitektura_SL.pdf → Belpro_Architecture.pdf
- `PostgreSQL Podatkovna Baza` --semantically_similar_to--> `PostgreSQL Database`  [INFERRED] [semantically similar]
  Belpro_Arhitektura_SL.pdf → Belpro_Architecture.pdf
- `Whisper Storitev Prepisovanja` --semantically_similar_to--> `Whisper Transcription Service`  [INFERRED] [semantically similar]
  Belpro_Arhitektura_SL.pdf → Belpro_Architecture.pdf

## Hyperedges (group relationships)
- **WhatsApp Voice Note → Whisper Transcription → n8n Workflow → PostgreSQL Entry Flow** — belpro_whatsapp_interface, belpro_faster_whisper, belpro_n8n_workflow, belpro_postgresql, belpro_voice_note_flow [EXTRACTED 0.95]
- **GDPR/ZVOP-2 Compliance: EMŠO Encryption + Photo EXIF Audit + Data Retention** — belpro_gdpr_zvop2, belpro_emso_encryption, belpro_cryptography_lib, belpro_photo_evidence [INFERRED 0.85]
- **Entry Status Lifecycle States** — claudemd_entry_status_flow, specmd_log_entries_table, specmd_confirmation_dialog, specmd_manager_approval_flow [EXTRACTED 1.00]
- **Core Data Model Tables** — specmd_volunteers_table, specmd_managers_table, specmd_log_entries_table, specmd_log_entry_photos_table, specmd_monthly_reports_table [EXTRACTED 1.00]
- **Manager Dashboard Views** — specmd_dashboard, specmd_analytics_page, frontend_login_screen, frontend_sidebar_nav, frontend_modal_component, frontend_chartjs_cdn, frontend_js_modules [EXTRACTED 0.95]
- **WhatsApp Message Processing Pipeline (Evolution API -> n8n Webhook -> Phone Lookup -> Volunteer Match)** — Evolution_API_and_N8N_phone_identification_solutions_whatsapp_message_flow, Evolution_API_and_N8N_phone_identification_solutions_evolution_phone_extraction, Evolution_API_and_N8N_phone_identification_solutions_n8n_webhook_trigger, Evolution_API_and_N8N_phone_identification_solutions_n8n_database_lookup, Evolution_API_and_N8N_phone_identification_solutions_volunteer_phone_matching [EXTRACTED 1.00]
- **Docker Compose Service Stack (Nginx, Frontend, FastAPI, n8n, PostgreSQL, Whisper, Evolution API)** — Belpro_Architecture_docker_compose_orchestration, Belpro_Architecture_nginx_reverse_proxy, Belpro_Architecture_frontend_dashboard, Belpro_Architecture_fastapi_backend, Belpro_Architecture_n8n_workflow_engine, Belpro_Architecture_postgresql_database, Belpro_Architecture_whisper_transcription_service, Belpro_Architecture_evolution_api_whatsapp [EXTRACTED 1.00]
- **Volunteer Entry Flow Triad (WhatsApp Ingestion, Voice Transcription, n8n Orchestration)** — Belpro_Architecture_volunteer_entry_flow, Belpro_Architecture_evolution_api_whatsapp, Belpro_Architecture_whisper_transcription_service, Belpro_Architecture_n8n_workflow_engine [EXTRACTED 1.00]
- **BelPro System Architecture — Five Row-1 Components Connected via Data Flow** — arch_volunteer_whatsapp, arch_evolution_api, arch_n8n_engine, arch_dashboard, arch_manager [EXTRACTED 1.00]
- **Five-Step Volunteer Entry Workflow — Record to Confirmation** — wf_record, wf_ai_clean, wf_confirm, wf_manager_approve, wf_done [EXTRACTED 1.00]
- **Monthly Reporting Cycle — Cron Trigger to CSD Submission** — rpt_cron_trigger, rpt_pdf_generation, rpt_email_delivery, rpt_csd_submission [EXTRACTED 1.00]

## Communities

### Community 0 - "API Data Models & Schemas"
Cohesion: 0.09
Nodes (113): Base, Base, Declarative base — import and subclass in every model., BaseSettings, DeclarativeBase, Raised when the manager has not configured SMTP., SmtpNotConfiguredError, SQLAlchemy ORM models — import all to ensure they register with Base.metadata. (+105 more)

### Community 1 - "Business Rules & Configuration"
Cohesion: 0.03
Nodes (75): Python Dependencies — FastAPI, SQLAlchemy, asyncpg, Alembic, Pydantic, WeasyPrint, cryptography, etc., ASCII Check Results — non-ASCII chars found: Naloži Stanje, Briši Popravi, Feature Addition Checklist — SPEC.md → Alembic → Pydantic → n8n JSON → update SPEC.md, Address Fields Structured — street, postal_code (4-digit), city, ASCII-only Identifiers Rule — Slovenian characters forbidden in code identifiers, BelPro — Beleženje Prostovoljstva (self-hosted volunteer diary system), EMŠO Encryption — AES-256 at rest, never logged, Entry Status Flow — one-way: pending_volunteer → pending_manager → approved or rejected (+67 more)

### Community 2 - "Frontend Dashboard JS"
Cohesion: 0.11
Nodes (53): _destroyCharts(), loadAnalytics(), renderAnalytics(), renderAnalyticsContent(), _renderCharts(), exportReportPdf(), fmtHours(), loadReports() (+45 more)

### Community 3 - "System Architecture Diagrams"
Cohesion: 0.12
Nodes (44): Dashboard — Web UI and FastAPI Backend, Nadzorna plošča — Spl. vmesnik + API, Evolution API — WhatsApp Gateway, Evolution API — API Prehod, Gmail — Email Delivery via SMTP, Gmail — Pošiljanje e-pošte, Manager — Browser or Phone Access, Vodja — Brskalnik / Telefon (+36 more)

### Community 4 - "Analytics Engine"
Cohesion: 0.1
Nodes (37): analytics_summary(), AnalyticsSummary, HoursPerLocation, HoursPerVolunteer, MonthlyTrendPoint, _preceding_months(), Pydantic schemas for the analytics summary endpoint., Per-volunteer approved hours for a given month. (+29 more)

### Community 5 - "BelPro Core Concepts"
Cohesion: 0.06
Nodes (42): AI Dialect Normalisation (Whisper + n8n), CSD — Centre for Social Work, Deployment Requirement: Dedicated Gmail Account, Deployment Requirement: Dedicated WhatsApp Phone Number, Docker Compose (Containerisation), EMŠO Encryption (AES-256 at rest), Entry Status Flow (pending_volunteer → pending_manager → approved/rejected), Evolution API (+34 more)

### Community 6 - "Graphify Community Map"
Cohesion: 0.06
Nodes (41): Graphify Section in CLAUDE.md, Community: API Entry Point 5 nodes cohesion 0.33, Community: Auth and Volunteer Management 43 nodes cohesion 0.14, Community: Config and Migrations Setup 14 nodes cohesion 0.15, Community: Database Session Layer 3 nodes cohesion 0.5, Community: EMSO Hash Migration 1 node cohesion 0.5, Community: Frontend API Client cohesion 1.0 thin, Community: Frontend Dashboard UI 37 nodes cohesion 0.16 (+33 more)

### Community 7 - "Architecture Documentation"
Cohesion: 0.07
Nodes (40): BelPro System Architecture, Docker Compose Orchestration, EMSO Encryption at Rest (AES-256), Evolution API WhatsApp Gateway, External Gmail Service, External WhatsApp Service, FastAPI Backend API, Frontend Manager Dashboard (+32 more)

### Community 8 - "API Request Handlers"
Cohesion: 0.07
Nodes (26): BaseHTTPRequestHandler, Async email sender backed by aiosmtplib.  Reads SMTP config from the Manager row, Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port, send_email(), Exception, approve_log_entry(), confirm_log_entry(), create_log_entry() (+18 more)

### Community 9 - "PDF Report Generation"
Cohesion: 0.13
Nodes (29): MonthlyReportSummary, _esc(), _fmt_date(), _generated_line(), _ngo_header_html(), NGOInfo, PDF rendering for monthly volunteer reports using WeasyPrint., Render an all-volunteer summary PDF and return raw bytes. (+21 more)

### Community 10 - "Encryption & Volunteer CRUD"
Cohesion: 0.16
Nodes (21): decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError, Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag (+13 more)

### Community 11 - "Architecture DOCX Generator"
Cohesion: 0.27
Nodes (18): body(), border(), borders(), cell(), complianceTable(), componentTable(), coverPage(), featureTable() (+10 more)

### Community 12 - "Migration Config & Settings"
Cohesion: 0.15
Nodes (14): _do_run_migrations(), _get_url(), Alembic environment — async SQLAlchemy / asyncpg configuration., Read DATABASE_URL from settings (env / .env file)., Run migrations without a live DB connection (generates SQL script)., Inner helper called inside the async connection context., Create an async engine and run migrations inside it., Run migrations against a live database. (+6 more)

### Community 13 - "Diagram Generator (EN)"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 14 - "Diagram Generator (SL)"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 15 - "ORM Database Models"
Cohesion: 0.39
Nodes (3): SQLAlchemy declarative base shared by all ORM models., LogEntryPhoto ORM model — one row per photo, many per log entry., MonthlyReport ORM model — tracks generated PDF reports.

### Community 16 - "Knowledge Graph Tools"
Cohesion: 0.33
Nodes (7): Glob/Grep Restriction — forbidden for initial codebase discovery, Graphify Primary Discovery Rule — use Graphify index before glob/grep, Graphify Update Maintenance — run graphify update . after code changes, Serena Semantic Symbol Navigation — precise symbol-level execution, 770 Inferred Edges — avg confidence 0.53, need verification, Graphify Knowledge Graph Report — 562 nodes, 1449 edges, 56 communities, AI-Assisted Development — Claude Code, Serena, Graphify used throughout

### Community 17 - "API Entry Point"
Cohesion: 0.33
Nodes (5): health(), Belpro FastAPI application entry point., Fail fast if the database is unreachable on startup., Health check — returns ok when the service is up., verify_db_connection()

### Community 18 - "Initial Schema Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch., upgrade()

### Community 19 - "Log Entry Photos Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 20 - "Report Prefs Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 21 - "WhatsApp & SMTP Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 22 - "NGO Davcna Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Add ngo_davcna column to managers.  Revision ID: 007 Revises: 006 Create Date: 2, Add ngo_davcna column to managers., Drop ngo_davcna column from managers., upgrade()

### Community 23 - "API Authentication"
Cohesion: 0.5
Nodes (3): Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw, FastAPI dependency — rejects requests without the correct manager password., require_manager()

### Community 24 - "Database Session"
Cohesion: 0.5
Nodes (3): get_db(), Async SQLAlchemy engine and session factory., FastAPI dependency — yields one async DB session per request.

### Community 25 - "Community 25"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 26 - "Community 26"
Cohesion: 0.67
Nodes (1): Rename non-ASCII node names to ASCII and fix all references.

### Community 27 - "Community 27"
Cohesion: 0.67
Nodes (1): Patch volunteer_entry workflow: thread remoteJid + fix location regex.

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (1): Patch v2: @lid real-phone extraction + name-based volunteer fallback lookup.

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (1): Patch v3: LID→real JID via findContacts, Slovenian word-hours parsing.

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (1): Patch v4: Use remoteJidAlt from v2.3.7 webhook; remove unreliable findContacts l

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (1): Patch v5: Remove pushName and name-based fallback — phone-only lookup is reliabl

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Deploy ASCII-renamed workflow to n8n.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Deploy fixed workflow to n8n instance.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Deploy popravi-fixed workflow to n8n.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Export volunteer_entry workflow from n8n to JSON file.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Fix Code: Clear State Popravi and Preklici to read from Nalozi Stanje instead of

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Fix Popravi flow: show transcript for editing instead of just discarding.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (2): Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS, Single-Tenant Architecture (one NGO per deployment)

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (2): No Skip Alembic Migrations — all schema changes via migrations, Project Directory Layout — docker-compose.yml, n8n/, whisper/, api/, frontend/, nginx/, scripts/, db/

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (2): Dashboard QR Modal Bug — base64 image received but not rendered (issue #1602), Related GitHub Issues — #1602, #2068, #2380

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (2): POST /test/inject-entry — injects pending_manager entry and fires n8n webhook, Two-Phase Testing Strategy — Phase 1: volunteer flow via dashboard; Phase 2: manager WhatsApp

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Partial update — all fields optional.  Only provided fields are written.

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Render a single-volunteer monthly report PDF and return raw bytes.

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Render an all-volunteer summary PDF and return raw bytes.

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Handle POST /transcribe requests.

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (1): Health check — GET /health returns 200 ok.

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (1): Send a simple HTTP response.

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (1): Route access logs to stdout.

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (1): Return a cached Settings instance (constructed once per process).

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (1): Fail fast if the database is unreachable on startup.

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Health check — returns ok when the service is up.

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (1): Rationale: Vanilla JS chosen — no framework overhead for NGO tool

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): CLAUDE.md references SPEC.md for full project details

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Maintenance Scripts — backup.sh, restore.sh, log tailing

## Knowledge Gaps
- **226 isolated node(s):** `Belpro FastAPI application entry point.`, `Fail fast if the database is unreachable on startup.`, `Health check — returns ok when the service is up.`, `Application settings — loaded from environment variables / .env file.`, `All configuration for the Belpro API service.      Values are read from the proc` (+221 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 32`** (2 nodes): `deploy_ascii_rename.py`, `Deploy ASCII-renamed workflow to n8n.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (2 nodes): `deploy_fix_clear_state.py`, `Deploy fixed workflow to n8n instance.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (2 nodes): `deploy_popravi_fix.py`, `Deploy popravi-fixed workflow to n8n.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (2 nodes): `export_workflow.py`, `Export volunteer_entry workflow from n8n to JSON file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `fix_clear_state.py`, `Fix Code: Clear State Popravi and Preklici to read from Nalozi Stanje instead of`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `fix_popravi_flow.py`, `Fix Popravi flow: show transcript for editing instead of just discarding.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS`, `Single-Tenant Architecture (one NGO per deployment)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (2 nodes): `No Skip Alembic Migrations — all schema changes via migrations`, `Project Directory Layout — docker-compose.yml, n8n/, whisper/, api/, frontend/, nginx/, scripts/, db/`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (2 nodes): `Dashboard QR Modal Bug — base64 image received but not rendered (issue #1602)`, `Related GitHub Issues — #1602, #2068, #2380`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (2 nodes): `POST /test/inject-entry — injects pending_manager entry and fires n8n webhook`, `Two-Phase Testing Strategy — Phase 1: volunteer flow via dashboard; Phase 2: manager WhatsApp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Partial update — all fields optional.  Only provided fields are written.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Render a single-volunteer monthly report PDF and return raw bytes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Render an all-volunteer summary PDF and return raw bytes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Handle POST /transcribe requests.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `Health check — GET /health returns 200 ok.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Send a simple HTTP response.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Route access logs to stdout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `Return a cached Settings instance (constructed once per process).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `Fail fast if the database is unreachable on startup.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Health check — returns ok when the service is up.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `Rationale: Vanilla JS chosen — no framework overhead for NGO tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `CLAUDE.md references SPEC.md for full project details`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Maintenance Scripts — backup.sh, restore.sh, log tailing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EntryStatus` connect `API Data Models & Schemas` to `API Request Handlers`, `PDF Report Generation`, `Analytics Engine`, `ORM Database Models`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Volunteer` connect `API Data Models & Schemas` to `PDF Report Generation`, `Encryption & Volunteer CRUD`, `Analytics Engine`, `ORM Database Models`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `Manager` connect `API Data Models & Schemas` to `PDF Report Generation`, `Analytics Engine`, `API Authentication`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 106 inferred relationships involving `EntryStatus` (e.g. with `Base` and `Pydantic schemas for the analytics summary endpoint.`) actually correct?**
  _`EntryStatus` has 106 INFERRED edges - model-reasoned connections that need verification._
- **Are the 70 inferred relationships involving `Volunteer` (e.g. with `Base` and `EntryStatus`) actually correct?**
  _`Volunteer` has 70 INFERRED edges - model-reasoned connections that need verification._
- **Are the 64 inferred relationships involving `LogEntry` (e.g. with `Base` and `Volunteer`) actually correct?**
  _`LogEntry` has 64 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `Manager` (e.g. with `Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw` and `FastAPI dependency — rejects requests without the correct manager password.`) actually correct?**
  _`Manager` has 54 INFERRED edges - model-reasoned connections that need verification._