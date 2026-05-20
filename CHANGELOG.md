# Changelog

All notable changes to BelPro are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

---

## [0.11.0-beta.0] — 2026-05-20

### Added
- **ISS-004 — Error log:** `error_log` DB table (migration 013); `POST /api/errors` (internal `X-Internal-Key` auth) for background services to report failures; `GET /api/errors` with `?unacknowledged=true` filter; `PATCH /api/errors/{id}/acknowledge`; `GET /api/errors/unacknowledged-count` for the nav badge. 9 pytest tests. (`api/routers/errors.py`, `api/models/error_log.py`, `api/schemas/error_log.py`, `api/tests/test_errors.py`)
- **ISS-014 — Ops sidecar:** new `ops` Docker service (Alpine/Python, non-root `ops` user, internal crond) with automated DB + photo backup at 02:00 daily. Backup failures reported via `POST /api/errors`. Retention controlled by `BACKUP_RETENTION_DAYS` (default 30 days). (`ops/Dockerfile`, `ops/scripts/backup.sh`, `ops/crontab`)
- **ISS-007 — Photo cleanup:** nightly photo retention job at 03:00 in the ops sidecar. Deletes photos from disk and DB for approved entries past the `photo_retention_days` setting window. Failures reported via `POST /api/errors`. (`ops/scripts/photo_cleanup.py`)
- **ISS-012 — Health widget:** `GET /api/health/detailed` endpoint with per-service status (PostgreSQL response time, Whisper, n8n, WhatsApp connection state, disk free space, last heartbeat entry). Live health widget on the Administracija page refreshes every 30 s. (`api/main.py`, `frontend/js/errors.js`, `frontend/js/admin.js`)
- **Dnevnik napak page:** operational error log in the dashboard — lists errors from background services, defaults to unacknowledged-only, per-row Potrdi button. Nav badge on the link shows unacknowledged count, hidden when zero, refreshed every 60 s. (`frontend/js/errors.js`, `frontend/index.html`, `frontend/css/main.css`)
- **ISS-026 — Settings table:** `settings` DB table (migrations 007–012); `AppSettings` service with DB-first, env-fallback config authority; `GET/PATCH /api/admin/settings`; Administracija page for runtime-tunable settings (photo limit, photo retention, session duration) without a container restart. (`api/models/app_setting.py`, `api/services/app_settings.py`, `api/routers/admin.py`, `frontend/js/admin.js`, `api/tests/test_app_settings.py`)
- **ISS-015 — GDPR consent PDF:** `GET /api/documents/consent-pdf?volunteer_id=` generates and streams a volunteer agreement PDF ready to print and sign; Dokumenti tab on the volunteer detail page; optional `gdpr_additional_clauses` field on the manager record. (`api/services/consent_pdf.py`, `api/routers/documents.py`, `frontend/js/volunteers.js`)
- **ISS-027 — Photo confirmation fixes (n8n):** every photo upload now sends an individual "Sprejeto" confirmation; duplicate messages for multi-photo batches suppressed; limit-reached confirmation sent correctly on the final accepted photo.

### Changed
- Health widget moved from the volunteers (main) page to the Administracija page.
- `backups` Docker volume added; ops sidecar writes all backups to `/backups`.
- `PHOTO_RETENTION_DAYS` and `BACKUP_RETENTION_DAYS` added to `.env.example`.

### Fixed
- Logo re-fetched in `showApp()` to recover from `onerror` firing while `#app` was hidden during a container rebuild.
- Health widget `setInterval` stopped on every `route()` navigation to prevent duplicate polling timers accumulating across page changes.
- `pg_dump` exit code captured correctly in `backup.sh` (`|| PG_RC=$?` pattern) — previously `$?` was always `0` inside the `if !` block.

---

## [0.10.2-beta.0] — 2026-05-19

### Added
- ISS-024: `POST /api/reports/send-monthly` now persists each generated PDF to disk under
  `/app/photos/reports/{year}/{month:02d}/`. Resending the same month overwrites — one record
  per volunteer per month, one consolidated record per month.
- ISS-024: `GET /api/reports/history` — list persisted report records, filterable by year/month.
- ISS-024: `GET /api/reports/history/{id}/pdf` — stream a stored PDF; returns 404 if missing.
- ISS-024: "Arhiv poročil" collapsible section on the reports page — table of past reports with
  period, volunteer name, sent date, and download button.

### Changed
- Migration 010: two partial unique indexes on `monthly_reports` enforce one-row-per-period
  invariant at the DB level (handles nullable `volunteer_id` correctly with partial WHERE clauses).

---

