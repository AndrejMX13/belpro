# Test Coverage Gaps — Design Spec
**Date:** 2026-05-24  
**Status:** Approved

---

## Overview

Six coverage gaps were identified in the BelPro API test suite. All tests live in `api/tests/`. One new file is needed (`test_migrations.py`); the remaining five tests are added to existing files.

Backup/restore testing was considered and deferred to ISS-031 — it requires new non-interactive scripts designed for an ops container before testing is possible.

---

## Infrastructure

### Migration test database

The session-scoped `engine` fixture in `conftest.py` already runs `alembic upgrade head` once for the whole test session. A downgrade/upgrade roundtrip mid-session would temporarily break the schema and corrupt subsequent tests.

**Fix:** add a second isolated database.

- `db/init.sql` — add `CREATE DATABASE belpro_test_migrations;`
- `api/.env.test` — add `DATABASE_URL_MIGRATIONS=postgresql+asyncpg://belpro:belpro_dev_2025@postgres:5432/belpro_test_migrations`

### `_PHOTOS_ROOT` monkeypatching

`api/routers/log_entries.py` has a module-level constant `_PHOTOS_ROOT = Path("/app/photos")` (line 37). Photo upload tests that write files must monkeypatch this to `tmp_path` so they don't touch the real filesystem. The existing multipart upload test in `test_app_settings.py` does not do this — it needs a fix alongside the new base64 test.

Pattern (already used by `test_logo.py` and `test_report_history.py`):
```python
import api.routers.log_entries as le_mod
monkeypatch.setattr(le_mod, "_PHOTOS_ROOT", tmp_path / "photos")
```

---

## Six Tests

### 1. Migration roundtrip — `api/tests/test_migrations.py` (new file)

**Gap:** No test verifies that all Alembic migrations apply cleanly and are reversible.

**Fixture:** session-scoped, targets `belpro_test_migrations` via `DATABASE_URL_MIGRATIONS`. Runs:
1. `alembic stamp base` — reset revision tracking
2. `alembic upgrade head` — apply all migrations
3. `alembic downgrade -1` — reverse the latest migration
4. `alembic upgrade head` — reapply

All `subprocess.run` calls use `check=True` with `DATABASE_URL` env-var overridden to `DATABASE_URL_MIGRATIONS`. After the final `upgrade head`, assert the `alembic_version` table contains exactly one row (confirms head was reached cleanly).

---

### 2. EMŠO encryption round-trip — `api/tests/test_volunteers.py`

**Gap:** No test proves EMŠO is stored encrypted (not plaintext) and never exposed via the API.

**Test logic:**
1. Create a volunteer via `POST /api/volunteers` with a known EMŠO.
2. Query the raw `emso` column directly via `db_session` (bypassing the ORM model's decryption).
3. Assert the raw DB value is not equal to the plaintext EMŠO.
4. Assert `GET /api/volunteers/{id}` response body does not contain the plaintext EMŠO anywhere.

---

### 3. Status-flow enforcement — `api/tests/test_log_entries.py`

**Gap:** Approve and reject on a `pending_volunteer` entry are not tested; only `pending_manager` → `approved`/`rejected` transitions are covered.

**Two tests:**
- `test_approve_pending_volunteer_returns_409`: create entry with `status=EntryStatus.PENDING_VOLUNTEER`, call `POST /api/log-entries/{id}/approve`, assert 409.
- `test_reject_pending_volunteer_returns_409`: same but `POST /api/log-entries/{id}/reject`, assert 409.

---

### 4. Analytics edge cases — `api/tests/test_analytics.py`

**Gap:** No test verifies that only `approved` entries count toward monthly hours totals, and that an all-rejected month returns 0 rather than an error.

**Two tests:**

**a) Mixed-status month:**
- Create one volunteer, three entries in the same month: `approved` (3 h), `rejected` (2 h), `pending_manager` (1 h).
- Call `GET /api/analytics/summary?year=…&month=…`.
- Assert approved hours = 3, not 6. Assert volunteer appears once in the summary.

**b) All-rejected month:**
- Create one volunteer, one entry: `rejected` (2 h).
- Call the same endpoint for that month.
- Assert response is 200, approved hours = 0 (not an error or missing key).

---

### 5. Base64 photo limit + monkeypatch — `api/tests/test_app_settings.py`

**Gap:** The existing multipart limit test writes to real `/app/photos` (no monkeypatch) and the base64 endpoint has no limit test at all.

**Changes to `test_app_settings.py`:**
1. Add `monkeypatch` parameter to the existing `test_photo_upload_respects_db_max_photos_setting` test. Apply `monkeypatch.setattr(le_mod, "_PHOTOS_ROOT", tmp_path / "photos")` before the first upload call.
2. Add new test `test_photo_upload_base64_respects_db_max_photos_setting` that mirrors the existing test but uses `POST /api/log-entries/{id}/photos/base64` with a base64-encoded minimal JPEG payload.

Both tests patch `max_photos_per_entry` to 1 via `PATCH /api/admin/settings` before uploading.

---

### 6. Manager password change — `api/tests/test_managers.py`

**Gap:** No test covers the PATCH manager endpoint or verifies that the old password stops working after a change.

**Test logic:**
1. `PATCH /api/managers/me` with `{"password": "newpassword456"}` using existing `auth` header — assert 200.
2. Attempt login / authenticated request with the **old** password — assert 401.
3. Attempt login / authenticated request with the **new** password — assert 200.

The `auth` fixture provides HTTP Basic Auth for the seeded manager. After the patch, construct a new Basic Auth header with `newpassword456` and verify it works.

---

## File Summary

| File | Action | Tests added |
|------|--------|-------------|
| `db/init.sql` | add `CREATE DATABASE belpro_test_migrations;` | — |
| `api/.env.test` | add `DATABASE_URL_MIGRATIONS` line | — |
| `api/tests/test_migrations.py` | **new file** | migration roundtrip |
| `api/tests/test_volunteers.py` | add test | EMŠO encryption |
| `api/tests/test_log_entries.py` | add 2 tests | status-flow 409s |
| `api/tests/test_analytics.py` | add 2 tests | analytics edge cases |
| `api/tests/test_app_settings.py` | fix + add test | monkeypatch + base64 limit |
| `api/tests/test_managers.py` | add test | password change |

---

## Out of Scope

- Backup/restore testing → ISS-031 (requires new non-interactive ops scripts first)
- n8n workflow integration tests (separate concern)
- Frontend JS tests (no test infrastructure in place)
