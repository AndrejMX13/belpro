# Graph Report - .  (2026-05-21)

## Corpus Check
- 156 files · ~308,357 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1066 nodes · 1644 edges · 84 communities detected
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 449 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Admin Settings & Ops Notification|Admin Settings & Ops Notification]]
- [[_COMMUNITY_Test Fixtures & Factories|Test Fixtures & Factories]]
- [[_COMMUNITY_Frontend Dashboard JS|Frontend Dashboard JS]]
- [[_COMMUNITY_Volunteer EMSO & Encryption|Volunteer EMSO & Encryption]]
- [[_COMMUNITY_Report Generation & Delivery|Report Generation & Delivery]]
- [[_COMMUNITY_WhatsApp & Phone Integration|WhatsApp & Phone Integration]]
- [[_COMMUNITY_Volunteer Data & Validation|Volunteer Data & Validation]]
- [[_COMMUNITY_NGO Logo Management|NGO Logo Management]]
- [[_COMMUNITY_Ops Server & Reconfiguration|Ops Server & Reconfiguration]]
- [[_COMMUNITY_Workflow Integration Tests|Workflow Integration Tests]]
- [[_COMMUNITY_Log Entry Lifecycle|Log Entry Lifecycle]]
- [[_COMMUNITY_Session Authentication|Session Authentication]]
- [[_COMMUNITY_Database Models|Database Models]]
- [[_COMMUNITY_GDPR Consent PDF|GDPR Consent PDF]]
- [[_COMMUNITY_Error Logging Tests|Error Logging Tests]]
- [[_COMMUNITY_Manager & Phone Seeding|Manager & Phone Seeding]]
- [[_COMMUNITY_Tax Number Validation|Tax Number Validation]]
- [[_COMMUNITY_Diagram Generation EN|Diagram Generation EN]]
- [[_COMMUNITY_Diagram Generation SL|Diagram Generation SL]]
- [[_COMMUNITY_Admin Settings Tests|Admin Settings Tests]]
- [[_COMMUNITY_n8n Workflow Scripts|n8n Workflow Scripts]]
- [[_COMMUNITY_Workflow Test Fixtures|Workflow Test Fixtures]]
- [[_COMMUNITY_Architecture Diagram EN|Architecture Diagram EN]]
- [[_COMMUNITY_Monthly Report Send Script|Monthly Report Send Script]]
- [[_COMMUNITY_Ops Photo Cleanup|Ops Photo Cleanup]]
- [[_COMMUNITY_Feature Planning Docs|Feature Planning Docs]]
- [[_COMMUNITY_PDF & Logo Features|PDF & Logo Features]]
- [[_COMMUNITY_Architecture Diagram SL|Architecture Diagram SL]]
- [[_COMMUNITY_Migration Initial Schema|Migration Initial Schema]]
- [[_COMMUNITY_Migration Log Entry Photos|Migration Log Entry Photos]]
- [[_COMMUNITY_Migration Report Prefs|Migration Report Prefs]]
- [[_COMMUNITY_Migration WhatsApp SMTP|Migration WhatsApp SMTP]]
- [[_COMMUNITY_Migration NGO Davcna|Migration NGO Davcna]]
- [[_COMMUNITY_Migration Work Date Rename|Migration Work Date Rename]]
- [[_COMMUNITY_Migration Reports Unique Index|Migration Reports Unique Index]]
- [[_COMMUNITY_Migration GDPR Clauses|Migration GDPR Clauses]]
- [[_COMMUNITY_Migration Error Log Table|Migration Error Log Table]]
- [[_COMMUNITY_Analytics Summary|Analytics Summary]]
- [[_COMMUNITY_EMSO Key Rotation|EMSO Key Rotation]]
- [[_COMMUNITY_Auth & WhatsApp Concepts|Auth & WhatsApp Concepts]]
- [[_COMMUNITY_Migration Settings Table|Migration Settings Table]]
- [[_COMMUNITY_Migration EMSO Hash|Migration EMSO Hash]]
- [[_COMMUNITY_Migration Manager Notified|Migration Manager Notified]]
- [[_COMMUNITY_List Pending Entries Script|List Pending Entries Script]]
- [[_COMMUNITY_BelPro Specification|BelPro Specification]]
- [[_COMMUNITY_Entry & Contact Edit Plans|Entry & Contact Edit Plans]]
- [[_COMMUNITY_Test Suite Plans|Test Suite Plans]]
- [[_COMMUNITY_Error Log & Ops Sidecar|Error Log & Ops Sidecar]]
- [[_COMMUNITY_Health Check Tests|Health Check Tests]]
- [[_COMMUNITY_HTTPOnly Cookie Auth|HTTPOnly Cookie Auth]]
- [[_COMMUNITY_Evolution API Logo|Evolution API Logo]]
- [[_COMMUNITY_WeasyPrint Dependencies|WeasyPrint Dependencies]]
- [[_COMMUNITY_Photo Upload Limit|Photo Upload Limit]]
- [[_COMMUNITY_Graphify Build Scripts|Graphify Build Scripts]]
- [[_COMMUNITY_Manager Field Rationale|Manager Field Rationale]]
- [[_COMMUNITY_Manager Rationale|Manager Rationale]]
- [[_COMMUNITY_Manager Rationale B|Manager Rationale B]]
- [[_COMMUNITY_Volunteer Rationale|Volunteer Rationale]]
- [[_COMMUNITY_Volunteer Rationale B|Volunteer Rationale B]]
- [[_COMMUNITY_Volunteer Rationale C|Volunteer Rationale C]]
- [[_COMMUNITY_API Tests Init|API Tests Init]]
- [[_COMMUNITY_API Utils Init|API Utils Init]]
- [[_COMMUNITY_Frontend API Client|Frontend API Client]]
- [[_COMMUNITY_Load Env Script|Load Env Script]]
- [[_COMMUNITY_Switch Manager Phone Script|Switch Manager Phone Script]]
- [[_COMMUNITY_Graphify Cache Script|Graphify Cache Script]]
- [[_COMMUNITY_Graphify Merge AST Script|Graphify Merge AST Script]]
- [[_COMMUNITY_Graphify Merge Semantic Script|Graphify Merge Semantic Script]]
- [[_COMMUNITY_Tests Init|Tests Init]]
- [[_COMMUNITY_Workflow Tests Init|Workflow Tests Init]]
- [[_COMMUNITY_BelPro Roadmap|BelPro Roadmap]]
- [[_COMMUNITY_Security Policy|Security Policy]]
- [[_COMMUNITY_FastAPI Dependency|FastAPI Dependency]]
- [[_COMMUNITY_SQLAlchemy Dependency|SQLAlchemy Dependency]]
- [[_COMMUNITY_Delete Entries Plan|Delete Entries Plan]]
- [[_COMMUNITY_Location Edit Spec|Location Edit Spec]]
- [[_COMMUNITY_Test Suite Spec|Test Suite Spec]]
- [[_COMMUNITY_Work Date Dashboard Spec|Work Date Dashboard Spec]]
- [[_COMMUNITY_Volunteer Contact Spec|Volunteer Contact Spec]]
- [[_COMMUNITY_Version Bump Spec|Version Bump Spec]]
- [[_COMMUNITY_n8n Workflow Scripts Spec|n8n Workflow Scripts Spec]]
- [[_COMMUNITY_Graph HTML Output|Graph HTML Output]]
- [[_COMMUNITY_Ops Requirements|Ops Requirements]]
- [[_COMMUNITY_Architecture SL Diagram|Architecture SL Diagram]]

