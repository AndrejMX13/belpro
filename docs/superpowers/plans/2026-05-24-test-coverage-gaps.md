# Test Coverage Gaps — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add seven gap-filling tests to the BelPro API test suite covering migration integrity, EMŠO encryption, entry status enforcement, analytics accuracy, base64 photo upload limits, and manager password change.

**Architecture:** All tests live in `api/tests/`. Tests target existing, already-correct implementation — no new API code is written. One new file (`test_migrations.py`) is added; all others add to existing files. A second isolated test database (`belpro_test_migrations`) is introduced so the migration roundtrip test does not corrupt the main `belpro_test` session schema.

**Tech Stack:** pytest-asyncio, httpx AsyncClient, SQLAlchemy 2.x async, Alembic, PostgreSQL 18.3, Docker Compose

---

## File Summary

| File | Action | Purpose |
|------|--------|---------|
| `db/create_extra_dbs.sh` | Modify | Add `belpro_test_migrations` database |
| `api/.env.test` | Modify | Add `DATABASE_URL_MIGRATIONS` env var |
| `api/tests/test_migrations.py` | **Create** | Migration roundtrip test |
| `api/tests/test_volunteers.py` | Modify | EMŠO encryption round-trip test |
| `api/tests/test_log_entries.py` | Modify | Status-flow: approve/reject on `pending_volunteer` → 409 |
| `api/tests/test_analytics.py` | Modify | Analytics: rejected hours excluded; all-rejected month → 0 |
| `api/tests/test_app_settings.py` | Modify | Fix `_PHOTOS_ROOT` monkeypatch in existing multipart test; add base64 limit test |
| `api/tests/test_managers.py` | Modify | Manager password change: old creds → 401, new creds → 200 |

---

### Task 1: Infrastructure — migration test database

**Files:**
- Modify: `db/create_extra_dbs.sh`
- Modify: `api/.env.test`

- [ ] **Step 1: Add `belpro_test_migrations` to `db/create_extra_dbs.sh`**

The file currently creates only the `evolution` database. Add two lines inside the heredoc:

```bash
#!/usr/bin/env bash
# Runs at postgres container init time (before 01_schema.sql).
# Creates the 'evolution' database for Evolution API.
# The main 'belpro' database is created automatically via POSTGRES_DB.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE evolution;
    GRANT ALL PRIVILEGES ON DATABASE evolution TO $POSTGRES_USER;
    CREATE DATABASE belpro_test_migrations;
    GRANT ALL PRIVILEGES ON DATABASE belpro_test_migrations TO $POSTGRES_USER;
EOSQL
```

- [ ] **Step 2: Create the database in the running postgres container**

Init scripts only run on first container creation. Create the DB immediately in the running container without a volume wipe:

```bash
docker compose exec postgres psql -U belpro -c "CREATE DATABASE belpro_test_migrations;" -c "GRANT ALL PRIVILEGES ON DATABASE belpro_test_migrations TO belpro;"
```

Expected output:
```
CREATE DATABASE
GRANT
```

- [ ] **Step 3: Add `DATABASE_URL_MIGRATIONS` to `api/.env.test`**

Append this line to `api/.env.test`:

```
DATABASE_URL_MIGRATIONS=postgresql+asyncpg://belpro:belpro_dev_2025@postgres:5432/belpro_test_migrations
```

- [ ] **Step 4: Commit**

```bash
git add db/create_extra_dbs.sh api/.env.test
git commit -m "infra: add belpro_test_migrations DB for migration roundtrip tests"
```

---

### Task 2: Migration roundtrip test

**Files:**
- Create: `api/tests/test_migrations.py`

The session-scoped `engine` fixture in `conftest.py` already runs `alembic upgrade head` against `belpro_test`. A downgrade against that database mid-session would corrupt the schema for all subsequent tests. This test uses its own file-local fixture targeting `belpro_test_migrations` exclusively.

The `DATABASE_URL_MIGRATIONS` env var is available because `conftest.py` calls `load_dotenv` at import time (before any test runs).

- [ ] **Step 1: Create `api/tests/test_migrations.py`**

