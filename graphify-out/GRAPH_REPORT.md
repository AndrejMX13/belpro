# Graph Report - .  (2026-05-03)

## Corpus Check
- 38 files · ~15,024 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 341 nodes · 800 edges · 22 communities detected
- Extraction: 56% EXTRACTED · 44% INFERRED · 0% AMBIGUOUS · INFERRED: 356 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_System Architecture & Stack|System Architecture & Stack]]
- [[_COMMUNITY_Log Entry Data Layer|Log Entry Data Layer]]
- [[_COMMUNITY_Graphify Knowledge Graph|Graphify Knowledge Graph]]
- [[_COMMUNITY_Frontend Dashboard UI|Frontend Dashboard UI]]
- [[_COMMUNITY_Auth & Volunteer Core|Auth & Volunteer Core]]
- [[_COMMUNITY_Volunteer & Encryption Services|Volunteer & Encryption Services]]
- [[_COMMUNITY_Manager API & Schemas|Manager API & Schemas]]
- [[_COMMUNITY_Config & Migrations Setup|Config & Migrations Setup]]
- [[_COMMUNITY_Whisper Transcription Service|Whisper Transcription Service]]
- [[_COMMUNITY_ORM Model Registry|ORM Model Registry]]
- [[_COMMUNITY_API Entry Point|API Entry Point]]
- [[_COMMUNITY_Initial DB Migration|Initial DB Migration]]
- [[_COMMUNITY_Photo Schema Migration|Photo Schema Migration]]
- [[_COMMUNITY_Database Session Layer|Database Session Layer]]
- [[_COMMUNITY_EMSO Hash Migration|EMSO Hash Migration]]
- [[_COMMUNITY_Single-Tenant Rationale|Single-Tenant Rationale]]
- [[_COMMUNITY_Package Initializer|Package Initializer]]
- [[_COMMUNITY_Package Initializer|Package Initializer]]
- [[_COMMUNITY_Package Initializer|Package Initializer]]
- [[_COMMUNITY_Package Initializer|Package Initializer]]
- [[_COMMUNITY_Package Initializer|Package Initializer]]
- [[_COMMUNITY_Frontend API Client|Frontend API Client]]

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 54 edges
2. `Volunteer` - 38 edges
3. `GRAPH_REPORT.md Knowledge Graph Report` - 33 edges
4. `LogEntry` - 32 edges
5. `Manager` - 25 edges
6. `LogEntryPhoto` - 22 edges
7. `$()` - 22 edges
8. `Settings` - 21 edges
9. `Base` - 20 edges
10. `LogEntryListResponse` - 16 edges

## Surprising Connections (you probably didn't know these)
- `EntryStatus` --uses--> `Fields required to create a new log entry.`  [INFERRED]
  api\models\log_entry.py → api\schemas\log_entry.py
- `EntryStatus` --uses--> `Full log entry returned by the API.`  [INFERRED]
  api\models\log_entry.py → api\schemas\log_entry.py
- `EntryStatus` --uses--> `A single photo attached to a log entry.`  [INFERRED]
  api\models\log_entry.py → api\schemas\log_entry.py
- `EntryStatus` --uses--> `Editable fields — blocked once the entry is approved.`  [INFERRED]
  api\models\log_entry.py → api\schemas\log_entry.py
- `EntryStatus` --uses--> `Paginated log entry list.`  [INFERRED]
  api\models\log_entry.py → api\schemas\log_entry.py

## Communities

### Community 0 - "System Architecture & Stack"
Cohesion: 0.04
Nodes (60): AI Dialect Normalisation (Whisper + n8n), Approvals Page (Odobritve), asyncpg (Async PostgreSQL driver), cryptography (Python library, AES-256), CSD — Centre for Social Work, Dashboard Login Screen (single-manager auth), Deployment Requirement: Dedicated Gmail Account, Deployment Requirement: Dedicated WhatsApp Phone Number (+52 more)

### Community 1 - "Log Entry Data Layer"
Cohesion: 0.13
Nodes (49): Base, Base, Declarative base — import and subclass in every model., DeclarativeBase, SQLAlchemy ORM models — import all to ensure they register with Base.metadata., approve_log_entry(), create_log_entry(), delete_photo() (+41 more)

### Community 2 - "Graphify Knowledge Graph"
Cohesion: 0.06
Nodes (41): Graphify Section in CLAUDE.md, Community: API Entry Point 5 nodes cohesion 0.33, Community: Auth and Volunteer Management 43 nodes cohesion 0.14, Community: Config and Migrations Setup 14 nodes cohesion 0.15, Community: Database Session Layer 3 nodes cohesion 0.5, Community: EMSO Hash Migration 1 node cohesion 0.5, Community: Frontend API Client cohesion 1.0 thin, Community: Frontend Dashboard UI 37 nodes cohesion 0.16 (+33 more)