## God Nodes (most connected - your core abstractions)
1. `volunteer_factory()` - 52 edges
2. `log_entry_factory()` - 34 edges
3. `$()` - 33 edges
4. `AppSettings` - 24 edges
5. `setHtml()` - 23 edges
6. `Settings` - 21 edges
7. `get_settings()` - 21 edges
8. `AppSetting` - 21 edges
9. `esc()` - 19 edges
10. `load_key()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `settings DB table spec` --references--> `AppSettings service class`  [INFERRED]
  SPEC.md → api/services/app_settings.py
- `Roadmap: Central settings service (shipped v0.11.0)` --references--> `AppSettings service class`  [INFERRED]
  ROADMAP.md → api/services/app_settings.py
- `_validate_davcna_checksum()` --calls--> `tax_number_valid()`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py → D:\Andrej\vsCode-workspace\BelPro\api\utils\tax_number.py
- `EMÅ O AES-256 encryption security requirement` --references--> `Settings (Pydantic BaseSettings)`  [INFERRED]
  SECURITY.md → api/core/settings.py
- `CLAUDE.md â€” Codebase instructions` --references--> `AppSettings service class`  [EXTRACTED]
  CLAUDE.md → api/services/app_settings.py

## Hyperedges (group relationships)
- **Admin Settings Read/Write Pipeline** — admin_get_admin_settings, admin_update_admin_settings, appsettings_AppSettings, settings_Settings, schemas_AdminSettingsResponse, schemas_AdminSettingsUpdate [EXTRACTED 0.95]
- **Ops Crontab Reconfiguration Flow** — admin__notify_ops, ops_server_reconfigure_endpoint, ops_server_write_crontab, ops_server_reload_crond, ops_monthly_report_send [EXTRACTED 0.95]
- **Admin Settings Test Coverage** — test_admin_get_defaults, test_admin_patch_saves, test_admin_patch_notifies_ops, test_admin_ops_failure_graceful, requirements_test [EXTRACTED 0.90]
- **pytest infrastructure: conftest, fixtures, factories** — plan_test_suite, test_strategy_regression [EXTRACTED 1.00]
- **Editable work_date field on entry detail** — plan_work_date_rename, plan_log_entry_location_edit [EXTRACTED 0.90]
- **Dashboard entry creation via 'Dodaj vnos' button** — plan_work_date_rename [EXTRACTED 1.00]
- **Inline editing of volunteer name, phone, email** — plan_volunteer_contact_inline_edit, plan_whatsapp_phone_sot [INFERRED 0.75]
- **Safe EMÅ O key rotation with backup/restore** — plan_rotate_emso_key, doc_emso_rotation, concept_emso_encryption_rotation [EXTRACTED 0.95]
- **n8n workflow management: import/export via Python script** — plan_n8n_workflow_scripts, plan_fix_image_upload [EXTRACTED 0.85]
- **Photo upload limit: volunteer-side enforcement in n8n** — plan_photo_upload_limit, concept_photo_limit_enforcement [EXTRACTED 1.00]
- **WeasyPrint PDF Generation Features** — feature_ngo_logo, feature_pdf_report_history, feature_gdpr_consent, component_weasyprint [EXTRACTED 1.00]
- **Operational Visibility: Logging & Error Tracking** — feature_ops_sidecar, feature_report_delivery_errors, component_error_log [EXTRACTED 1.00]
- **Runtime Configuration & Settings Management** — feature_settings_table, feature_auto_monthly_reports, component_app_settings [EXTRACTED 1.00]
- **WhatsApp Voice/Message Ingestion Pipeline** — architecture_volunteer, architecture_evolution_api, architecture_n8n, architecture_faster_whisper [EXTRACTED 1.00]
- **Core Backend Services** — architecture_n8n, architecture_postgresql, architecture_smtp, architecture_fastapi_dashboard [EXTRACTED 0.90]
- **WhatsApp Voice/Photo Ingestion Pipeline** — architecture_sl_volunteer, architecture_sl_evolution_api, architecture_sl_n8n, architecture_sl_whisper [EXTRACTED 1.00]
- **Data Persistence and Notification Subsystem** — architecture_sl_n8n, architecture_sl_postgresql, architecture_sl_smtp [EXTRACTED 1.00]
- **Manager Dashboard Integration** — architecture_sl_evolution_api, architecture_sl_n8n, architecture_sl_fastapi_dashboard [INFERRED 0.85]

## Communities

### Community 0 - "Admin Settings & Ops Notification"
Cohesion: 0.03
Nodes (117): AdminSettingsResponse, AdminSettingsUpdate, get_admin_settings(), _notify_ops(), Pydantic schemas for the admin settings endpoints., Partial update for runtime-tunable settings. Only provided fields are written., POST /reconfigure to ops. Logs and persists error on failure; never raises., Return current values of all runtime-tunable settings. (+109 more)

### Community 1 - "Test Fixtures & Factories"
Cohesion: 0.03
Nodes (98): auth(), client(), db_session(), engine(), log_entry_factory(), AsyncClient with get_db dependency wired to the test session., HTTP Basic Auth header for the seeded manager., Returns an async callable that inserts a Volunteer row via flush (not commit) (+90 more)

### Community 2 - "Frontend Dashboard JS"
Cohesion: 0.08
Nodes (63): renderAdmin(), renderDocuments(), healthWidgetHTML(), initAppLogPage(), loadAppLog(), loadHealthWidget(), refreshErrorBadge(), renderAppLog() (+55 more)

### Community 3 - "Volunteer EMSO & Encryption"
Cohesion: 0.06
Nodes (54): decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError, Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag (+46 more)

### Community 4 - "Report Generation & Delivery"
Cohesion: 0.06
Nodes (45): _check_mx(), Async email sender backed by aiosmtplib.  Reads SMTP config from the Manager row, Raise ValueError if the recipient domain has no MX records., Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port, send_email(), logo_src(), Return a data URI for the NGO logo, or None if no logo is uploaded., MonthlyReportSummary (+37 more)

### Community 5 - "WhatsApp & Phone Integration"
Cohesion: 0.07
Nodes (36): EvolutionClient, Async HTTP client for the Evolution API WhatsApp gateway., Return (normalized_phone, state) for the configured instance.          States: ", Send a PDF document to a WhatsApp number via Evolution API sendMedia., ConfigInfoResponse, ManagerCreate, ManagerResponse, ManagerUpdate (+28 more)

### Community 6 - "Volunteer Data & Validation"
Cohesion: 0.06
Nodes (39): emso_checksum_valid(), EMŠO (Enotna matična številka občana) validation utilities., Return True if emso passes the mod-11 checksum.      Assumes the caller already, Unit tests for the EMŠO checksum validator utility., test_emso_checksum_valid_accepts_valid_numbers(), test_emso_checksum_valid_rejects_bad_checksum(), test_emso_checksum_valid_rejects_malformed_input(), Unit tests for VolunteerUpdate schema — no DB required. (+31 more)

### Community 7 - "NGO Logo Management"
Cohesion: 0.08
Nodes (33): delete_logo(), get_logo(), logo_exists(), _open_image(), NGO logo file management., Return the NGO logo as PNG, or 404 if none has been uploaded., Return True if a logo file is present on disk., Remove the logo file if it exists. Silent if absent. (+25 more)

### Community 8 - "Ops Server & Reconfiguration"
Cohesion: 0.07
Nodes (34): _notify_ops() helper, Admin APIRouter (/admin), AppSettings service class, get_app_settings() FastAPI dependency, BaseHTTPRequestHandler, BelPro CHANGELOG, CLAUDE.md â€” Codebase instructions, report_error() in monthly_report_send.py (+26 more)

### Community 9 - "Workflow Integration Tests"
Cohesion: 0.11
Nodes (34): make_response_payload(), make_text_payload(), poll_for_entry(), poll_for_entry_gone(), poll_for_entry_status(), post_to_webhook(), Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError, Build a WhatsApp text-message webhook body for the given bare-digit phone. (+26 more)

### Community 10 - "Log Entry Lifecycle"
Cohesion: 0.07
Nodes (31): approve_log_entry(), confirm_log_entry(), delete_log_entry(), delete_photo(), _extract_exif(), get_log_entry(), get_photo_file(), get_photo_limit() (+23 more)

### Community 11 - "Session Authentication"
Cohesion: 0.09
Nodes (23): login(), LoginRequest, LoginResponse, logout(), _make_session_token(), Schemas for the auth endpoints., Response for login and logout endpoints., Verify manager password and set an httpOnly session cookie. (+15 more)

### Community 12 - "Database Models"
Cohesion: 0.07
Nodes (22): AppSetting ORM model — runtime-tunable key-value configuration., Pydantic schemas for the error_log endpoint., SQLAlchemy ORM models — import all to ensure they register with Base.metadata., create_log_entry(), Create a new log entry.  Volunteer must exist and be active., EntryStatus, LogEntry, Pydantic schemas for the LogEntry entity. (+14 more)

### Community 13 - "GDPR Consent PDF"
Cohesion: 0.09
Nodes (23): _esc(), _now_str(), GDPR Article 13 consent notice PDF generation., Render the GDPR Article 13 consent notice PDF and return raw bytes.      `manage, render_consent_pdf(), download_consent_pdf(), Documents router — downloadable compliance documents., Generate and stream the GDPR Article 13 consent notice PDF. (+15 more)