```python
"""Migration roundtrip test — runs against belpro_test_migrations (isolated DB)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

_API_DIR = str(Path(__file__).parent.parent)


@pytest_asyncio.fixture(scope="session")
async def migrations_engine():
    """Session-scoped engine targeting belpro_test_migrations."""
    url = os.environ["DATABASE_URL_MIGRATIONS"]
    eng = create_async_engine(url, poolclass=NullPool, echo=False)
    yield eng
    await eng.dispose()


async def test_migration_roundtrip(migrations_engine) -> None:
    """stamp base → upgrade head → downgrade -1 → upgrade head all exit 0."""
    migrations_url = os.environ["DATABASE_URL_MIGRATIONS"]
    env = {**os.environ, "DATABASE_URL": migrations_url}

    for args in [
        ["stamp", "base"],
        ["upgrade", "head"],
        ["downgrade", "-1"],
        ["upgrade", "head"],
    ]:
        subprocess.run(
            [sys.executable, "-m", "alembic"] + args,
            check=True,
            cwd=_API_DIR,
            env=env,
        )

    async with migrations_engine.connect() as conn:
        count = (
            await conn.execute(text("SELECT COUNT(*) FROM alembic_version"))
        ).scalar()
    assert count == 1
```

- [ ] **Step 2: Run the test inside the API container**

```bash
docker compose exec api pytest tests/test_migrations.py -v
```

Expected: `PASSED tests/test_migrations.py::test_migration_roundtrip`

- [ ] **Step 3: Commit**

```bash
git add api/tests/test_migrations.py
git commit -m "test: add Alembic migration roundtrip test on isolated DB"
```

---

### Task 3: EMŠO encryption round-trip

**Files:**
- Modify: `api/tests/test_volunteers.py`

Verifies two things: the raw `emso` column in Postgres is not the plaintext value (it is AES-256 ciphertext), and the API response for `GET /api/volunteers/{id}` does not expose the plaintext anywhere in its body.

- [ ] **Step 1: Append to `api/tests/test_volunteers.py`**

```python
async def test_emso_stored_encrypted(
    client: AsyncClient, auth: dict, db_session
) -> None:
    """EMŠO is stored encrypted in DB and never returned as plaintext by the API."""
    from sqlalchemy import text

    plaintext_emso = "0101990500006"
    payload = {
        "first_name": "Enc",
        "last_name": "Test",
        "street": "Testna 1",
        "postal_code": "1000",
        "city": "Ljubljana",
        "emso": plaintext_emso,
        "phone": "+38641777888",
    }
    r = await client.post("/api/volunteers", json=payload, headers=auth)
    assert r.status_code == 201
    vol_id = r.json()["id"]

    # Raw DB column must not equal the plaintext
    row = (
        await db_session.execute(
            text("SELECT emso FROM volunteers WHERE id = CAST(:id AS UUID)"),
            {"id": vol_id},
        )
    ).one()
    assert row.emso != plaintext_emso

    # API response must not contain the plaintext EMŠO anywhere
    r2 = await client.get(f"/api/volunteers/{vol_id}", headers=auth)
    assert r2.status_code == 200
    assert plaintext_emso not in r2.text
```

- [ ] **Step 2: Run the test**

```bash
docker compose exec api pytest tests/test_volunteers.py::test_emso_stored_encrypted -v
```

Expected: `PASSED`

- [ ] **Step 3: Commit**

```bash
git add api/tests/test_volunteers.py
git commit -m "test: verify EMSO is stored encrypted and not exposed by API"
```

---

### Task 4: Status-flow enforcement — `pending_volunteer` → 409

**Files:**
- Modify: `api/tests/test_log_entries.py`

The existing tests cover `approved` → approve → 409 and `pending_manager` → approve → 200. These two tests confirm the guard also blocks `pending_volunteer`.

The `log_entry_factory` defaults to `status=EntryStatus.PENDING_MANAGER`. Pass `status=EntryStatus.PENDING_VOLUNTEER` explicitly.

- [ ] **Step 1: Append to `api/tests/test_log_entries.py`**

```python
async def test_approve_pending_volunteer_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_VOLUNTEER)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_reject_pending_volunteer_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_VOLUNTEER)
    r = await client.patch(f"/api/log-entries/{e.id}/reject", headers=auth)
    assert r.status_code == 409
```

- [ ] **Step 2: Run the tests**