## [0.10.1-beta.0] — 2026-05-19

### Added
- **ISS-005 — httpOnly cookie auth:** login/logout endpoints, secure session token helpers, `SESSION_DURATION_HOURS` and `COOKIE_SECURE` env vars. Dashboard replaces `sessionStorage` credential with a server-set httpOnly cookie. (`api/core/auth.py`, `api/routers/auth.py`, `frontend/js/api.js`)
- **ISS-016 — NGO logo:** upload/replace/delete via `POST`/`DELETE /api/logo`; logo displayed as thumbnail in "Podatki organizacije" settings card; embedded as base64 data URI in all monthly PDF reports; shown in the sidebar above the BelPro brand on every page. (`api/services/logo.py`, `api/routers/logo.py`, `api/services/report_pdf.py`, `frontend/js/volunteers.js`, `frontend/index.html`)
- Delete button for pending log entries — `DELETE /log-entries/{id}` now covers `pending_manager` state and cleans up associated photos from disk. (`api/routers/log_entries.py`)
- `MAX_PHOTOS_PER_ENTRY` env variable (default `5`) enforced at API level; per-entry photo limit also checked in the n8n volunteer entry workflow. `GET /api/log-entries/photo-limit` exposes the configured limit to the frontend. (`api/routers/log_entries.py`, `api/core/settings.py`)
- Slovenian tax number (davčna številka) Modulus 11 validation in manager settings. (`api/routers/managers.py`)
- EMŠO encryption key rotation: `scripts/rotate_emso_key.py` (Python) + `scripts/rotate_emso_key.sh` (bash wrapper) with automatic backup, DB re-encryption, and operator guidance. Procedure guide added to `docs/` and referenced from both READMEs.
- `scripts/upgrade.sh` — automated upgrade script: pre-flight checks, backup, `git pull`, Docker rebuild, Alembic migrations, health-check wait, summary. Procedure documented in both READMEs.
- ISS-025 added to `OPEN_ISSUES.md`: Emergency SMS notifications via local router SMS gateway (depends on ISS-014 ops sidecar).

### Changed
- Auth: `require_manager` now accepts both httpOnly cookie sessions and the legacy API key header (dual-auth), keeping the n8n/script integration path working without changes.
- Photo limit enforcement moved from n8n-only to API level; n8n workflow updated to read the limit from the API endpoint rather than a hardcoded value.

### Fixed
- Slovenian validation error messages now displayed in the frontend for API errors (previously raw JSON detail was shown).
- Rate limiting, CORS hardening, timezone audit, and stale env var cleanup across API and Docker Compose config.
- n8n volunteer entry workflow: correct cancel key (3→4); send confirm/cancel menu when photo limit is reached; include menu options in out-of-state photo reply; carry `mediaBody` through the photo-limit check.
- `upgrade.sh`: auto-detects git remote instead of hardcoding `origin`.
- EMŠO key rotation: `load_key()` now accepts both standard base64 and base64url-encoded keys.

---

## [0.10.0-beta.2] — 2026-05-16

### Added
- Slovenian translations of `README.md`, `SPEC.md`, `EVOLUTION_QR_TROUBLESHOOTING.md`, and `n8n/credentials/README.md` (`*_SL.md` parallel files with language switcher links).
- 7 specialist Claude Code skills added to `.claude/skills/`: `code-documenter`, `code-reviewer`, `database-optimizer`, `debugging-wizard`, `devops-engineer`, `secure-code-guardian`, `test-master`.

### Changed
- All Slovenian API error messages: previously English strings in `api/routers/volunteers.py`, `log_entries.py`, and `managers.py` translated to Slovenian.
- `python3` replaced with `python` across all host-side scripts and docs (`scripts/setup.sh`, `scripts/test_backup_restore.sh`, `scripts/switch_manager_phone.sh`, `scripts/gen_diagrams.py`, `scripts/gen_diagrams_sl.py`, `api/core/settings.py`, `EVOLUTION_QR_TROUBLESHOOTING.md`, `README.md`, `CLAUDE.md`).
- README installation order corrected: create Evolution API instance → configure and activate n8n workflows → scan WhatsApp QR. Previously n8n setup came after QR scan, meaning the first incoming message would hit inactive workflows.
- `SPEC.md` section 4.4: removed incorrect claim that transcript normalisation uses a Claude/OpenAI LLM node. Actual implementation uses pattern matching in a plain n8n code node.
- `SPEC.md` section 12: `load_env.sh` and `switch_manager_phone.sh` bash variants documented alongside their PowerShell equivalents.
- `.gitignore`: `n8n/credentials/` pattern changed from directory-level ignore to `n8n/credentials/*` to allow `!` exceptions for both `README.md` and `README_SL.md`.

