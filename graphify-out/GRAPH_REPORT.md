# Graph Report - D:\Andrej\vsCode-workspace\BelPro  (2026-05-14)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 442 nodes · 822 edges · 34 communities detected
- Extraction: 66% EXTRACTED · 34% INFERRED · 0% AMBIGUOUS · INFERRED: 276 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_volunteer_factory()|volunteer_factory()]]
- [[_COMMUNITY_EntryStatus|EntryStatus]]
- [[_COMMUNITY_volunteers.js|volunteers.js]]
- [[_COMMUNITY_volunteer.py|volunteer.py]]
- [[_COMMUNITY_normalize_phone()|normalize_phone()]]
- [[_COMMUNITY_write_env_key()|write_env_key()]]
- [[_COMMUNITY_report_pdf.py|report_pdf.py]]
- [[_COMMUNITY_test_edit_path()|test_edit_path()]]
- [[_COMMUNITY_VolunteerUpdate|VolunteerUpdate]]
- [[_COMMUNITY_manager.py|manager.py]]
- [[_COMMUNITY_conftest.py|conftest.py]]
- [[_COMMUNITY_001_initial_schema.py|001_initial_schema.py]]
- [[_COMMUNITY_004_log_entry_photos.py|004_log_entry_photos.py]]
- [[_COMMUNITY_005_report_prefs.py|005_report_prefs.py]]
- [[_COMMUNITY_006_whatsapp_and_smtp_config.py|006_whatsapp_and_smtp_config.py]]
- [[_COMMUNITY_007_add_ngo_davcna.py|007_add_ngo_davcna.py]]
- [[_COMMUNITY_009_rename_entry_date_to_work_date.py|009_rename_entry_date_to_work_date.py]]
- [[_COMMUNITY_analytics_summary()|analytics_summary()]]
- [[_COMMUNITY_test_reports.py|test_reports.py]]
- [[_COMMUNITY_list_pending_entries.py|list_pending_entries.py]]
- [[_COMMUNITY_002_add_emso_hash.py|002_add_emso_hash.py]]
- [[_COMMUNITY_008_add_manager_notified_at.py|008_add_manager_notified_at.py]]
- [[_COMMUNITY_test_health_returns_ok()|test_health_returns_ok()]]
- [[_COMMUNITY_Normalize to WhatsApp-native digits-only format; reject unparseable values.|Normalize to WhatsApp-native digits-only format; reject unparseable values.]]
- [[_COMMUNITY_Normalise phone to bare E.164 digits, pass through None.|Normalise phone to bare E.164 digits, pass through None.]]
- [[_COMMUNITY_Treat empty string as absent — store None rather than ''.|Treat empty string as absent — store None rather than ''.]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY_api.js|api.js]]
- [[_COMMUNITY_load_env.ps1|load_env.ps1]]
- [[_COMMUNITY_switch_manager_phone.ps1|switch_manager_phone.ps1]]
- [[_COMMUNITY_export_wf.py|export_wf.py]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY___init__.py|__init__.py]]

## God Nodes (most connected - your core abstractions)
1. `EntryStatus` - 32 edges
2. `volunteer_factory()` - 30 edges
3. `$()` - 25 edges
4. `LogEntryListResponse` - 21 edges
5. `LogEntry` - 20 edges
6. `LogEntryCreate` - 20 edges
7. `LogEntryResponse` - 20 edges
8. `PhotoResponse` - 20 edges
9. `PhotoBase64Request` - 20 edges
10. `LogEntryUpdate` - 20 edges

## Surprising Connections (you probably didn't know these)
- `normalize_wa_phone()` --calls--> `normalize_phone()`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\schemas\manager.py → D:\Andrej\vsCode-workspace\BelPro\api\utils\phone.py
- `lifespan()` --calls--> `get_settings()`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\main.py → D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py
- `_notify_volunteer_email()` --calls--> `get_settings()`  [INFERRED]
  api\routers\log_entries.py → D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py
- `send_monthly_reports()` --calls--> `get_settings()`  [INFERRED]
  D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py → D:\Andrej\vsCode-workspace\BelPro\api\core\settings.py
- `Fields required to create a new log entry.` --uses--> `EntryStatus`  [INFERRED]
  api\schemas\log_entry.py → D:\Andrej\vsCode-workspace\BelPro\api\models\log_entry.py

## Communities

### Community 0 - "volunteer_factory()"
Cohesion: 0.05
Nodes (47): BaseSettings, auth(), client(), db_session(), engine(), log_entry_factory(), AsyncClient with get_db dependency wired to the test session., HTTP Basic Auth header for the seeded manager. (+39 more)