```bash
docker compose exec api pytest tests/test_log_entries.py::test_approve_pending_volunteer_returns_409 tests/test_log_entries.py::test_reject_pending_volunteer_returns_409 -v
```

Expected: both `PASSED`

- [ ] **Step 3: Commit**

```bash
git add api/tests/test_log_entries.py
git commit -m "test: assert approve/reject on pending_volunteer entry returns 409"
```

---

### Task 5: Analytics edge cases

**Files:**
- Modify: `api/tests/test_analytics.py`

The analytics router (`api/routers/analytics.py`) sums hours only for `APPROVED` entries. `entries_pending` counts `PENDING_MANAGER` (not `PENDING_VOLUNTEER`). The existing tests cover approved + pending_manager; these two tests add rejected entries to the mix and verify an all-rejected month doesn't error.

The file already imports `from decimal import Decimal`, `from datetime import date`, `from models.log_entry import EntryStatus` — no new imports needed.

- [ ] **Step 1: Append to `api/tests/test_analytics.py`**

```python
async def test_analytics_rejected_hours_excluded(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """Rejected entries don't contribute to total_hours; pending_manager entries don't either."""
    v = await volunteer_factory()
    await log_entry_factory(
        v.id, work_date=date(2026, 4, 10), hours=Decimal("3.0"),
        status=EntryStatus.APPROVED,
    )
    await log_entry_factory(
        v.id, work_date=date(2026, 4, 11), hours=Decimal("2.0"),
        status=EntryStatus.REJECTED,
    )
    await log_entry_factory(
        v.id, work_date=date(2026, 4, 12), hours=Decimal("1.0"),
        status=EntryStatus.PENDING_MANAGER,
    )
    r = await client.get("/api/analytics/summary?year=2026&month=4", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert float(data["total_hours"]) == 3.0
    assert data["entries_approved"] == 1
    assert data["entries_rejected"] == 1
    assert data["entries_pending"] == 1


async def test_analytics_all_rejected_returns_zero_hours(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """A month with only rejected entries returns total_hours=0, not an error."""
    v = await volunteer_factory()
    await log_entry_factory(
        v.id, work_date=date(2026, 5, 10), hours=Decimal("4.0"),
        status=EntryStatus.REJECTED,
    )
    r = await client.get("/api/analytics/summary?year=2026&month=5", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert float(data["total_hours"]) == 0.0
    assert data["entries_approved"] == 0
    assert data["entries_rejected"] == 1
```

- [ ] **Step 2: Run the tests**

```bash
docker compose exec api pytest tests/test_analytics.py::test_analytics_rejected_hours_excluded tests/test_analytics.py::test_analytics_all_rejected_returns_zero_hours -v
```

Expected: both `PASSED`

- [ ] **Step 3: Commit**

```bash
git add api/tests/test_analytics.py
git commit -m "test: verify rejected hours excluded and all-rejected month returns 0"
```

---

### Task 6: Base64 photo limit + `_PHOTOS_ROOT` monkeypatch

**Files:**
- Modify: `api/tests/test_app_settings.py`

Two changes in one task:

1. The existing `test_photo_upload_respects_db_max_photos_setting` writes files to the real `/app/photos` inside the container. Add `monkeypatch` + `tmp_path` and redirect `_PHOTOS_ROOT` (the module-level constant at line 37 of `api/routers/log_entries.py`) to a temp dir.
2. Add a mirror test for the base64 endpoint. The request body is `{"image_base64": "<base64 string>", "filename": "photo.jpg"}`. The limit is enforced identically to the multipart endpoint.

- [ ] **Step 1: Add `monkeypatch` and `tmp_path` to the existing multipart test**

In `api/tests/test_app_settings.py`, find `test_photo_upload_respects_db_max_photos_setting` and change its signature and add two lines at the top of the body:

**Before:**
```python
async def test_photo_upload_respects_db_max_photos_setting(
    client: AsyncClient,
    auth: dict,
    db_session,
    volunteer_factory,
    log_entry_factory,
) -> None:
    """upload_photo rejects a second photo when max_photos_per_entry is patched to 1 in DB."""
    import io
```

