# Changelog

All notable changes to BelPro are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

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