### Community 14 - "Error Logging Tests"
Cohesion: 0.12
Nodes (20): _internal_header(), Tests for POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge., PATCH /{id}/acknowledge on unknown id returns 404., GET /api/errors/unacknowledged-count returns integer count., POST with valid internal key creates a record., POST without internal key is rejected., POST with wrong internal key is rejected., GET /api/errors without manager auth is rejected. (+12 more)

### Community 15 - "Manager & Phone Seeding"
Cohesion: 0.12
Nodes (6): Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null., seed_whatsapp_phone_from_env(), seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null, seed_whatsapp_phone_from_env leaves existing DB value untouched., test_seed_whatsapp_phone_does_not_overwrite_existing_value(), test_seed_whatsapp_phone_populates_null_db_field()

### Community 16 - "Tax Number Validation"
Cohesion: 0.18
Nodes (5): Slovenian tax number (davčna številka) validation utilities., Return True if value passes the Modulus 11 check digit algorithm.      Accepts b, tax_number_valid(), Tests for Slovenian tax number (davčna številka) validation., TestTaxNumberValid

### Community 17 - "Diagram Generation EN"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 18 - "Diagram Generation SL"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 19 - "Admin Settings Tests"
Cohesion: 0.2
Nodes (9): Tests for report auto-delivery settings., GET /api/admin/settings returns defaults for report_auto_day and report_auto_per, PATCH /api/admin/settings persists report_auto_day and report_auto_period., PATCH /api/admin/settings calls ops /reconfigure with updated values., PATCH /api/admin/settings still returns 200 when ops service is unreachable., test_get_settings_returns_report_defaults(), test_patch_settings_notifies_ops(), test_patch_settings_ops_failure_does_not_break_save() (+1 more)