---

## [0.10.0-beta.1] — 2026-05-15

### Added
- Monthly reports can now be delivered via WhatsApp in addition to email. Per-volunteer and manager delivery channels are controlled by the existing `report_email` / `report_whatsapp` preference flags. (`api/routers/reports.py`, `api/services/evolution.py`)
- "Pošlji poročila" button on the Reports page — triggers report delivery for the selected month directly from the dashboard without going through n8n. (`frontend/js/reports.js`, `frontend/js/api.js`)
- Photo EXIF metadata (GPS coordinates and timestamp) extracted and displayed in the log entry detail view when present in the uploaded photo. (`api/routers/log_entries.py`, `frontend/js/log_entry_detail.js`)
- EMŠO encryption unit tests: encrypt/decrypt roundtrip, nonce uniqueness, wrong-key rejection, hash determinism, and `mask_emso` boundary cases. (`api/tests/test_encryption.py`)
- Three additional report tests covering the `with_entries_only` filter: excludes volunteers with no entries, includes any-status entries (not only approved), and the `false` default case. (`api/tests/test_reports.py`)

### Changed
- All Docker Compose services now have healthchecks. Dependency conditions tightened throughout: `api` waits for `whisper` healthy (not just started), `frontend` waits for `api` healthy. `whisper` gets `start_period: 120s` to survive large-v3 model loading on cold boot. (`docker-compose.yml`)
- Consolidated summary PDF now excludes volunteers with zero approved entries for the selected month, both on manual export and on send. (`api/routers/reports.py`)

### Fixed
- Volunteer entries in per-volunteer PDFs sent via "Pošlji poročila" are now ordered by `work_date`. Previously order was undefined. (`api/routers/reports.py`)

---

## [0.9.7] — 2026-05-15

### Removed
- Email notification to volunteer on approve/reject. Since volunteers must have WhatsApp to participate in the workflow, the duplicate email adds no value. WhatsApp is now the sole notification channel for volunteers. (`api/routers/log_entries.py`)

### Fixed
- Hour parsing from Slovenian voice transcripts (`pet` through `dvanajst`): JavaScript `\w` is ASCII-only and silently failed to match words with diacritics (`šest`, `štiri`). Regex changed to `[^\s,.:!?]+`; diacritic variants (`šest`, `šestih`, `štiri`, `štirih`) added to the word dictionary; typo `stirib` corrected to `stirih`. Applies to three n8n Code nodes: `Code: Transcribe + Extract`, `Text Extract`, `Code: Procesiraj Popravek`.
- Hours declension in all volunteer and manager WhatsApp messages now follows Slovenian grammar: `1 ura`, `2 uri`, `3/4 ure`, `5+ ur`. Previously all messages showed `X ur` regardless of count.

---

## [0.9.6] — 2026-05-14

### Fixed
- Photo dedup: sending multiple photos in one WhatsApp message no longer sends multiple identical "Sprejeto" confirmation menus. The API now serializes concurrent uploads with `SELECT ... FOR UPDATE` and returns `photo_count`; the n8n workflow only sends the menu when `photo_count === 1`.

### Added
- `scripts/graphify/` — pipeline recovery scripts for when graphify subagents return results via notifications instead of writing chunk files to disk. Four scripts: `check_cache.py`, `merge_semantic.py`, `merge_ast_semantic.py`, `build_graph.py`.

---

## [0.9.5] — 2026-05-11

### Added
- `api/utils/phone.py`: `normalize_phone()` — strips `+`, spaces, dashes, parentheses; returns digits-only WhatsApp-native number or `None` for invalid input.
- `api/utils/env_writer.py`: `write_env_key()` — safely updates or appends a key in `.env`; non-fatal on failure (logs warning, returns bool).
- `api/services/evolution.py`: `EvolutionClient.get_connected_phone()` — queries `fetchInstances`, returns `(phone, state)` tuple; handles unreachable API, `@lid` JIDs, and both flat (v2.3.7) and nested (pre-v2.3) response formats.
- `api/schemas/manager.py`: `ConfigInfoResponse` — typed response for the settings config endpoint, including `wa_phone`, `wa_state`, `wa_synced`, `wa_env_write_ok`.
- Settings page: connection state badge ("Povezano"/"Odklopljeno"/etc.), read-only phone field when connected, auto-sync toast, `.env` write failure warning.
- `curl`, `wget`, `iputils-ping` added to `api/Dockerfile` and `whisper/Dockerfile` for in-container debugging.
- `docker-compose.yml`: `.env` bind-mounted into `api` container (`rw`) for `.env` write-back; `AUTHENTICATION_API_KEY` and `NGO_WHATSAPP_PHONE` env vars wired to `api` service.

