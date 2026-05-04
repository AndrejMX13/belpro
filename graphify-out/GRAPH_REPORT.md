# Graph Report - D:\Andrej\vsCode-workspace\BelPro  (2026-05-04)

## Corpus Check
- 42 files · ~74,270 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 467 nodes · 1185 edges · 35 communities detected
- Extraction: 53% EXTRACTED · 47% INFERRED · 0% AMBIGUOUS · INFERRED: 558 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
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

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 76 edges
2. `Volunteer` - 55 edges
3. `LogEntry` - 49 edges
4. `Manager` - 37 edges
5. `Settings` - 33 edges
6. `GRAPH_REPORT.md Knowledge Graph Report` - 33 edges
7. `$()` - 31 edges
8. `VolunteerResponse` - 26 edges
9. `EmsoCheckResponse` - 25 edges
10. `VolunteerDetailResponse` - 25 edges

## Surprising Connections (you probably didn't know these)
- `EntryStatus` --uses--> `Pydantic schemas for the Volunteer entity.`  [INFERRED]
  api\models\log_entry.py → api\schemas\volunteer.py
- `EntryStatus` --uses--> `Compact log entry view — used inside VolunteerDetailResponse.`  [INFERRED]
  api\models\log_entry.py → api\schemas\volunteer.py
- `EntryStatus` --uses--> `Plaintext EMŠO submitted for duplicate check before creating a volunteer.`  [INFERRED]
  api\models\log_entry.py → api\schemas\volunteer.py
- `EntryStatus` --uses--> `Result of an EMŠO duplicate check.`  [INFERRED]
  api\models\log_entry.py → api\schemas\volunteer.py
- `EntryStatus` --uses--> `Fields required to register a new volunteer.`  [INFERRED]
  api\models\log_entry.py → api\schemas\volunteer.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (57): Base, Base, SQLAlchemy declarative base shared by all ORM models., Declarative base — import and subclass in every model., DeclarativeBase, SQLAlchemy ORM models — import all to ensure they register with Base.metadata., approve_log_entry(), create_log_entry() (+49 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (57): BaseSettings, decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError (+49 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (53): _destroyCharts(), loadAnalytics(), renderAnalytics(), renderAnalyticsContent(), _renderCharts(), exportReportPdf(), fmtHours(), loadReports() (+45 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (42): AI Dialect Normalisation (Whisper + n8n), CSD — Centre for Social Work, Deployment Requirement: Dedicated Gmail Account, Deployment Requirement: Dedicated WhatsApp Phone Number, Docker Compose (Containerisation), EMŠO Encryption (AES-256 at rest), Entry Status Flow (pending_volunteer → pending_manager → approved/rejected), Evolution API (+34 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (41): Graphify Section in CLAUDE.md, Community: API Entry Point 5 nodes cohesion 0.33, Community: Auth and Volunteer Management 43 nodes cohesion 0.14, Community: Config and Migrations Setup 14 nodes cohesion 0.15, Community: Database Session Layer 3 nodes cohesion 0.5, Community: EMSO Hash Migration 1 node cohesion 0.5, Community: Frontend API Client cohesion 1.0 thin, Community: Frontend Dashboard UI 37 nodes cohesion 0.16 (+33 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (25): Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw, FastAPI dependency — rejects requests without the correct manager password., require_manager(), Manager, ManagerCreate, ManagerResponse, ManagerUpdate, PasswordChangeRequest (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (20): MonthlyReportSummary, _esc(), _fmt_date(), _generated_line(), PDF rendering for monthly volunteer reports using WeasyPrint., Render a single-volunteer monthly report PDF and return raw bytes., Render an all-volunteer summary PDF and return raw bytes., render_summary_pdf() (+12 more)

### Community 7 - "Community 7"
Cohesion: 0.27
Nodes (18): body(), border(), borders(), cell(), complianceTable(), componentTable(), coverPage(), featureTable() (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (16): analytics_summary(), AnalyticsSummary, HoursPerLocation, HoursPerVolunteer, MonthlyTrendPoint, _preceding_months(), Pydantic schemas for the analytics summary endpoint., Per-volunteer approved hours for a given month. (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (14): _do_run_migrations(), _get_url(), Alembic environment — async SQLAlchemy / asyncpg configuration., Read DATABASE_URL from settings (env / .env file)., Run migrations without a live DB connection (generates SQL script)., Inner helper called inside the async connection context., Create an async engine and run migrations inside it., Run migrations against a live database. (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (8): BaseHTTPRequestHandler, _Handler, Thin HTTP wrapper around Faster-Whisper for local speech-to-text.  Exposes a sin, Handle POST /transcribe requests., Transcribe the uploaded audio and return plain-text., Health check — GET /health returns 200 ok., Send a simple HTTP response., Route access logs to stdout.

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (5): health(), Belpro FastAPI application entry point., Fail fast if the database is unreachable on startup., Health check — returns ok when the service is up., verify_db_connection()

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch., upgrade()

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 18 - "Community 18"
Cohesion: 0.5
Nodes (3): get_db(), Async SQLAlchemy engine and session factory., FastAPI dependency — yields one async DB session per request.

### Community 19 - "Community 19"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (2): Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS, Single-Tenant Architecture (one NGO per deployment)

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Return a cached Settings instance (constructed once per process).

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Fail fast if the database is unreachable on startup.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Health check — returns ok when the service is up.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Rationale: Vanilla JS chosen — no framework overhead for NGO tool

## Knowledge Gaps
- **120 isolated node(s):** `Belpro FastAPI application entry point.`, `Fail fast if the database is unreachable on startup.`, `Health check — returns ok when the service is up.`, `Application settings — loaded from environment variables / .env file.`, `All configuration for the Belpro API service.      Values are read from the proc` (+115 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 20`** (2 nodes): `Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS`, `Single-Tenant Architecture (one NGO per deployment)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Return a cached Settings instance (constructed once per process).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Fail fast if the database is unreachable on startup.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Health check — returns ok when the service is up.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Rationale: Vanilla JS chosen — no framework overhead for NGO tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EntryStatus` connect `Community 0` to `Community 8`, `Community 1`, `Community 6`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Volunteer` connect `Community 0` to `Community 8`, `Community 1`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `Settings` connect `Community 1` to `Community 0`, `Community 9`, `Community 5`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 73 inferred relationships involving `EntryStatus` (e.g. with `Pydantic schemas for the analytics summary endpoint.` and `Return aggregated analytics data scoped to the given month.      Defaults to t`) actually correct?**
  _`EntryStatus` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `Volunteer` (e.g. with `Manager` and `Pydantic schemas for the Manager entity.`) actually correct?**
  _`Volunteer` has 52 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `LogEntry` (e.g. with `Volunteer` and `Registered volunteer.  Soft-deleted via active=False — never hard-deleted.`) actually correct?**
  _`LogEntry` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `Manager` (e.g. with `Base` and `Volunteer`) actually correct?**
  _`Manager` has 34 INFERRED edges - model-reasoned connections that need verification._