**After:**
```python
async def test_photo_upload_respects_db_max_photos_setting(
    client: AsyncClient,
    auth: dict,
    db_session,
    volunteer_factory,
    log_entry_factory,
    monkeypatch,
    tmp_path,
) -> None:
    """upload_photo rejects a second photo when max_photos_per_entry is patched to 1 in DB."""
    import io
    import api.routers.log_entries as le_mod
    monkeypatch.setattr(le_mod, "_PHOTOS_ROOT", tmp_path / "photos")
```

The rest of the test body is unchanged.

- [ ] **Step 2: Append the base64 limit test**

```python
async def test_photo_upload_base64_respects_db_max_photos_setting(
    client: AsyncClient,
    auth: dict,
    db_session,
    volunteer_factory,
    log_entry_factory,
    monkeypatch,
    tmp_path,
) -> None:
    """upload_photo_base64 rejects a second photo when max_photos_per_entry is 1 in DB."""
    import base64
    import api.routers.log_entries as le_mod

    monkeypatch.setattr(le_mod, "_PHOTOS_ROOT", tmp_path / "photos")

    r_patch = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 1}
    )
    assert r_patch.status_code == 200
    assert r_patch.json()["max_photos_per_entry"] == 1

    v = await volunteer_factory()
    e = await log_entry_factory(v.id)

    fake_image = b"\xff\xd8\xff\xe0" + b"\x00" * 100
    fake_b64 = base64.b64encode(fake_image).decode()

    r1 = await client.post(
        f"/api/log-entries/{e.id}/photos/base64",
        headers=auth,
        json={"image_base64": fake_b64, "filename": "photo1.jpg"},
    )
    assert r1.status_code == 201, f"First upload failed: {r1.text}"

    r2 = await client.post(
        f"/api/log-entries/{e.id}/photos/base64",
        headers=auth,
        json={"image_base64": fake_b64, "filename": "photo2.jpg"},
    )
    assert r2.status_code == 409, f"Expected 409 but got {r2.status_code}: {r2.text}"
    assert "1" in r2.json()["detail"]
```

- [ ] **Step 3: Run both photo limit tests**

```bash
docker compose exec api pytest tests/test_app_settings.py::test_photo_upload_respects_db_max_photos_setting tests/test_app_settings.py::test_photo_upload_base64_respects_db_max_photos_setting -v
```

Expected: both `PASSED`

- [ ] **Step 4: Commit**

```bash
git add api/tests/test_app_settings.py
git commit -m "test: monkeypatch _PHOTOS_ROOT in photo limit tests; add base64 endpoint coverage"
```

---

### Task 7: Manager password change

**Files:**
- Modify: `api/tests/test_managers.py`

The endpoint is `POST /api/managers/me/change-password` with body `{"current_password": str, "new_password": str (min 8 chars)}`. Returns 204 on success. The seeded manager has `password_hash = hash_password("testpass123")` (set in the session-scoped `engine` fixture). The `auth` fixture encodes `manager:testpass123` as HTTP Basic Auth.

After a successful change the `auth` header carries stale credentials — the next authenticated request must return 401. A freshly built header with the new password must return 200. The SAVEPOINT-based teardown rolls back the password change after the test, so other tests are unaffected.

- [ ] **Step 1: Append to `api/tests/test_managers.py`**

```python
@pytest.mark.asyncio
async def test_change_password_invalidates_old_credentials(
    client: AsyncClient, auth: dict
) -> None:
    """After a password change, old credentials return 401 and new ones return 200."""
    import base64

    r = await client.post(
        "/api/managers/me/change-password",
        headers=auth,
        json={"current_password": "testpass123", "new_password": "newpassword456"},
    )
    assert r.status_code == 204

    # Old credentials must now be rejected
    r2 = await client.get("/api/managers/me", headers=auth)
    assert r2.status_code == 401

    # New credentials must be accepted
    new_creds = base64.b64encode(b"manager:newpassword456").decode()
    r3 = await client.get(
        "/api/managers/me", headers={"Authorization": f"Basic {new_creds}"}
    )
    assert r3.status_code == 200
```

- [ ] **Step 2: Run the test**

```bash
docker compose exec api pytest tests/test_managers.py::test_change_password_invalidates_old_credentials -v
```

Expected: `PASSED`

- [ ] **Step 3: Run the full test suite to confirm no regressions**

```bash
docker compose exec api pytest tests/ -v --tb=short
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add api/tests/test_managers.py
git commit -m "test: verify password change invalidates old credentials"
```