### Community 20 - "n8n Workflow Scripts"
Cohesion: 0.31
Nodes (9): api_request(), cmd_export(), cmd_import(), load_env(), main(), Overwrite each repo workflow file with its current definition from n8n., Parse KEY=VALUE lines from a .env file; ignore comments and blanks., Make an authenticated request to the n8n API.      Returns (status_code, respo (+1 more)

### Community 21 - "Workflow Test Fixtures"
Cohesion: 0.28
Nodes (8): api_client(), _auth_header(), _manager_password(), n8n_client(), Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable., Session-scoped AsyncClient against n8n. Skips all tests if unreachable., Creates a volunteer with a unique phone, yields the volunteer dict,     deletes, test_volunteer()

### Community 22 - "Architecture Diagram EN"
Cohesion: 0.5
Nodes (8): Evolution API (WhatsApp Gateway), FastAPI + Web Dashboard (Manager UI & API), Faster-Whisper (Speech-to-Text CPU), n8n Workflow (Business Logic Engine), PostgreSQL 18 (Data Store), SMTP (Email Delivery), BelPro System Architecture Diagram, Volunteer (WhatsApp)

### Community 23 - "Monthly Report Send Script"
Cohesion: 0.38
Nodes (6): main(), POST failure to the API error log., Return (year, month) for the given period label.      'current'  → today's year, Resolve target month and call the send-monthly API endpoint., report_error(), resolve_period()

### Community 24 - "Ops Photo Cleanup"
Cohesion: 0.38
Nodes (6): dsn_from_url(), main(), POST failure to the API error log., Convert asyncpg DATABASE_URL to psycopg2 DSN., Query approved entries older than retention cutoff, delete their photos and DB r, report_error()

### Community 25 - "Feature Planning Docs"
Cohesion: 0.29
Nodes (7): AppSettings Central Authority, Auto Monthly Report Delivery, Settings Table (ISS-026), No caching on AppSettings; single-tenant, low-frequency reads justify DB query per request, ThreadingHTTPServer handles concurrent requests; main loop never blocks crond, Auto Monthly Report Delivery Design, Settings Table Design Spec

### Community 26 - "PDF & Logo Features"
Cohesion: 0.29
Nodes (7): WeasyPrint PDF Generation, GDPR Consent Document (ISS-015), NGO Logo Feature, PDF Report History (ISS-024), Logo stored at /app/photos/logo/logo.png for backup script coverage, Partial unique indexes prevent duplicate monthly report rows per volunteer/period, GDPR Consent Document Design Spec

### Community 27 - "Architecture Diagram SL"
Cohesion: 0.33
Nodes (7): Evolution API (WhatsApp Gateway), FastAPI + Web Dashboard (Manager UI and API), n8n Workflow Engine, PostgreSQL 18 (Database), SMTP (Email Delivery), Prostovoljec (Volunteer via WhatsApp), Faster-Whisper (Speech-to-Text, CPU)

### Community 28 - "Migration Initial Schema"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch (idempotent — safe to re-run)., upgrade()

### Community 29 - "Migration Log Entry Photos"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 30 - "Migration Report Prefs"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 31 - "Migration WhatsApp SMTP"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 32 - "Migration NGO Davcna"
Cohesion: 0.33
Nodes (5): downgrade(), Add ngo_davcna column to managers.  Revision ID: 007 Revises: 006 Create Date: 2, Add ngo_davcna column to managers., Drop ngo_davcna column from managers., upgrade()

### Community 33 - "Migration Work Date Rename"
Cohesion: 0.33
Nodes (5): downgrade(), Rename entry_date to work_date in log_entries.  'work_date' is clearer than 'ent, Rename entry_date to work_date and update index names., Reverse rename: work_date back to entry_date and restore index names., upgrade()

### Community 34 - "Migration Reports Unique Index"
Cohesion: 0.33
Nodes (5): downgrade(), Add unique partial indexes to monthly_reports.  One row per volunteer per month;, Create unique partial indexes on monthly_reports., Drop unique partial indexes from monthly_reports., upgrade()

### Community 35 - "Migration GDPR Clauses"
Cohesion: 0.33
Nodes (5): downgrade(), Add gdpr_additional_clauses to managers.  Revision ID: 011 Revises: 010 Create D, Add gdpr_additional_clauses nullable text column to managers., Remove gdpr_additional_clauses column from managers., upgrade()

### Community 36 - "Migration Error Log Table"
Cohesion: 0.33
Nodes (5): downgrade(), Add error_log table for structured operational failure records.  Revision ID: 01, Create error_log table., Drop error_log table., upgrade()

### Community 37 - "Analytics Summary"
Cohesion: 0.4
Nodes (5): analytics_summary(), _preceding_months(), Analytics router — aggregated summary for the dashboard analytics page., Return `count` consecutive (year, month) tuples ending at (year, month)., Return aggregated analytics data scoped to the given month.      Defaults to t

### Community 38 - "EMSO Key Rotation"
Cohesion: 0.4
Nodes (6): Backup 2026-05-18 17:00:50, EMÅ O encryption key rotation, EMÅ O Key Rotation Guide, EMÅ O Key Rotation Guide (Slovenian), EMÅ O Key Rotation Script Plan, Upgrade Script Implementation Plan

### Community 39 - "Auth & WhatsApp Concepts"
Cohesion: 0.33
Nodes (6): httpOnly session cookie auth, WhatsApp phone as single source of truth, Fix Image Upload Env Access Plan, httpOnly Cookie Auth (ISS-005) Plan, n8n Workflow Import/Export Script Plan, WhatsApp Phone Source of Truth Plan

### Community 40 - "Migration Settings Table"
Cohesion: 0.4
Nodes (3): Add settings table for runtime-tunable configuration.  Revision ID: 012 Revises:, Create settings table and seed default values., upgrade()

### Community 41 - "Migration EMSO Hash"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 42 - "Migration Manager Notified"
Cohesion: 0.5
Nodes (1): Add manager_notified_at column to log_entries.  Revision ID: 008 Revises: 007 Cr

### Community 43 - "List Pending Entries Script"
Cohesion: 0.83
Nodes (3): _auth(), _get(), main()

### Community 44 - "BelPro Specification"
Cohesion: 0.5
Nodes (4): BelPro System Specification, Data Model (volunteers, managers, log_entries, settings, error_log), Rationale: Use n8n nodes first, custom code only when needed, WhatsApp Volunteer Entry Flow

### Community 45 - "Entry & Contact Edit Plans"
Cohesion: 0.5
Nodes (4): entry_date â†’ work_date refactor, Log Entry Location Edit Implementation Plan, Volunteer Contact Inline Edit Plan, Work Date Rename Implementation Plan

### Community 46 - "Test Suite Plans"
Cohesion: 0.5
Nodes (4): Test Suite Implementation Plan, Workflow Integration Tests Plan, n8n integration tests (end-to-end WhatsApp), Regression test suite (pytest)

### Community 47 - "Error Log & Ops Sidecar"
Cohesion: 0.5
Nodes (4): ErrorLog DB Table & API, Ops Sidecar & Error Logging (ISS-004/014/007/012), Report Delivery Error Visibility, SmtpNotConfiguredError collapsed into general exception handler to prevent batch abort

### Community 48 - "Health Check Tests"
Cohesion: 0.67
Nodes (2): Health endpoint must return 200 with status ok., test_health_returns_ok()

### Community 49 - "HTTPOnly Cookie Auth"
Cohesion: 0.67
Nodes (3): Frontend HTML (index.html), httpOnly cookie moves credential out of JavaScript reach to prevent XSS theft, httpOnly Cookie Auth (ISS-005)

### Community 50 - "Evolution API Logo"
Cohesion: 0.67
Nodes (3): Evolution API Logo, Evolution API Service, WhatsApp Integration

### Community 51 - "WeasyPrint Dependencies"
Cohesion: 1.0
Nodes (2): pydyf 0.10.0 (PDF dep), WeasyPrint 62.3 (PDF)

### Community 52 - "Photo Upload Limit"
Cohesion: 1.0
Nodes (2): Photo upload limit enforcement, Photo Upload Limit (ISS-002) Plan

### Community 53 - "Graphify Build Scripts"
Cohesion: 1.0
Nodes (1): Graphify Knowledge Graph Report

### Community 54 - "Manager Field Rationale"
Cohesion: 1.0
Nodes (1): Reject tax numbers that fail the Modulus 11 check digit.

### Community 55 - "Manager Rationale"
Cohesion: 1.0
Nodes (1): Reject tax numbers that fail the Modulus 11 check digit.

### Community 56 - "Manager Rationale B"
Cohesion: 1.0
Nodes (1): Normalize to WhatsApp-native digits-only format; reject unparseable values.

### Community 57 - "Volunteer Rationale"
Cohesion: 1.0
Nodes (1): Reject EMŠO numbers that fail the mod-11 checksum.

### Community 58 - "Volunteer Rationale B"
Cohesion: 1.0
Nodes (1): Normalise phone to bare E.164 digits, pass through None.

### Community 59 - "Volunteer Rationale C"
Cohesion: 1.0
Nodes (1): Treat empty string as absent — store None rather than ''.

### Community 60 - "API Tests Init"
Cohesion: 1.0
Nodes (0): 

### Community 61 - "API Utils Init"
Cohesion: 1.0
Nodes (0): 

### Community 62 - "Frontend API Client"
Cohesion: 1.0
Nodes (0): 

### Community 63 - "Load Env Script"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Switch Manager Phone Script"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Graphify Cache Script"
Cohesion: 1.0
Nodes (0): 

### Community 66 - "Graphify Merge AST Script"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Graphify Merge Semantic Script"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Tests Init"
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Workflow Tests Init"
Cohesion: 1.0
Nodes (0): 

### Community 70 - "BelPro Roadmap"
Cohesion: 1.0
Nodes (1): BelPro Roadmap

### Community 71 - "Security Policy"
Cohesion: 1.0
Nodes (1): BelPro Security Policy

### Community 72 - "FastAPI Dependency"
Cohesion: 1.0
Nodes (1): FastAPI 0.115.5

### Community 73 - "SQLAlchemy Dependency"
Cohesion: 1.0
Nodes (1): SQLAlchemy 2.0.36

### Community 74 - "Delete Entries Plan"
Cohesion: 1.0
Nodes (1): Delete Non-Approved Entries Plan

### Community 75 - "Location Edit Spec"
Cohesion: 1.0
Nodes (1): Log Entry Location Edit Design

### Community 76 - "Test Suite Spec"
Cohesion: 1.0
Nodes (1): Test Suite Design

### Community 77 - "Work Date Dashboard Spec"
Cohesion: 1.0
Nodes (1): Work Date Rename & Dashboard Entry Design

### Community 78 - "Volunteer Contact Spec"
Cohesion: 1.0
Nodes (1): Volunteer Contact Info Inline Edit

### Community 79 - "Version Bump Spec"
Cohesion: 1.0
Nodes (1): Version-Bump Skill Design

### Community 80 - "n8n Workflow Scripts Spec"
Cohesion: 1.0
Nodes (1): n8n Workflow Import/Export Script Design

### Community 81 - "Graph HTML Output"
Cohesion: 1.0
Nodes (1): Graphify Knowledge Graph (HTML)

### Community 82 - "Ops Requirements"
Cohesion: 1.0
Nodes (1): Ops Service Requirements

### Community 83 - "Architecture SL Diagram"
Cohesion: 1.0
Nodes (1): Architecture Diagram (Slovenian)

## Knowledge Gaps
- **362 isolated node(s):** `Belpro FastAPI application entry point.`, `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`, `Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null.`, `Health check — returns ok when the service is up.`, `Per-service health status for the manager dashboard widget.` (+357 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `WeasyPrint Dependencies`** (2 nodes): `pydyf 0.10.0 (PDF dep)`, `WeasyPrint 62.3 (PDF)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Photo Upload Limit`** (2 nodes): `Photo upload limit enforcement`, `Photo Upload Limit (ISS-002) Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graphify Build Scripts`** (2 nodes): `build_graph.py`, `Graphify Knowledge Graph Report`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Manager Field Rationale`** (1 nodes): `Reject tax numbers that fail the Modulus 11 check digit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Manager Rationale`** (1 nodes): `Reject tax numbers that fail the Modulus 11 check digit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Manager Rationale B`** (1 nodes): `Normalize to WhatsApp-native digits-only format; reject unparseable values.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Volunteer Rationale`** (1 nodes): `Reject EMŠO numbers that fail the mod-11 checksum.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Volunteer Rationale B`** (1 nodes): `Normalise phone to bare E.164 digits, pass through None.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Volunteer Rationale C`** (1 nodes): `Treat empty string as absent — store None rather than ''.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `API Tests Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `API Utils Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend API Client`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Load Env Script`** (1 nodes): `load_env.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Switch Manager Phone Script`** (1 nodes): `switch_manager_phone.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graphify Cache Script`** (1 nodes): `check_cache.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graphify Merge AST Script`** (1 nodes): `merge_ast_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graphify Merge Semantic Script`** (1 nodes): `merge_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tests Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflow Tests Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `BelPro Roadmap`** (1 nodes): `BelPro Roadmap`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Security Policy`** (1 nodes): `BelPro Security Policy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `FastAPI Dependency`** (1 nodes): `FastAPI 0.115.5`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `SQLAlchemy Dependency`** (1 nodes): `SQLAlchemy 2.0.36`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Delete Entries Plan`** (1 nodes): `Delete Non-Approved Entries Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Location Edit Spec`** (1 nodes): `Log Entry Location Edit Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Test Suite Spec`** (1 nodes): `Test Suite Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Work Date Dashboard Spec`** (1 nodes): `Work Date Rename & Dashboard Entry Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Volunteer Contact Spec`** (1 nodes): `Volunteer Contact Info Inline Edit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Version Bump Spec`** (1 nodes): `Version-Bump Skill Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `n8n Workflow Scripts Spec`** (1 nodes): `n8n Workflow Import/Export Script Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graph HTML Output`** (1 nodes): `Graphify Knowledge Graph (HTML)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Requirements`** (1 nodes): `Ops Service Requirements`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Architecture SL Diagram`** (1 nodes): `Architecture Diagram (Slovenian)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `Admin Settings & Ops Notification` to `Ops Server & Reconfiguration`, `Test Fixtures & Factories`, `Report Generation & Delivery`, `Error Logging Tests`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `send_monthly_reports()` connect `Report Generation & Delivery` to `Admin Settings & Ops Notification`, `Test Fixtures & Factories`, `WhatsApp & Phone Integration`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `volunteer_factory()` connect `Test Fixtures & Factories` to `Admin Settings & Ops Notification`, `Volunteer EMSO & Encryption`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `volunteer_factory()` (e.g. with `get_settings()` and `load_key()`) actually correct?**
  _`volunteer_factory()` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `str` (e.g. with `health_detailed()` and `_notify_ops()`) actually correct?**
  _`str` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `log_entry_factory()` (e.g. with `test_analytics_summary_counts_approved_hours()` and `test_photo_upload_respects_db_max_photos_setting()`) actually correct?**
  _`log_entry_factory()` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `$()` (e.g. with `renderAdmin()` and `renderDocuments()`) actually correct?**
  _`$()` has 8 INFERRED edges - model-reasoned connections that need verification._