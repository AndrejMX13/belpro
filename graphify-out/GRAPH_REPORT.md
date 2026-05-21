# Graph Report - D:\Andrej\vsCode-workspace\BelPro  (2026-05-21)

## Corpus Check
- 108 files · ~302,069 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1180 nodes · 3232 edges · 95 communities detected
- Extraction: 37% EXTRACTED · 63% INFERRED · 0% AMBIGUOUS · INFERRED: 2021 edges (avg confidence: 0.57)
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
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 190 edges
2. `Manager` - 159 edges
3. `LogEntry` - 125 edges
4. `Volunteer` - 111 edges
5. `LogEntryListResponse` - 68 edges
6. `Settings` - 67 edges
7. `LogEntryCreate` - 67 edges
8. `LogEntryResponse` - 67 edges
9. `PhotoResponse` - 67 edges
10. `PhotoBase64Request` - 67 edges

## Surprising Connections (you probably didn't know these)
- `Settings` --uses--> `Maximum photos allowed per log entry.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py → D:\Andrej\vsCode-workspace\BelPro\api\services\app_settings.py
- `Settings` --uses--> `Number of days approved entry photos are retained on disk.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py → D:\Andrej\vsCode-workspace\BelPro\api\services\app_settings.py
- `Settings` --uses--> `Manager session cookie lifetime in hours.`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py → D:\Andrej\vsCode-workspace\BelPro\api\services\app_settings.py
- `AppSetting ORM model — runtime-tunable key-value configuration.` --uses--> `Base`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\app_setting.py → api\models\base.py
- `One row per named setting. All values stored as TEXT.` --uses--> `Base`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\models\app_setting.py → api\models\base.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (145): Create a signed, self-expiring session token., Return True if the token signature is valid and not expired., Verify password against DB hash or env var fallback., Reject requests without a valid session cookie or Basic Auth credentials., Base, BaseSettings, Generate and stream the GDPR Article 13 consent notice PDF., _check_mx() (+137 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (127): Base, Declarative base — import and subclass in every model., AsyncClient with get_db dependency wired to the test session., HTTP Basic Auth header for the seeded manager., Returns an async callable that inserts a LogEntry row via flush., Run Alembic migrations against belpro_test, seed one Manager row.     Drops all, Per-test session inside a SAVEPOINT.  The app's commit() releases the     savepo, DeclarativeBase (+119 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (71): auth(), client(), db_session(), engine(), log_entry_factory(), Returns an async callable that inserts a Volunteer row via flush (not commit), volunteer_factory(), Exception (+63 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (83): decrypt_emso(), encrypt_emso(), hash_emso(), load_key(), mask_emso(), AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l, Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError, Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag (+75 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (71): AdminSettingsResponse, AdminSettingsUpdate, get_admin_settings(), Pydantic schemas for the admin settings endpoints., Partial update for runtime-tunable settings. Only provided fields are written., Return current values of all runtime-tunable settings., Update one or more runtime-tunable settings. Returns updated state., Current values of all runtime-tunable settings. (+63 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (68): renderAdmin(), _destroyCharts(), loadAnalytics(), renderAnalytics(), renderAnalyticsContent(), _renderCharts(), renderDocuments(), healthWidgetHTML() (+60 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (52): analytics_summary(), AnalyticsSummary, HoursPerLocation, HoursPerVolunteer, MonthlyTrendPoint, _preceding_months(), Analytics router — aggregated summary for the dashboard analytics page., Per-volunteer approved hours for a given month. (+44 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (26): Return (normalized_phone, state) for the configured instance.          States: ", health(), health_detailed(), lifespan(), seed_whatsapp_phone_from_env(), normalize_wa_phone(), normalize_phone(), Return digits-only WhatsApp-native phone number, or None for invalid input. (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (33): delete_logo(), get_logo(), logo_exists(), _open_image(), NGO logo file management., Return the NGO logo as PNG, or 404 if none has been uploaded., Return True if a logo file is present on disk., Remove the logo file if it exists. Silent if absent. (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (34): make_response_payload(), make_text_payload(), poll_for_entry(), poll_for_entry_gone(), poll_for_entry_status(), post_to_webhook(), Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError, Build a WhatsApp text-message webhook body for the given bare-digit phone. (+26 more)

### Community 10 - "Community 10"
Cohesion: 0.1
Nodes (34): Dashboard — Web UI and FastAPI Backend, Nadzorna plošča — Spl. vmesnik + API, Evolution API — WhatsApp Gateway, Evolution API — API Prehod, Gmail — Email Delivery via SMTP, Gmail — Pošiljanje e-pošte, Manager — Browser or Phone Access, Vodja — Brskalnik / Telefon (+26 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (30): _esc(), _now_str(), GDPR Article 13 consent notice PDF generation., Render the GDPR Article 13 consent notice PDF and return raw bytes.      `manage, render_consent_pdf(), _esc(), _fmt_date(), _generated_line() (+22 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (20): _internal_header(), Tests for POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge., PATCH /{id}/acknowledge on unknown id returns 404., GET /api/errors/unacknowledged-count returns integer count., POST with valid internal key creates a record., POST without internal key is rejected., POST with wrong internal key is rejected., GET /api/errors without manager auth is rejected. (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.27
Nodes (18): body(), border(), borders(), cell(), complianceTable(), componentTable(), coverPage(), featureTable() (+10 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (6): _validate_davcna_checksum(), Slovenian tax number (davčna številka) validation utilities., Return True if value passes the Modulus 11 check digit algorithm.      Accepts b, tax_number_valid(), Tests for Slovenian tax number (davčna številka) validation., TestTaxNumberValid

### Community 15 - "Community 15"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.27
Nodes (12): arrow_h(), arrow_h_dashed(), arrow_h_dotted(), arrow_v(), draw_box(), fig1(), fig2(), fig3() (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (8): BaseHTTPRequestHandler, _Handler, Thin HTTP wrapper around Faster-Whisper for local speech-to-text.  Exposes a sin, Handle POST /transcribe requests., Transcribe the uploaded audio and return plain-text., Health check — GET /health returns 200 ok., Send a simple HTTP response., Route access logs to stdout.

### Community 18 - "Community 18"
Cohesion: 0.21
Nodes (11): _do_run_migrations(), _get_url(), Alembic environment — async SQLAlchemy / asyncpg configuration., Read DATABASE_URL from settings (env / .env file)., Run migrations without a live DB connection (generates SQL script)., Inner helper called inside the async connection context., Create an async engine and run migrations inside it., Run migrations against a live database. (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.24
Nodes (8): emso_checksum_valid(), EMŠO (Enotna matična številka občana) validation utilities., Return True if emso passes the mod-11 checksum.      Assumes the caller already, Unit tests for the EMŠO checksum validator utility., test_emso_checksum_valid_accepts_valid_numbers(), test_emso_checksum_valid_rejects_bad_checksum(), test_emso_checksum_valid_rejects_malformed_input(), _validate_emso_checksum()

### Community 20 - "Community 20"
Cohesion: 0.31
Nodes (9): api_request(), cmd_export(), cmd_import(), load_env(), main(), Overwrite each repo workflow file with its current definition from n8n., Parse KEY=VALUE lines from a .env file; ignore comments and blanks., Make an authenticated request to the n8n API.      Returns (status_code, respo (+1 more)

### Community 21 - "Community 21"
Cohesion: 0.28
Nodes (8): api_client(), _auth_header(), _manager_password(), n8n_client(), Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable., Session-scoped AsyncClient against n8n. Skips all tests if unreachable., Creates a volunteer with a unique phone, yields the volunteer dict,     deletes, test_volunteer()

### Community 22 - "Community 22"
Cohesion: 0.38
Nodes (6): dsn_from_url(), main(), POST failure to the API error log., Convert asyncpg DATABASE_URL to psycopg2 DSN., Query approved entries older than retention cutoff, delete their photos and DB r, report_error()

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch (idempotent — safe to re-run)., upgrade()

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (5): downgrade(), Add ngo_davcna column to managers.  Revision ID: 007 Revises: 006 Create Date: 2, Add ngo_davcna column to managers., Drop ngo_davcna column from managers., upgrade()

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (5): downgrade(), Rename entry_date to work_date in log_entries.  'work_date' is clearer than 'ent, Rename entry_date to work_date and update index names., Reverse rename: work_date back to entry_date and restore index names., upgrade()

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (5): downgrade(), Add unique partial indexes to monthly_reports.  One row per volunteer per month;, Create unique partial indexes on monthly_reports., Drop unique partial indexes from monthly_reports., upgrade()

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (5): downgrade(), Add gdpr_additional_clauses to managers.  Revision ID: 011 Revises: 010 Create D, Add gdpr_additional_clauses nullable text column to managers., Remove gdpr_additional_clauses column from managers., upgrade()

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (5): downgrade(), Add error_log table for structured operational failure records.  Revision ID: 01, Create error_log table., Drop error_log table., upgrade()

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (3): SQLAlchemy declarative base shared by all ORM models., LogEntryPhoto ORM model — one row per photo, many per log entry., MonthlyReport ORM model — tracks generated PDF reports.

### Community 33 - "Community 33"
Cohesion: 0.4
Nodes (3): Add settings table for runtime-tunable configuration.  Revision ID: 012 Revises:, Create settings table and seed default values., upgrade()

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (3): get_db(), Async SQLAlchemy engine and session factory., FastAPI dependency — yields one async DB session per request.

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (1): Add manager_notified_at column to log_entries.  Revision ID: 008 Revises: 007 Cr

### Community 37 - "Community 37"
Cohesion: 0.83
Nodes (3): _auth(), _get(), main()

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (2): Health endpoint must return 200 with status ok., test_health_returns_ok()

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
Nodes (1): Reject tax numbers that fail the Modulus 11 check digit.

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Reject tax numbers that fail the Modulus 11 check digit.

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Normalize to WhatsApp-native digits-only format; reject unparseable values.

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
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (0): 

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (0): 

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (0): 

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (0): 

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (0): 

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (0): 

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Raised when the manager has not configured SMTP.

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (1): Return a cached Settings instance (constructed once per process).

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Response schema for GET /managers/me/config-info.

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (1): Per-volunteer aggregated totals for a given month.

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): Aggregated monthly summary across all active volunteers.

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): NGO identity shown in every PDF header.

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Render the NGO header block as an HTML string.

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Render a single-volunteer monthly report PDF and return raw bytes.

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): Render an all-volunteer summary PDF and return raw bytes.

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (1): FastAPI dependency — rejects requests without the correct manager password.

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): Return a cached Settings instance (constructed once per process).

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): Re-encrypt all EMŠOs from old_key to new_key. Returns count of rotated records.

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): Print pending_manager entries as JSON for the manual trigger node.  Usage:   pyt

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): Return a cached Settings instance (constructed once per process).

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): Fields required for first-time manager setup.

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Partial update — all fields optional.  Only provided fields are written.

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Normalize to WhatsApp-native digits-only format; reject unparseable values.

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Payload for the change-password endpoint.

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Manager profile returned by the API.

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Response schema for GET /managers/me/config-info.

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Decrypt EMŠO ciphertext produced by encrypt_emso.      Returns the plaintext str

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): Return HMAC-SHA256 hex digest of plaintext EMŠO.      Deterministic (unlike encr

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (1): Return EMŠO with all but the last 3 characters replaced by *.      Used in all A

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (1): Update or append KEY=value in a .env file. Returns True on success, False on fai

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (1): Belpro_Architecture.docx — English Architecture Document

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (1): Belpro_Arhitektura_Sl.docx — Slovenian Architecture Document

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (1): POST a WhatsApp event to the n8n webhook. Asserts 200.

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (1): Poll GET /api/log-entries until at least one entry for volunteer_id appears.

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (1): Poll GET /api/log-entries/{entry_id} until its status matches expected_status.

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (1): Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): A message from an unregistered phone must not create any log entry.     The work

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Async HTTP client for the Evolution API WhatsApp gateway.

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Return (normalized_phone, state) for the configured instance.          States: "

## Knowledge Gaps
- **227 isolated node(s):** `Application settings — loaded from environment variables / .env file.`, `All configuration for the Belpro API service.      Values are read from the proc`, `Return a cached Settings instance (constructed once per process).`, `Async SQLAlchemy engine and session factory.`, `FastAPI dependency — yields one async DB session per request.` (+222 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 39`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Reject tax numbers that fail the Modulus 11 check digit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Reject tax numbers that fail the Modulus 11 check digit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Normalize to WhatsApp-native digits-only format; reject unparseable values.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `load_env.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `switch_manager_phone.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `build_graph.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `check_cache.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `merge_ast_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `merge_semantic.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Raised when the manager has not configured SMTP.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `Return a cached Settings instance (constructed once per process).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Response schema for GET /managers/me/config-info.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `Per-volunteer aggregated totals for a given month.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Aggregated monthly summary across all active volunteers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `NGO identity shown in every PDF header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Render the NGO header block as an HTML string.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Render a single-volunteer monthly report PDF and return raw bytes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `Render an all-volunteer summary PDF and return raw bytes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `FastAPI dependency — rejects requests without the correct manager password.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `Return a cached Settings instance (constructed once per process).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `Re-encrypt all EMŠOs from old_key to new_key. Returns count of rotated records.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `Print pending_manager entries as JSON for the manual trigger node.  Usage:   pyt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `Return a cached Settings instance (constructed once per process).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `Fields required for first-time manager setup.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `Partial update — all fields optional.  Only provided fields are written.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Normalize to WhatsApp-native digits-only format; reject unparseable values.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Payload for the change-password endpoint.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Manager profile returned by the API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Response schema for GET /managers/me/config-info.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Decrypt EMŠO ciphertext produced by encrypt_emso.      Returns the plaintext str`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `Return HMAC-SHA256 hex digest of plaintext EMŠO.      Deterministic (unlike encr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `Return EMŠO with all but the last 3 characters replaced by *.      Used in all A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `Update or append KEY=value in a .env file. Returns True on success, False on fai`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `Belpro_Architecture.docx — English Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `Belpro_Arhitektura_Sl.docx — Slovenian Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `POST a WhatsApp event to the n8n webhook. Asserts 200.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `Poll GET /api/log-entries until at least one entry for volunteer_id appears.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `Poll GET /api/log-entries/{entry_id} until its status matches expected_status.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `A message from an unregistered phone must not create any log entry.     The work`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Async HTTP client for the Evolution API WhatsApp gateway.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `Return (normalized_phone, state) for the configured instance.          States: "`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EntryStatus` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 6`, `Community 7`, `Community 12`, `Community 18`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `Manager` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 187 inferred relationships involving `EntryStatus` (e.g. with `Base` and `LogEntryPhoto`) actually correct?**
  _`EntryStatus` has 187 INFERRED edges - model-reasoned connections that need verification._
- **Are the 156 inferred relationships involving `Manager` (e.g. with `Belpro FastAPI application entry point.` and `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`) actually correct?**
  _`Manager` has 156 INFERRED edges - model-reasoned connections that need verification._
- **Are the 122 inferred relationships involving `LogEntry` (e.g. with `Belpro FastAPI application entry point.` and `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`) actually correct?**
  _`LogEntry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 108 inferred relationships involving `Volunteer` (e.g. with `EntryStatus` and `LogEntry`) actually correct?**
  _`Volunteer` has 108 INFERRED edges - model-reasoned connections that need verification._