### Changed
- `api/routers/managers.py`: `get_config_info` now queries Evolution API live on every settings page load; auto-syncs DB and `.env` when a different number is detected in "open" state.
- `api/routers/managers.py`: `update_manager` writes `NGO_WHATSAPP_PHONE` back to `.env` after a successful phone number change.
- `api/schemas/manager.py`: `ManagerUpdate.ngo_whatsapp_phone` normalised via `field_validator` (strips formatting, rejects too-short strings).
- `api/main.py`: `lifespan` seeds `ngo_whatsapp_phone` from `.env` into DB on first boot if DB value is null.
- Evolution API manager UI link corrected from `/manager/login` to `/manager`.

### Fixed
- `api/services/evolution.py`: Evolution API v2.3.7 `fetchInstances` returns flat objects (`name`, `connectionStatus`, `ownerJid`) — parser now handles both flat and legacy nested formats; previously always returned `wa_state: "close"`.

---

## [0.9.4] — 2026-05-10

### Added
- `tests/workflow/` — n8n workflow integration test suite (4 scenarios: happy-path confirm, edit, cancel, unknown volunteer). Tests post real WhatsApp payloads to the n8n webhook and assert DB state via the FastAPI API. No mocking — real Evolution, real PostgreSQL.
- `tests/workflow/conftest.py`: session-scoped `api_client`/`n8n_client` (httpx), function-scoped `test_volunteer` factory with direct-SQL teardown via `docker compose exec postgres psql`.
- `tests/workflow/helpers.py`: `make_text_payload`, `make_response_payload`, `post_to_webhook`, and three polling utilities (`poll_for_entry`, `poll_for_entry_status`, `poll_for_entry_gone`).
- Root-level `pyproject.toml` with `asyncio_mode = auto` and session event-loop scope for pytest-asyncio.

### Changed
- `api/main.py`: version string extracted to `__version__ = "0.9.4"` module constant; `FastAPI(version=__version__)` now references it instead of a bare literal.

---

## [0.9.3] — 2026-05-10

### Added
- Inline editing of `first_name`, `last_name`, `phone`, and `email` on the volunteer detail page. Each field group has its own pencil toggle with Save/Cancel — no modal, no page reload, in-place DOM update on success.
- `api/tests/test_volunteer_update_schema.py`: 10 unit tests for the extended `VolunteerUpdate` schema (no DB required).

### Changed
- `VolunteerUpdate` schema now accepts `first_name`, `last_name`, and `email` in addition to the existing `phone` and report-preference fields. Email is stored as a plain string (no format validation); an empty string is coerced to `null`.

### Fixed
- `PATCH /volunteers/{id}` now returns HTTP 409 with a Slovenian error message when a duplicate phone number is submitted (previously caused an unhandled 500).

---

## [0.9.2] — 2026-05-09

### Added
- Full automated test suite: 57 pytest tests covering all API endpoints (health, managers, volunteers, log entries, reports, analytics). Real PostgreSQL only — no mocks.
- `api/tests/conftest.py`: session-scoped engine fixture (Alembic migrations on `belpro_test`), function-scoped SAVEPOINT isolation, `AsyncClient` with dependency override, `volunteer_factory` and `log_entry_factory` helpers.
- `scripts/test_backup_restore.sh`: standalone smoke test for backup/restore cycle (seeds data → backup → drop DB → restore → verify).
- `api/requirements-test.txt` and `api/pyproject.toml` with pytest configuration.
- `api/.env.test` (gitignored) for test database URL and secrets.

### Changed
- All 9 Alembic migrations made idempotent (`IF NOT EXISTS` guards throughout) so the test session can run `stamp base → upgrade head` against a database that already has schema from `init.sql`.

### Fixed
- Version drift: `main.py` had been stuck at `0.8.2` since before the 0.9.x work; corrected to `0.9.2`.

---

## [0.9.1] — 2026-05-09

### Added
- `work_date` (dan opravljenega dela) is now editable in the entry detail form — blocked for approved entries.
- "Dodaj vnos" button on the volunteer detail page: managers can create log entries directly from the dashboard (starts as `pending_manager`, no volunteer confirmation step).
- Two-column date display in approvals list and volunteer log list: "Dan opravljenega dela" (`work_date`) and "Dan vnosa" (`created_at`), both sortable.
- `location` field added to the log entry edit form; changes are saved and the detail view refreshes immediately.
- Alembic migration 009: `entry_date` → `work_date` rename with index renames, fully reversible via `downgrade()`.
- Date range filter in both log lists now has a `Dan vnosa` toggle checkbox — unchecked filters by `Datum dela` (default), checked filters by submission date.

