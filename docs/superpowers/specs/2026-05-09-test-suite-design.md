# Test Suite Design — BelPro API

**Date:** 2026-05-09  
**Status:** Approved  
**Scope:** FastAPI backend + backup/restore smoke test. n8n workflows excluded (structural changes pending).

---

## Goals

Provide a regression safety net that catches breaking changes across all API endpoints. Not aiming for deep behavioural coverage yet — broad first, deep later. No mocks, ever.

---

## Constraints

- Real PostgreSQL database only. No mocks, no stubs of the DB layer.
- Tests run from WSL2 host against a dedicated `belpro_test` database on the existing Postgres container.
- n8n workflow tests are explicitly out of scope until workflow structure stabilises.
- EMŠO encryption correctness is not a current priority; basic happy/sad paths are sufficient.

---

## Infrastructure

### Test database

A second database `belpro_test` created on the existing `postgres` Docker container. No new container, no new service. The test DB is reachable at `localhost:5432/belpro_test` from WSL2 (the port is already exposed).

A `DATABASE_TEST_URL` environment variable (or a `.env.test` file) points pytest at the test DB. Production `DATABASE_URL` is never touched by tests.

### pytest configuration

`pyproject.toml` in `api/` configures:
- `asyncio_mode = "auto"` (pytest-asyncio)
- `testpaths = ["tests"]`
- `env` loading from `.env.test`

Dependencies added to a `requirements-test.txt` (not mixed into `requirements.txt`):
- `pytest`
- `pytest-asyncio`
- `pytest-env`
- `httpx`

---

## Fixture Architecture

### Session-scoped (once per `pytest` run)

1. Create the `belpro_test` database if it does not exist.
2. Run `alembic upgrade head` against `belpro_test` — schema is always up to date.
3. Insert one `Manager` row (username + hashed password) used for authenticated requests.
4. Yield the `AsyncEngine`.
5. On teardown: drop all tables (leaves the DB ready for the next run without re-running migrations from scratch).

### Function-scoped (once per test)

Each test gets:
- A `SAVEPOINT` (SQLAlchemy nested transaction). All writes made during the test are rolled back on teardown — no data leaks between tests.
- An `AsyncClient` wrapping the FastAPI `app`, with the DB session dependency overridden to use the test transaction's connection. The app sees a real session; writes just never commit to the actual DB.
- HTTP Basic Auth headers pre-built from the seeded manager credentials, available as an `auth_headers` fixture.

### Data factories

Direct DB inserts — not HTTP calls, not mocks. Factories are plain async functions called from test fixtures:

- `volunteer_factory(**overrides)` — inserts a `Volunteer` row, returns the ORM instance.
- `log_entry_factory(volunteer, **overrides)` — inserts a `LogEntry` row linked to a volunteer.

Factories accept keyword overrides so individual tests can customise fields without boilerplate.

---

## Test Files

All under `api/tests/`.

### `test_health.py`
- `GET /api/health` returns `{"status": "ok"}` and HTTP 200.

### `test_managers.py`
- `POST /api/managers` — attempting to create a second manager is rejected (single-manager constraint).
- Auth: valid credentials accepted, wrong password returns 401, missing credentials returns 401.

### `test_volunteers.py`
- `GET /api/volunteers` — empty list; list with one entry; pagination/sorting where applicable.
- `POST /api/volunteers` — success; duplicate EMŠO rejected; missing required fields return 422.
- `GET /api/volunteers/{id}` — found; 404 on unknown ID.
- `PUT /api/volunteers/{id}` — update fields; 404 on unknown ID.
- `POST /api/volunteers/{id}/deactivate` — deactivates active volunteer; 404 on unknown ID.
- `POST /api/volunteers/{id}/activate` — reactivates deactivated volunteer.
- `DELETE /api/volunteers/{id}` — deletes volunteer; 404 on unknown ID.

### `test_log_entries.py`
- `GET /api/log-entries` — empty; filtered by volunteer; filtered by status.
- `POST /api/log-entries` — success; missing required fields return 422.
- `GET /api/log-entries/{id}` — found; 404 on unknown ID.
- `PUT /api/log-entries/{id}` — update editable fields; 404 on unknown ID.
- `POST /api/log-entries/{id}/approve` — approves a `pending_manager` entry; wrong status returns error.
- `POST /api/log-entries/{id}/reject` — rejects a `pending_manager` entry; wrong status returns error.
- `POST /api/log-entries/{id}/confirm` — volunteer confirms a `pending_volunteer` entry.
- `DELETE /api/log-entries/{id}` — deletes entry; 404 on unknown ID.
- Photo: `POST /api/log-entries/{id}/photo` — upload accepted file; unsupported extension rejected.
- Photo: `DELETE /api/log-entries/{id}/photo/{photo_id}` — success; 404 on unknown photo.
- **Status machine:** entry cannot move from `approved` back to `pending_manager` or `pending_volunteer`. Covered by attempting invalid transitions and asserting the appropriate error response.

### `test_reports.py`
- `POST /api/reports/generate` — triggers generation; returns report metadata.
- `GET /api/reports` — list reports.
- `GET /api/reports/{id}` — found; 404 on unknown ID.
- `GET /api/reports/{id}/pdf` — returns a PDF (`application/pdf` content type); 404 on unknown ID.

### `test_analytics.py`
- Summary endpoint(s) — return 200 with expected shape; no assertion on exact counts (varies by seed data), just that required keys are present.

---

## Backup / Restore Smoke Test

A standalone shell script `scripts/test_backup_restore.sh`. Not part of the default `pytest` run. Run manually or as a separate CI step.

### Sequence

1. Confirm `belpro` stack is running (`docker compose ps`).
2. Seed known data via the API: one volunteer + one approved log entry.
3. Run `scripts/backup.sh` → capture the snapshot file path.
4. Drop the `belpro` database.
5. Re-run `db/init.sql` to recreate an empty schema.
6. Run `scripts/restore.sh <snapshot>`.
7. Query `GET /api/volunteers` and `GET /api/log-entries` — assert the seeded records are present.
8. Clean up: delete the snapshot file, remove the seeded test records (or re-drop and re-init).

### Pass criteria

The volunteer and log entry inserted in step 2 are returned by the API in step 7 with matching IDs and field values.

---

## What is NOT covered (yet)

- Deep encryption correctness tests (low priority for now).
- n8n workflow tests (structural changes pending).
- PDF content validation (only content-type is checked).
- WhatsApp integration paths.
- Multi-volunteer concurrency.
- Performance / load testing.