### Community 1 - "EntryStatus"
Cohesion: 0.15
Nodes (50): Base, BaseModel, approve_log_entry(), confirm_log_entry(), create_log_entry(), delete_log_entry(), delete_photo(), _extract_exif() (+42 more)

### Community 2 - "volunteers.js"
Cohesion: 0.14
Nodes (44): $(), applyFilters(), approvalsSortTh(), checkManagerSetup(), closeModal(), esc(), fmtDatetime(), fmtHours() (+36 more)

### Community 3 - "volunteer.py"
Cohesion: 0.06
Nodes (39): EmsoCheckRequest, EmsoCheckResponse, LogEntryBrief, _normalise_phone(), _normalise_phone_field(), Pydantic schemas for the Volunteer entity., Paginated volunteer list., Strip whitespace and leading ``+``, return bare E.164 digits. (+31 more)

### Community 4 - "normalize_phone()"
Cohesion: 0.07
Nodes (23): health(), lifespan(), Belpro FastAPI application entry point., Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null., Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null., Health check — returns ok when the service is up., seed_whatsapp_phone_from_env(), normalize_phone() (+15 more)

### Community 5 - "write_env_key()"
Cohesion: 0.08
Nodes (28): Update or append KEY=value in a .env file. Returns True on success, False on fai, write_env_key(), EvolutionClient, Async HTTP client for the Evolution API WhatsApp gateway., Return (normalized_phone, state) for the configured instance.          States: ", change_password(), create_manager(), get_config_info() (+20 more)

### Community 6 - "report_pdf.py"
Cohesion: 0.15
Nodes (21): _esc(), _fmt_date(), _generated_line(), _ngo_header_html(), NGOInfo, PDF rendering for monthly volunteer reports using WeasyPrint., Render an all-volunteer summary PDF and return raw bytes., NGO identity shown in every PDF header. (+13 more)

### Community 7 - "test_edit_path()"
Cohesion: 0.16
Nodes (21): make_response_payload(), make_text_payload(), poll_for_entry(), poll_for_entry_gone(), poll_for_entry_status(), post_to_webhook(), Poll until GET /api/log-entries/{entry_id} returns 404.     Raises TimeoutError, Build a WhatsApp text-message webhook body for the given bare-digit phone. (+13 more)

### Community 8 - "VolunteerUpdate"
Cohesion: 0.24
Nodes (13): Unit tests for VolunteerUpdate schema — no DB required., test_accepts_email_string(), test_accepts_first_name(), test_accepts_last_name(), test_accepts_none_email(), test_all_none_produces_empty_dump(), test_coerces_empty_email_to_none(), test_first_name_included_in_dump() (+5 more)

### Community 9 - "manager.py"
Cohesion: 0.15
Nodes (12): ConfigInfoResponse, ManagerCreate, ManagerResponse, ManagerUpdate, normalize_wa_phone(), PasswordChangeRequest, Pydantic schemas for the Manager entity., Fields required for first-time manager setup. (+4 more)

### Community 10 - "conftest.py"
Cohesion: 0.28
Nodes (8): api_client(), _auth_header(), _manager_password(), n8n_client(), Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable., Session-scoped AsyncClient against n8n. Skips all tests if unreachable., Creates a volunteer with a unique phone, yields the volunteer dict,     deletes, test_volunteer()

### Community 11 - "001_initial_schema.py"
Cohesion: 0.33
Nodes (5): downgrade(), Initial schema — baseline migration reflecting db/init.sql.  Revision ID: 001 Re, Drop all Belpro tables and the entry_status enum., Create the full Belpro schema from scratch (idempotent — safe to re-run)., upgrade()

### Community 12 - "004_log_entry_photos.py"
Cohesion: 0.33
Nodes (5): downgrade(), Create log_entry_photos table; drop single-photo columns from log_entries.  Revi, Create log_entry_photos; drop single-photo columns from log_entries., Drop log_entry_photos; restore single-photo columns on log_entries., upgrade()

### Community 13 - "005_report_prefs.py"
Cohesion: 0.33
Nodes (5): downgrade(), Add report channel preferences to managers and volunteers.  Revision ID: 005 Rev, Add report preference columns to managers and volunteers., Drop report preference columns from managers and volunteers., upgrade()

### Community 14 - "006_whatsapp_and_smtp_config.py"
Cohesion: 0.33
Nodes (5): downgrade(), Add WhatsApp bot number and SMTP config columns to managers.  Revision ID: 006 R, Add WhatsApp bot number and SMTP config columns to managers., Drop WhatsApp bot number and SMTP config columns from managers., upgrade()