### Changed
- Renamed `entry_date` → `work_date` throughout the stack (DB column, ORM model, Pydantic schemas, all routers, PDF service, n8n workflows, frontend JS, scripts, `init.sql`, `SPEC.md`) to clearly separate "when work was performed" from `created_at` (submission timestamp).
- Docker base images (`python:3.11-slim`, `redis:7-alpine`, `nginx:alpine`) pinned to exact digests for reproducible builds.

### Fixed
- `LogEntryBrief` schema in volunteer detail response was missing the `work_date` field rename, causing serialisation failures on the volunteer detail page.
- Downgrade operations in migration 009 reordered: column rename now happens before index renames to avoid inconsistent state on partial failure.
- `Datum dela` was missing as a labeled field in the log entry detail info grid (was only shown as the unlabeled page header).
- Date column header label shortened to `Datum dela` across all lists and forms (was `Dan opravljenega dela`).
- After creating a new entry from the volunteer detail page, navigation now returns to the volunteer detail page instead of opening the new entry detail.
- All dates now displayed in `yyyy-mm-dd` format consistently throughout the dashboard.

---

## [0.8.2] — 2026-05-08

### Removed
- 13 one-off workflow patching and deployment scripts used during early development.

## [0.8.1] — 2026-05-08

### Added
- Full WhatsApp volunteer entry flow: voice transcription → volunteer confirmation (Potrdi/Popravi/Prekliči) → manager approval via WhatsApp → email notification.
- Manager detection and routing in `volunteer_entry` workflow.
- Manager approval workflow (`manager_approval`) — WhatsApp Approve/Reject buttons.
- Test script to switch a phone number between manager and volunteer roles.
- Design spec and implementation plan for manager WhatsApp approval.

### Changed
- Updated initial database creation SQL script.
- Nginx configuration updated to prevent IP loss when API container restarts.
- Evolution API documentation updated for environment variables and API keys.
- Setup wizard updated to reflect Evolution API changes.
- Minor fixes to SPEC.md.

### Fixed
- Edit entry flow in `volunteer_entry` workflow — volunteer can now re-submit corrected entries.
- Link from Execute Workflow node to `manager_approval` workflow.
- Chrome mobile menu not working.
- Evolution API QR generation issues (see `EVOLUTION_QR_TROUBLESHOOTING.md`).

## [0.6.1] — 2026-05-04

### Added
- NGO WhatsApp number and SMTP configuration to settings.
- Analytics page with monthly analytics.
- BelPro branding fixes.
- Email service and monthly reports endpoint.
- n8n `monthly_reports` workflow.
- Approve/reject email notifications.
- `backup.sh` and `restore.sh` scripts.
- Setup wizard (`setup.sh`) for guided installation.

## [0.5.1] — 2026-05-04

### Added
- Checkboxes for monthly report preferences (manager, volunteer, global defaults).
- "Test entry" workflow documentation for testing with multiple phone numbers.

### Changed
- SPEC.md updated to reflect current code state.

## [0.4.1] — 2026-05-03

### Added
- PDF report generation (HTML→PDF via WeasyPrint) — monthly reports export.
- Reports ("Poročila") page in the dashboard.
- Dynamic back links in the UI.
- Architecture documents.

### Changed
- Cleaned Slovenian translations.
- Menu item renamed from "Odobritve" to "Dnevniki" for clarity.

### Fixed
- Nginx upload limit to allow photo uploads.
- File permissions for photo uploads.
- Removed unused environment variable references.

## [0.4.0 and earlier] — 2026-05-01 to 2026-05-03

### Added
- Project scaffold: Docker Compose services, PostgreSQL schema, FastAPI skeleton.
- Manager dashboard: login, manager record creation, volunteer management (add, search, duplicate detection, delete).
- Volunteer list with filtering, searching, sorting, re-activation.
- Log entries backend (API) and frontend (dashboard approval, lists, volunteer log list).
- Log entry detail page with photo display.
- Settings page: manager/NGO data editing and password change.
- Graphify knowledge graph tooling.
- Search and date range filtering on volunteer log list.
- MIT License and README.

---

## Changelog maintenance

To update the changelog when cutting a new release:

```bash
# Get all commits since the last version tag
git log v0.8.1..HEAD --oneline
```

Then categorize the commits under the appropriate headings and add a new section.