### Community 3 - "Frontend Dashboard UI"
Cohesion: 0.16
Nodes (37): $(), applyFilters(), approvalsSortTh(), checkManagerSetup(), closeModal(), esc(), fmtDatetime(), fmtHours() (+29 more)

### Community 4 - "Auth & Volunteer Core"
Cohesion: 0.22
Nodes (33): Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw, FastAPI dependency — rejects requests without the correct manager password., require_manager(), BaseSettings, EntryStatus, Manager, All configuration for the Belpro API service.      Values are read from the proc, Settings (+25 more)

### Community 5 - "Volunteer & Encryption Services"
Cohesion: 0.16
Nodes (20): decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError, Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag (+12 more)

### Community 6 - "Manager API & Schemas"
Cohesion: 0.2
Nodes (19): BaseModel, ManagerCreate, ManagerResponse, ManagerUpdate, PasswordChangeRequest, Fields required for first-time manager setup., Partial update — all fields optional.  Only provided fields are written., Payload for the change-password endpoint. (+11 more)

### Community 7 - "Config & Migrations Setup"
Cohesion: 0.15
Nodes (14): _do_run_migrations(), _get_url(), Alembic environment — async SQLAlchemy / asyncpg configuration., Read DATABASE_URL from settings (env / .env file)., Run migrations without a live DB connection (generates SQL script)., Inner helper called inside the async connection context., Create an async engine and run migrations inside it., Run migrations against a live database. (+6 more)

### Community 8 - "Whisper Transcription Service"
Cohesion: 0.18
Nodes (8): BaseHTTPRequestHandler, _Handler, Thin HTTP wrapper around Faster-Whisper for local speech-to-text.  Exposes a sin, Handle POST /transcribe requests., Transcribe the uploaded audio and return plain-text., Health check — GET /health returns 200 ok., Send a simple HTTP response., Route access logs to stdout.

### Community 9 - "ORM Model Registry"
Cohesion: 0.47
Nodes (2): SQLAlchemy declarative base shared by all ORM models., Pydantic schemas for the Manager entity.

### Community 10 - "API Entry Point"
Cohesion: 0.33
Nodes (5): health(), Belpro FastAPI application entry point., Fail fast if the database is unreachable on startup., Health check — returns ok when the service is up., verify_db_connection()

### Community 11 - "Initial DB Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch., upgrade()

### Community 12 - "Photo Schema Migration"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 13 - "Database Session Layer"
Cohesion: 0.5
Nodes (3): get_db(), Async SQLAlchemy engine and session factory., FastAPI dependency — yields one async DB session per request.

### Community 14 - "EMSO Hash Migration"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 15 - "Single-Tenant Rationale"
Cohesion: 1.0
Nodes (2): Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS, Single-Tenant Architecture (one NGO per deployment)

### Community 16 - "Package Initializer"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Package Initializer"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Package Initializer"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Package Initializer"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Package Initializer"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Frontend API Client"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **102 isolated node(s):** `Belpro FastAPI application entry point.`, `Fail fast if the database is unreachable on startup.`, `Health check — returns ok when the service is up.`, `Application settings — loaded from environment variables / .env file.`, `All configuration for the Belpro API service.      Values are read from the proc` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Single-Tenant Rationale`** (2 nodes): `Rationale: Single-tenant — out of scope for v1 to support multi-NGO SaaS`, `Single-Tenant Architecture (one NGO per deployment)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Initializer`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Initializer`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Initializer`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Initializer`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Initializer`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend API Client`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EntryStatus` connect `Auth & Volunteer Core` to `Log Entry Data Layer`, `ORM Model Registry`, `Manager API & Schemas`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `Settings` connect `Auth & Volunteer Core` to `Manager API & Schemas`, `Config & Migrations Setup`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Volunteer` connect `Log Entry Data Layer` to `ORM Model Registry`, `Auth & Volunteer Core`, `Volunteer & Encryption Services`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `EntryStatus` (e.g. with `Base` and `LogEntryPhoto`) actually correct?**
  _`EntryStatus` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Volunteer` (e.g. with `Base` and `EntryStatus`) actually correct?**
  _`Volunteer` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `LogEntry` (e.g. with `Base` and `LogEntryPhoto`) actually correct?**
  _`LogEntry` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Manager` (e.g. with `Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw` and `FastAPI dependency — rejects requests without the correct manager password.`) actually correct?**
  _`Manager` has 22 INFERRED edges - model-reasoned connections that need verification._