### Community 15 - "007_add_ngo_davcna.py"
Cohesion: 0.33
Nodes (5): downgrade(), Add ngo_davcna column to managers.  Revision ID: 007 Revises: 006 Create Date: 2, Add ngo_davcna column to managers., Drop ngo_davcna column from managers., upgrade()

### Community 16 - "009_rename_entry_date_to_work_date.py"
Cohesion: 0.33
Nodes (5): downgrade(), Rename entry_date to work_date in log_entries.  'work_date' is clearer than 'ent, Rename entry_date to work_date and update index names., Reverse rename: work_date back to entry_date and restore index names., upgrade()

### Community 17 - "analytics_summary()"
Cohesion: 0.4
Nodes (5): analytics_summary(), _preceding_months(), Analytics router — aggregated summary for the dashboard analytics page., Return `count` consecutive (year, month) tuples ending at (year, month)., Return aggregated analytics data scoped to the given month.      Defaults to t

### Community 18 - "test_reports.py"
Cohesion: 0.4
Nodes (0): 

### Community 19 - "list_pending_entries.py"
Cohesion: 0.6
Nodes (4): _auth(), _get(), main(), Print pending_manager entries as JSON for the manual trigger node.  Usage:   pyt

### Community 20 - "002_add_emso_hash.py"
Cohesion: 0.5
Nodes (1): Add emso_hash column for EMŠO uniqueness enforcement.  Revision ID: 002 Revises:

### Community 21 - "008_add_manager_notified_at.py"
Cohesion: 0.5
Nodes (1): Add manager_notified_at column to log_entries.  Revision ID: 008 Revises: 007 Cr

### Community 22 - "test_health_returns_ok()"
Cohesion: 0.67
Nodes (2): Health endpoint must return 200 with status ok., test_health_returns_ok()

### Community 23 - "Normalize to WhatsApp-native digits-only format; reject unparseable values."
Cohesion: 1.0
Nodes (1): Normalize to WhatsApp-native digits-only format; reject unparseable values.

### Community 24 - "Normalise phone to bare E.164 digits, pass through None."
Cohesion: 1.0
Nodes (1): Normalise phone to bare E.164 digits, pass through None.

### Community 25 - "Treat empty string as absent — store None rather than ''."
Cohesion: 1.0
Nodes (1): Treat empty string as absent — store None rather than ''.

### Community 26 - "__init__.py"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "__init__.py"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "api.js"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "load_env.ps1"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "switch_manager_phone.ps1"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "export_wf.py"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "__init__.py"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "__init__.py"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **107 isolated node(s):** `Belpro FastAPI application entry point.`, `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`, `Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null.`, `Health check — returns ok when the service is up.`, `Application settings — loaded from environment variables / .env file.` (+102 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Normalize to WhatsApp-native digits-only format; reject unparseable values.`** (1 nodes): `Normalize to WhatsApp-native digits-only format; reject unparseable values.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Normalise phone to bare E.164 digits, pass through None.`** (1 nodes): `Normalise phone to bare E.164 digits, pass through None.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Treat empty string as absent — store None rather than ''.`** (1 nodes): `Treat empty string as absent — store None rather than ''.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `__init__.py`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `__init__.py`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `api.js`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `load_env.ps1`** (1 nodes): `load_env.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `switch_manager_phone.ps1`** (1 nodes): `switch_manager_phone.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `export_wf.py`** (1 nodes): `export_wf.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `__init__.py`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `__init__.py`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `volunteer_factory()` to `EntryStatus`, `normalize_phone()`, `report_pdf.py`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `EntryStatus` connect `EntryStatus` to `volunteer_factory()`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `EntryStatus` (e.g. with `Log entries CRUD router — volunteer work diary entries.` and `Best-effort email notification to volunteer after approve/reject.      Silentl`) actually correct?**
  _`EntryStatus` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `volunteer_factory()` (e.g. with `get_settings()` and `test_analytics_summary_counts_approved_hours()`) actually correct?**
  _`volunteer_factory()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `LogEntryListResponse` (e.g. with `Log entries CRUD router — volunteer work diary entries.` and `Best-effort email notification to volunteer after approve/reject.      Silentl`) actually correct?**
  _`LogEntryListResponse` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `LogEntry` (e.g. with `Log entries CRUD router — volunteer work diary entries.` and `Best-effort email notification to volunteer after approve/reject.      Silentl`) actually correct?**
  _`LogEntry` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Belpro FastAPI application entry point.`, `Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.`, `Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null.` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._