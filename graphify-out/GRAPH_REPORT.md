# Graph Report - D:\Andrej\vsCode-workspace\BelPro  (2026-05-15)

## Corpus Check
- 74 files · ~180,713 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 621 nodes · 1563 edges · 46 communities detected
- Extraction: 47% EXTRACTED · 53% INFERRED · 0% AMBIGUOUS · INFERRED: 821 edges (avg confidence: 0.58)
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

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 92 edges
2. `LogEntry` - 61 edges
3. `Manager` - 56 edges
4. `Volunteer` - 52 edges
5. `LogEntryListResponse` - 34 edges
6. `LogEntryCreate` - 33 edges
7. `LogEntryResponse` - 33 edges
8. `PhotoResponse` - 33 edges
9. `PhotoBase64Request` - 33 edges
10. `LogEntryUpdate` - 33 edges

## Surprising Connections (you probably didn't know these)
- `EntryStatus` --uses--> `Pydantic schemas for the Volunteer entity.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py
- `EntryStatus` --uses--> `Strip whitespace and leading ``+``, return bare E.164 digits.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py
- `EntryStatus` --uses--> `Compact log entry view — used inside VolunteerDetailResponse.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py
- `EntryStatus` --uses--> `Plaintext EMŠO submitted for duplicate check before creating a volunteer.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py
- `EntryStatus` --uses--> `Result of an EMŠO duplicate check.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\schemas\volunteer.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (78): Base, Base, Declarative base — import and subclass in every model., AsyncClient with get_db dependency wired to the test session., HTTP Basic Auth header for the seeded manager., Returns an async callable that inserts a LogEntry row via flush., Run Alembic migrations against belpro_test, seed one Manager row.     Drops all, Per-test session inside a SAVEPOINT.  The app's commit() releases the     savepo (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (39): auth(), client(), db_session(), engine(), log_entry_factory(), Returns an async callable that inserts a Volunteer row via flush (not commit), volunteer_factory(), get_settings() (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (64): BaseSettings, decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError (+56 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (54): _destroyCharts(), loadAnalytics(), renderAnalytics(), renderAnalyticsContent(), _renderCharts(), exportReportPdf(), fmtHours(), loadReports() (+46 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (34): BaseModel, Update or append KEY=value in a .env file. Returns True on success, False on fai, write_env_key(), EvolutionClient, Async HTTP client for the Evolution API WhatsApp gateway., ConfigInfoResponse, ManagerCreate, ManagerResponse (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (31): Async email sender backed by aiosmtplib.  Reads SMTP config from the Manager row, Raised when the manager has not configured SMTP., Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port, send_email(), SmtpNotConfiguredError, MonthlyReportSummary, _esc(), _fmt_date() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (34): Dashboard — Web UI and FastAPI Backend, Nadzorna plošča — Spl. vmesnik + API, Evolution API — WhatsApp Gateway, Evolution API — API Prehod, Gmail — Email Delivery via SMTP, Gmail — Pošiljanje e-pošte, Manager — Browser or Phone Access, Vodja — Brskalnik / Telefon (+26 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (21): Return (normalized_phone, state) for the configured instance.          States: ", Exception, normalize_wa_phone(), normalize_phone(), Return digits-only WhatsApp-native phone number, or None for invalid input., _make_mock_http(), test_connected_returns_normalized_phone_and_open_state(), test_disconnected_returns_none_and_close_state() (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (11): health(), lifespan(), Belpro FastAPI application entry point., Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null., Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null., Health check — returns ok when the service is up., seed_whatsapp_phone_from_env(), seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (21): make_response_payload(), make_text_payload(), poll_for_entry(), poll_for_entry_gone(), poll_for_entry_status(), post_to_webhook(), Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError, Build a WhatsApp text-message webhook body for the given bare-digit phone. (+13 more)

### Community 10 - "Community 10"
Cohesion: 0.27
Nodes (18): body(), border(), borders(), cell(), complianceTable(), componentTable(), coverPage(), featureTable() (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.3
Nodes (13): analytics_summary(), AnalyticsSummary, HoursPerLocation, HoursPerVolunteer, MonthlyTrendPoint, _preceding_months(), Analytics router — aggregated summary for the dashboard analytics page., Per-volunteer approved hours for a given month. (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (8): BaseHTTPRequestHandler, _Handler, Thin HTTP wrapper around Faster-Whisper for local speech-to-text.  Exposes a sin, Handle POST /transcribe requests., Transcribe the uploaded audio and return plain-text., Health check — GET /health returns 200 ok., Send a simple HTTP response., Route access logs to stdout.

### Community 13 - "Community 13"
Cohesion: 0.21
Nodes (11): _do_run_migrations(), _get_url(), Alembic environment — async SQLAlchemy / asyncpg configuration., Read DATABASE_URL from settings (env / .env file)., Run migrations without a live DB connection (generates SQL script)., Inner helper called inside the async connection context., Create an async engine and run migrations inside it., Run migrations against a live database. (+3 more)

### Community 14 - "Community 14"
Cohesion: 0.24
Nodes (6): SQLAlchemy declarative base shared by all ORM models., SQLAlchemy ORM models — import all to ensure they register with Base.metadata., LogEntryPhoto ORM model — one row per photo, many per log entry., MonthlyReport, MonthlyReport ORM model — tracks generated PDF reports., Tracks generated PDF reports for audit and re-delivery purposes.      volunteer_

### Community 15 - "Community 15"
Cohesion: 0.28
Nodes (8): api_client(), _auth_header(), _manager_password(), n8n_client(), Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable., Session-scoped AsyncClient against n8n. Skips all tests if unreachable., Creates a volunteer with a unique phone, yields the volunteer dict,     deletes, test_volunteer()

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch (idempotent — safe to re-run)., upgrade()

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (5): downgrade(), Add ngo_davcna column to managers.  Revision ID: 007 Revises: 006 Create Date: 2, Add ngo_davcna column to managers., Drop ngo_davcna column from managers., upgrade()

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (5): downgrade(), Rename entry_date to work_date in log_entries.  'work_date' is clearer than 'ent, Rename entry_date to work_date and update index names., Reverse rename: work_date back to entry_date and restore index names., upgrade()

### Community 22 - "Community 22"
Cohesion: 0.6
Nodes (4): _auth(), _get(), main(), Print pending_manager entries as JSON for the manual trigger node.  Usage:   pyt

### Community 23 - "Community 23"
Cohesion: 0.5
Nodes (3): Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw, FastAPI dependency — rejects requests without the correct manager password., require_manager()

### Community 24 - "Community 24"
Cohesion: 0.5
Nodes (3): get_db(), Async SQLAlchemy engine and session factory., FastAPI dependency — yields one async DB session per request.

### Community 25 - "Community 25"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 26 - "Community 26"
Cohesion: 0.5
Nodes (1): Add manager_notified_at column to log_entries.  Revision ID: 008 Revises: 007 Cr

### Community 27 - "Community 27"
Cohesion: 0.5
Nodes (4): Belpro_Architecture.docx — English Architecture Document, Belpro_Arhitektura_Sl.docx — Slovenian Architecture Document, gen_diagrams.py — English Diagram Generator, gen_diagrams_sl.py — Slovenian Diagram Generator

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (2): Health endpoint must return 200 with status ok., test_health_returns_ok()

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Normalize to WhatsApp-native digits-only format; reject unparseable values.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

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

## Knowledge Gaps
- **98 isolated node(s):** `Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw`, `FastAPI dependency — rejects requests without the correct manager password.`, `Application settings — loaded from environment variables / .env file.`, `All configuration for the Belpro API service.      Values are read from the proc`, `Return a cached Settings instance (constructed once per process).` (+93 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Normalize to WhatsApp-native digits-only format; reject unparseable values.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `load_env.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `switch_manager_phone.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `build_graph.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `check_cache.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `merge_ast_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `merge_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EntryStatus` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 11`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `Manager` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 8`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `Community 1` to `Community 8`, `Community 2`, `Community 5`, `Community 13`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `EntryStatus` (e.g. with `Base` and `LogEntryPhoto`) actually correct?**
  _`EntryStatus` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Are the 58 inferred relationships involving `LogEntry` (e.g. with `Base` and `LogEntryPhoto`) actually correct?**
  _`LogEntry` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 53 inferred relationships involving `Manager` (e.g. with `Belpro FastAPI application entry point.` and `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`) actually correct?**
  _`Manager` has 53 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `Volunteer` (e.g. with `EntryStatus` and `LogEntry`) actually correct?**
  _`Volunteer` has 49 INFERRED edges - model-reasoned connections that need verification._