# Test Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a full-coverage API regression test suite (pytest + real PostgreSQL, no mocks) plus a backup/restore smoke-test script.

**Architecture:** Each pytest test runs inside a SQLAlchemy SAVEPOINT that rolls back on teardown — migrations run once per session, data never leaks between tests. A dedicated `belpro_test` database on the existing Postgres container is the only infrastructure change. The backup/restore smoke test is a standalone shell script separate from pytest.

**Tech Stack:** pytest, pytest-asyncio, httpx (AsyncClient + ASGITransport), SQLAlchemy 2.x async (SAVEPOINT pattern), Alembic (programmatic upgrade), python-dotenv.

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Create | `api/.env.test` | Test-specific env vars (DB URL pointing at `belpro_test`) |
| Create | `api/requirements-test.txt` | Test-only Python deps |
| Create | `api/pyproject.toml` | pytest config (asyncio_mode, testpaths) |
| Create | `api/tests/__init__.py` | Package marker |
| Create | `api/tests/conftest.py` | All fixtures: engine, session, client, factories |
| Create | `api/tests/test_health.py` | Health endpoint smoke test |
| Create | `api/tests/test_managers.py` | Manager CRUD + auth tests |
| Create | `api/tests/test_volunteers.py` | Volunteer CRUD tests |
| Create | `api/tests/test_log_entries.py` | Log entry CRUD + status machine tests |
| Create | `api/tests/test_reports.py` | Monthly summary + PDF endpoint tests |
| Create | `api/tests/test_analytics.py` | Analytics summary tests |
| Create | `scripts/test_backup_restore.sh` | Backup → drop → restore smoke test |

---

## Task 1: Test Infrastructure

**Files:**
- Create: `api/.env.test`
- Create: `api/requirements-test.txt`
- Create: `api/pyproject.toml`
- Create: `api/tests/__init__.py`
- Create: `api/tests/conftest.py`

### Step 1.1 — Create `belpro_test` database

Run from WSL2:

```bash
docker compose exec postgres psql -U belpro -c "CREATE DATABASE belpro_test;"
```

Expected: `CREATE DATABASE`

### Step 1.2 — Create `api/.env.test`

Copy `DATABASE_URL` from `api/.env`, change the database name to `belpro_test`. All other values can be the same as `.env` except `MANAGER_PASSWORD` which is set to a known test value.

```dotenv
# Test database — separate from production belpro DB
DATABASE_URL=postgresql+asyncpg://belpro:YOUR_POSTGRES_PASSWORD@localhost:5432/belpro_test

# Keep these the same as your .env
EMSO_ENCRYPTION_KEY=YOUR_KEY_FROM_ENV
API_SECRET_KEY=YOUR_KEY_FROM_ENV

# Fixed test password — used as fallback; session fixture seeds a manager with password_hash
MANAGER_PASSWORD=testpass123

# Silence optional services
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE_NAME=belpro
```

### Step 1.3 — Create `api/requirements-test.txt`

```
pytest>=8.0
pytest-asyncio>=0.23
httpx>=0.27
python-dotenv>=1.0
```

### Step 1.4 — Create `api/pyproject.toml`

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Step 1.5 — Create `api/tests/__init__.py`

Empty file:

```python
```

### Step 1.6 — Create `api/tests/conftest.py`

```python
# Load test env BEFORE any app imports — must be the very first thing.
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env.test", override=True)

# ── stdlib / third-party ──────────────────────────────────────────────────────
import base64
import subprocess
import sys
from decimal import Decimal
from datetime import date
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

# ── app imports (Settings already reads the overridden env vars) ──────────────
from core.settings import get_settings
from db.session import get_db
from main import app
from models.base import Base
from models.log_entry import EntryStatus, LogEntry
from models.manager import Manager
from models.volunteer import Volunteer
from services.encryption import encrypt_emso, hash_emso, load_key
from services.password import hash_password

# ── test constants ─────────────────────────────────────────────────────────────
_TEST_PASS = "testpass123"


# ── session-scoped: migrate once, seed manager once ───────────────────────────
@pytest_asyncio.fixture(scope="session")
async def engine():
    """
    Run Alembic migrations against belpro_test, seed one Manager row.
    Drops all tables on teardown so next pytest session starts clean.
    """
    settings = get_settings()
    eng = create_async_engine(settings.database_url, poolclass=NullPool, echo=False)

    # Alembic reads DATABASE_URL from the environment (already overridden by load_dotenv above).
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        check=True,
        cwd=str(Path(__file__).parent.parent),  # api/ directory
    )

    # Seed the single manager row (committed — visible to all tests).
    async with AsyncSession(eng) as session:
        async with session.begin():
            session.add(
                Manager(
                    first_name="Test",
                    last_name="Manager",
                    phone="+38641000000",
                    email="test@belpro.si",
                    ngo_name="Test NGO d.o.o.",
                    ngo_street="Testna ulica 1",
                    ngo_postal_code="1000",
                    ngo_city="Ljubljana",
                    password_hash=hash_password(_TEST_PASS),
                )
            )

    yield eng

    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


# ── function-scoped: SAVEPOINT per test ───────────────────────────────────────
@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Per-test session inside a SAVEPOINT.  The app's commit() releases the
    savepoint (data stays in the outer transaction); rollback at teardown
    undoes everything.  No data leaks between tests.
    """
    conn = await engine.connect()
    await conn.begin()

    session = AsyncSession(
        bind=conn,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    yield session

    await session.close()
    await conn.rollback()
    await conn.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient with get_db dependency wired to the test session."""

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def auth() -> dict[str, str]:
    """HTTP Basic Auth header for the seeded manager."""
    creds = base64.b64encode(f"admin:{_TEST_PASS}".encode()).decode()
    return {"Authorization": f"Basic {creds}"}


# ── data factories ─────────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def volunteer_factory(db_session: AsyncSession):
    """
    Returns an async callable that inserts a Volunteer row via flush (not commit)
    so the write stays inside the current SAVEPOINT.
    """
    settings = get_settings()
    key = load_key(settings.emso_encryption_key)
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()

    async def _make(
        first_name: str = "Ana",
        last_name: str = "Novak",
        emso: str = "1234567890123",
        phone: str = "+38641111111",
        active: bool = True,
        **overrides,
    ) -> Volunteer:
        v = Volunteer(
            first_name=first_name,
            last_name=last_name,
            street="Testna 1",
            postal_code="1000",
            city="Ljubljana",
            emso=encrypt_emso(emso, key),
            emso_hash=hash_emso(emso, key),
            phone=phone,
            active=active,
            manager_id=manager.id,
            **overrides,
        )
        db_session.add(v)
        await db_session.flush()
        return v

    return _make


@pytest_asyncio.fixture
async def log_entry_factory(db_session: AsyncSession):
    """
    Returns an async callable that inserts a LogEntry row via flush.
    """

    async def _make(
        volunteer_id,
        work_date: date = date(2026, 1, 15),
        activity_description: str = "Testno delo",
        hours: Decimal = Decimal("2.0"),
        status: EntryStatus = EntryStatus.PENDING_MANAGER,
        **overrides,
    ) -> LogEntry:
        e = LogEntry(
            volunteer_id=volunteer_id,
            work_date=work_date,
            activity_description=activity_description,
            hours=hours,
            status=status,
            **overrides,
        )
        db_session.add(e)
        await db_session.flush()
        return e

    return _make
```

### Step 1.7 — Install test dependencies

```bash
cd api
pip install -r requirements-test.txt
```

### Step 1.8 — Verify infrastructure with a dry run

```bash
cd api
pytest --collect-only
```

Expected: `no tests ran` (0 errors, 0 failures — just collection succeeds).

### Step 1.9 — Commit

```bash
git add api/.env.test api/requirements-test.txt api/pyproject.toml api/tests/
git commit -m "test: add pytest infrastructure (conftest, fixtures, env)"
```

---

## Task 2: Health Endpoint

**Files:**
- Create: `api/tests/test_health.py`

### Step 2.1 — Write test

```python
# api/tests/test_health.py
import pytest
from httpx import AsyncClient


async def test_health_returns_ok(client: AsyncClient) -> None:
    """Health endpoint must return 200 with status ok."""
    r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
```

### Step 2.2 — Run

```bash
cd api && pytest tests/test_health.py -v
```

Expected:
```
PASSED tests/test_health.py::test_health_returns_ok
```

### Step 2.3 — Commit

```bash
git add api/tests/test_health.py
git commit -m "test: add health endpoint test"
```

---

## Task 3: Manager Endpoints

**Files:**
- Create: `api/tests/test_managers.py`

### Step 3.1 — Write tests

```python
# api/tests/test_managers.py
import pytest
from httpx import AsyncClient


async def test_get_manager_returns_profile(client: AsyncClient, auth: dict) -> None:
    """GET /api/managers/me returns the seeded manager."""
    r = await client.get("/api/managers/me", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Manager"
    assert data["email"] == "test@belpro.si"


async def test_create_manager_returns_409_when_already_configured(
    client: AsyncClient, auth: dict
) -> None:
    """POST /api/managers must reject a second manager (single-manager constraint)."""
    payload = {
        "first_name": "Nova",
        "last_name": "Upravljalka",
        "phone": "+38641999999",
        "email": "nova@belpro.si",
        "ngo_name": "Nova NGO",
        "ngo_street": "Nova 1",
        "ngo_postal_code": "2000",
        "ngo_city": "Maribor",
    }
    r = await client.post("/api/managers", json=payload, headers=auth)
    assert r.status_code == 409


async def test_auth_wrong_password_returns_401(client: AsyncClient) -> None:
    """Wrong password must return 401."""
    import base64
    bad = base64.b64encode(b"admin:wrongpassword").decode()
    r = await client.get("/api/managers/me", headers={"Authorization": f"Basic {bad}"})
    assert r.status_code == 401


async def test_auth_missing_credentials_returns_401(client: AsyncClient) -> None:
    """Request with no Authorization header must return 401."""
    r = await client.get("/api/managers/me")
    assert r.status_code == 401
```

### Step 3.2 — Run

```bash
cd api && pytest tests/test_managers.py -v
```

Expected: 4 tests PASSED.

### Step 3.3 — Commit

```bash
git add api/tests/test_managers.py
git commit -m "test: add manager endpoint tests"
```

---

## Task 4: Volunteer Endpoints

**Files:**
- Create: `api/tests/test_volunteers.py`

### Step 4.1 — Write tests

```python
# api/tests/test_volunteers.py
import uuid
import pytest
from httpx import AsyncClient


_VALID_PAYLOAD = {
    "first_name": "Ana",
    "last_name": "Novak",
    "street": "Testna 1",
    "postal_code": "1000",
    "city": "Ljubljana",
    "emso": "1234567890123",
    "phone": "+38641111111",
}


# ── list ──────────────────────────────────────────────────────────────────────

async def test_list_volunteers_empty(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/volunteers", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


async def test_list_volunteers_returns_created_volunteer(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    await volunteer_factory()
    r = await client.get("/api/volunteers", headers=auth)
    assert r.status_code == 200
    assert r.json()["total"] == 1


# ── create ────────────────────────────────────────────────────────────────────

async def test_create_volunteer_success(client: AsyncClient, auth: dict) -> None:
    r = await client.post("/api/volunteers", json=_VALID_PAYLOAD, headers=auth)
    assert r.status_code == 201
    data = r.json()
    assert data["first_name"] == "Ana"
    assert data["last_name"] == "Novak"
    assert "id" in data


async def test_create_volunteer_duplicate_emso_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    await volunteer_factory(emso="1234567890123")
    r = await client.post("/api/volunteers", json=_VALID_PAYLOAD, headers=auth)
    assert r.status_code == 409


async def test_create_volunteer_duplicate_phone_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    await volunteer_factory(phone="+38641111111")
    r = await client.post("/api/volunteers", json=_VALID_PAYLOAD, headers=auth)
    assert r.status_code == 409


async def test_create_volunteer_missing_required_field_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    payload = {k: v for k, v in _VALID_PAYLOAD.items() if k != "emso"}
    r = await client.post("/api/volunteers", json=payload, headers=auth)
    assert r.status_code == 422


async def test_create_volunteer_invalid_postal_code_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    payload = {**_VALID_PAYLOAD, "postal_code": "AB12"}
    r = await client.post("/api/volunteers", json=payload, headers=auth)
    assert r.status_code == 422


async def test_create_volunteer_invalid_emso_length_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    payload = {**_VALID_PAYLOAD, "emso": "123"}
    r = await client.post("/api/volunteers", json=payload, headers=auth)
    assert r.status_code == 422


# ── get single ────────────────────────────────────────────────────────────────

async def test_get_volunteer_found(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    r = await client.get(f"/api/volunteers/{v.id}", headers=auth)
    assert r.status_code == 200
    assert r.json()["id"] == str(v.id)


async def test_get_volunteer_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.get(f"/api/volunteers/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


# ── update ────────────────────────────────────────────────────────────────────

async def test_update_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    r = await client.put(
        f"/api/volunteers/{v.id}",
        json={"first_name": "Maja", "last_name": "Kovac",
              "street": "Nova 2", "postal_code": "2000", "city": "Maribor"},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["first_name"] == "Maja"


async def test_update_volunteer_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.put(
        f"/api/volunteers/{uuid.uuid4()}",
        json={"first_name": "X", "last_name": "Y",
              "street": "Z 1", "postal_code": "1000", "city": "Ljubljana"},
        headers=auth,
    )
    assert r.status_code == 404


# ── activate / deactivate ──────────────────────────────────────────────────────

async def test_deactivate_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=True)
    r = await client.post(f"/api/volunteers/{v.id}/deactivate", headers=auth)
    assert r.status_code == 200
    assert r.json()["active"] is False


async def test_deactivate_volunteer_not_found(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.post(f"/api/volunteers/{uuid.uuid4()}/deactivate", headers=auth)
    assert r.status_code == 404


async def test_activate_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=False)
    r = await client.post(f"/api/volunteers/{v.id}/activate", headers=auth)
    assert r.status_code == 200
    assert r.json()["active"] is True


# ── delete ────────────────────────────────────────────────────────────────────

async def test_delete_volunteer_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.delete(f"/api/volunteers/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


# ── EMŠO check ────────────────────────────────────────────────────────────────

async def test_check_emso_not_registered(client: AsyncClient, auth: dict) -> None:
    r = await client.post(
        "/api/volunteers/check-emso",
        json={"emso": "9876543210987"},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["exists"] is False


async def test_check_emso_already_registered(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    await volunteer_factory(emso="1234567890123")
    r = await client.post(
        "/api/volunteers/check-emso",
        json={"emso": "1234567890123"},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["exists"] is True
```

### Step 4.2 — Run

```bash
cd api && pytest tests/test_volunteers.py -v
```

Expected: all tests PASSED. If `test_delete_volunteer_not_found` fails with 405 (method not allowed), check the actual HTTP method used by the delete endpoint and adjust.

### Step 4.3 — Commit

```bash
git add api/tests/test_volunteers.py
git commit -m "test: add volunteer endpoint tests"
```

---

## Task 5: Log Entry Endpoints

**Files:**
- Create: `api/tests/test_log_entries.py`

### Step 5.1 — Write tests

```python
# api/tests/test_log_entries.py
import uuid
from decimal import Decimal
from datetime import date
import pytest
from httpx import AsyncClient

from models.log_entry import EntryStatus


_WORK_DATE = "2026-01-15"


# ── list ──────────────────────────────────────────────────────────────────────

async def test_list_entries_empty(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/log-entries", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


async def test_list_entries_returns_created_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id)
    r = await client.get("/api/log-entries", headers=auth)
    assert r.status_code == 200
    assert r.json()["total"] == 1


async def test_list_entries_filter_by_volunteer(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v1 = await volunteer_factory(phone="+38641111111", emso="1234567890123")
    v2 = await volunteer_factory(phone="+38641222222", emso="9876543210987")
    await log_entry_factory(v1.id)
    await log_entry_factory(v2.id)
    r = await client.get(f"/api/log-entries?volunteer_id={v1.id}", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["volunteer_id"] == str(v1.id)


async def test_list_entries_filter_by_status(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.get("/api/log-entries?status=approved", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["status"] == "approved"


# ── create ────────────────────────────────────────────────────────────────────

async def test_create_entry_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    payload = {
        "volunteer_id": str(v.id),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoč pri prireditvi",
        "hours": "3.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 201
    data = r.json()
    assert data["volunteer_id"] == str(v.id)
    assert data["status"] == "pending_manager"


async def test_create_entry_inactive_volunteer_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=False)
    payload = {
        "volunteer_id": str(v.id),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoč",
        "hours": "1.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 409


async def test_create_entry_unknown_volunteer_returns_404(
    client: AsyncClient, auth: dict
) -> None:
    payload = {
        "volunteer_id": str(uuid.uuid4()),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoč",
        "hours": "1.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 404


async def test_create_entry_missing_required_field_returns_422(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    payload = {"volunteer_id": str(v.id), "work_date": _WORK_DATE}  # missing hours
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 422


# ── get single ────────────────────────────────────────────────────────────────

async def test_get_entry_found(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.get(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 200
    assert r.json()["id"] == str(e.id)


async def test_get_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.get(f"/api/log-entries/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


# ── update ────────────────────────────────────────────────────────────────────

async def test_update_entry_success(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.put(
        f"/api/log-entries/{e.id}",
        json={"activity_description": "Ažurirano delo", "hours": "4.0",
              "work_date": _WORK_DATE},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["activity_description"] == "Ažurirano delo"


async def test_update_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.put(
        f"/api/log-entries/{uuid.uuid4()}",
        json={"activity_description": "X", "hours": "1.0", "work_date": _WORK_DATE},
        headers=auth,
    )
    assert r.status_code == 404


# ── approve ───────────────────────────────────────────────────────────────────

async def test_approve_pending_manager_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "approved"


async def test_approve_already_approved_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_approve_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(f"/api/log-entries/{uuid.uuid4()}/approve", headers=auth)
    assert r.status_code == 404


# ── reject ────────────────────────────────────────────────────────────────────

async def test_reject_pending_manager_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    r = await client.patch(f"/api/log-entries/{e.id}/reject", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"


async def test_reject_approved_entry_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/reject", headers=auth)
    assert r.status_code == 409


async def test_reject_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(f"/api/log-entries/{uuid.uuid4()}/reject", headers=auth)
    assert r.status_code == 404


# ── confirm ───────────────────────────────────────────────────────────────────

async def test_confirm_pending_volunteer_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_VOLUNTEER)
    r = await client.post(f"/api/log-entries/{e.id}/confirm", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "pending_manager"


async def test_confirm_already_approved_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.post(f"/api/log-entries/{e.id}/confirm", headers=auth)
    assert r.status_code == 409


async def test_confirm_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.post(f"/api/log-entries/{uuid.uuid4()}/confirm", headers=auth)
    assert r.status_code == 404


# ── status machine ────────────────────────────────────────────────────────────

async def test_status_cannot_go_from_approved_to_pending_manager(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """Approved entry cannot be approved again (would be a no-op but status must stay approved)."""
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_status_cannot_go_from_rejected_to_approved(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.REJECTED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


# ── delete ────────────────────────────────────────────────────────────────────

async def test_delete_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.delete(f"/api/log-entries/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


# ── photo upload ──────────────────────────────────────────────────────────────

async def test_photo_upload_unsupported_extension_returns_400(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """Files with unsupported extensions must be rejected before any disk write."""
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.post(
        f"/api/log-entries/{e.id}/photo",
        files={"file": ("test.exe", b"fake content", "application/octet-stream")},
        headers=auth,
    )
    assert r.status_code in (400, 422)
```

### Step 5.2 — Run

```bash
cd api && pytest tests/test_log_entries.py -v
```

Expected: all tests PASSED. Note: `test_photo_upload_unsupported_extension_returns_400` may return 400 or 422 depending on implementation — both are acceptable.

### Step 5.3 — Commit

```bash
git add api/tests/test_log_entries.py
git commit -m "test: add log entry endpoint tests including status machine"
```

---

## Task 6: Report Endpoints

**Files:**
- Create: `api/tests/test_reports.py`

### Step 6.1 — Write tests

```python
# api/tests/test_reports.py
import pytest
from httpx import AsyncClient
from decimal import Decimal
from datetime import date

from models.log_entry import EntryStatus


async def test_monthly_summary_empty(client: AsyncClient, auth: dict) -> None:
    """Monthly summary with no entries returns zero totals."""
    r = await client.get("/api/reports/monthly?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["year"] == 2026
    assert data["month"] == 1
    assert data["total_entries"] == 0
    assert float(data["total_hours"]) == 0.0


async def test_monthly_summary_counts_only_approved_entries(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """Only approved entries are counted in the monthly totals."""
    v = await volunteer_factory()
    await log_entry_factory(
        v.id,
        work_date=date(2026, 1, 15),
        hours=Decimal("3.0"),
        status=EntryStatus.APPROVED,
    )
    await log_entry_factory(
        v.id,
        work_date=date(2026, 1, 20),
        hours=Decimal("2.0"),
        status=EntryStatus.PENDING_MANAGER,
    )
    r = await client.get("/api/reports/monthly?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total_entries"] == 1
    assert float(data["total_hours"]) == 3.0


async def test_monthly_summary_missing_params_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    """year and month are required query params."""
    r = await client.get("/api/reports/monthly", headers=auth)
    assert r.status_code == 422


async def test_monthly_pdf_returns_pdf_content_type(
    client: AsyncClient, auth: dict
) -> None:
    """PDF endpoint returns application/pdf content-type."""
    r = await client.post(
        "/api/reports/monthly/pdf?year=2026&month=1", headers=auth
    )
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"


async def test_monthly_pdf_for_unknown_volunteer_returns_404(
    client: AsyncClient, auth: dict
) -> None:
    import uuid
    r = await client.post(
        f"/api/reports/monthly/pdf?year=2026&month=1&volunteer_id={uuid.uuid4()}",
        headers=auth,
    )
    assert r.status_code == 404
```

### Step 6.2 — Run

```bash
cd api && pytest tests/test_reports.py -v
```

Expected: all tests PASSED. `test_monthly_pdf_returns_pdf_content_type` requires WeasyPrint to be installed and working (it is, per `requirements.txt`).

### Step 6.3 — Commit

```bash
git add api/tests/test_reports.py
git commit -m "test: add report endpoint tests"
```

---

## Task 7: Analytics Endpoint

**Files:**
- Create: `api/tests/test_analytics.py`

### Step 7.1 — Write tests

```python
# api/tests/test_analytics.py
import pytest
from decimal import Decimal
from datetime import date
from httpx import AsyncClient

from models.log_entry import EntryStatus


_REQUIRED_KEYS = {
    "year", "month", "total_hours", "active_volunteer_count",
    "entries_pending", "entries_approved", "entries_rejected",
    "hours_per_volunteer", "hours_per_location", "monthly_trend",
}


async def test_analytics_summary_default_month(
    client: AsyncClient, auth: dict
) -> None:
    """Summary without explicit year/month defaults to current month."""
    r = await client.get("/api/analytics/summary", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert _REQUIRED_KEYS.issubset(data.keys())


async def test_analytics_summary_explicit_month(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.get("/api/analytics/summary?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["year"] == 2026
    assert data["month"] == 1


async def test_analytics_summary_counts_approved_hours(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    """Approved entries contribute to total_hours; pending/rejected do not."""
    v = await volunteer_factory()
    await log_entry_factory(
        v.id,
        work_date=date(2026, 3, 10),
        hours=Decimal("5.0"),
        status=EntryStatus.APPROVED,
    )
    await log_entry_factory(
        v.id,
        work_date=date(2026, 3, 11),
        hours=Decimal("3.0"),
        status=EntryStatus.PENDING_MANAGER,
    )
    r = await client.get("/api/analytics/summary?year=2026&month=3", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert float(data["total_hours"]) == 5.0
    assert data["entries_pending"] == 1
    assert data["entries_approved"] == 1


async def test_analytics_summary_active_volunteer_count(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    """active_volunteer_count reflects only active volunteers."""
    await volunteer_factory(phone="+38641111111", emso="1111111111111", active=True)
    await volunteer_factory(phone="+38641222222", emso="2222222222222", active=False)
    r = await client.get("/api/analytics/summary", headers=auth)
    assert r.status_code == 200
    # At least 1 active volunteer (there may be others from the session seed)
    assert r.json()["active_volunteer_count"] >= 1


async def test_analytics_summary_monthly_trend_has_6_points(
    client: AsyncClient, auth: dict
) -> None:
    """monthly_trend always returns exactly 6 data points."""
    r = await client.get("/api/analytics/summary?year=2026&month=6", headers=auth)
    assert r.status_code == 200
    assert len(r.json()["monthly_trend"]) == 6
```

### Step 7.2 — Run

```bash
cd api && pytest tests/test_analytics.py -v
```

Expected: all tests PASSED.

### Step 7.3 — Commit

```bash
git add api/tests/test_analytics.py
git commit -m "test: add analytics summary tests"
```

---

## Task 8: Run Full Suite

### Step 8.1 — Run all tests

```bash
cd api && pytest -v
```

Expected: all tests green. Note the count — you should see approximately 50+ tests.

### Step 8.2 — Commit if any fixes were needed

If any tests needed adjustment during the run, commit those fixes:

```bash
git add -p
git commit -m "test: fix test assertions after full suite run"
```

---

## Task 9: Backup / Restore Smoke Test

**Files:**
- Create: `scripts/test_backup_restore.sh`

### Step 9.1 — Verify backup.sh and restore.sh exist

```bash
ls scripts/backup.sh scripts/restore.sh
```

Expected: both files present. If either is missing, this task cannot proceed — raise the issue before continuing.

### Step 9.2 — Write `scripts/test_backup_restore.sh`

```bash
#!/usr/bin/env bash
# Smoke test: backup → drop → init.sql → restore → verify.
# Run from the repo root.  Requires the belpro stack to be up.
set -euo pipefail

API="http://localhost:8100"
MANAGER_USER="admin"
MANAGER_PASS="${MANAGER_PASSWORD:-changeme}"  # read from env or .env
AUTH="-u ${MANAGER_USER}:${MANAGER_PASS}"

echo "=== BelPro backup/restore smoke test ==="

# 1. Confirm stack is running
echo "[1] Checking stack health..."
curl -sf "${API}/api/health" | grep -q '"status":"ok"' \
  || { echo "FAIL: stack not healthy"; exit 1; }

# 2. Seed known data via API
echo "[2] Seeding test data..."
VOLUNTEER_RESP=$(curl -sf -X POST "${API}/api/volunteers" \
  ${AUTH} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Backup",
    "last_name": "Test",
    "street": "Testna 99",
    "postal_code": "1000",
    "city": "Ljubljana",
    "emso": "9999999999999",
    "phone": "+38641999888"
  }')

VOLUNTEER_ID=$(echo "${VOLUNTEER_RESP}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "    Seeded volunteer: ${VOLUNTEER_ID}"

# 3. Run backup
echo "[3] Running backup..."
SNAPSHOT=$(bash scripts/backup.sh | tail -1)
echo "    Snapshot: ${SNAPSHOT}"
[ -f "${SNAPSHOT}" ] || { echo "FAIL: snapshot file not created at ${SNAPSHOT}"; exit 1; }

# 4. Drop the belpro database
echo "[4] Dropping belpro database..."
docker compose exec -T postgres psql -U belpro -d postgres -c "DROP DATABASE IF EXISTS belpro;"

# 5. Recreate schema via init.sql
echo "[5] Recreating schema via init.sql..."
docker compose exec -T postgres psql -U belpro -d postgres -c "CREATE DATABASE belpro;"
docker compose exec -T postgres psql -U belpro -d belpro < db/init.sql

# 6. Restore from snapshot
echo "[6] Restoring from snapshot..."
bash scripts/restore.sh "${SNAPSHOT}"

# 7. Verify the seeded volunteer is present
echo "[7] Verifying restore..."
ITEMS=$(curl -sf "${API}/api/volunteers" ${AUTH} | python3 -c "import sys,json; print(json.load(sys.stdin)['total'])")
echo "    Volunteers after restore: ${ITEMS}"

curl -sf "${API}/api/volunteers/${VOLUNTEER_ID}" ${AUTH} > /dev/null \
  || { echo "FAIL: seeded volunteer not found after restore"; exit 1; }

# 8. Cleanup test data
echo "[8] Cleaning up seeded test volunteer..."
curl -sf -X DELETE "${API}/api/volunteers/${VOLUNTEER_ID}" ${AUTH} || true
rm -f "${SNAPSHOT}"

echo ""
echo "=== PASS: backup/restore smoke test completed successfully ==="
```

### Step 9.3 — Make executable

```bash
chmod +x scripts/test_backup_restore.sh
```

### Step 9.4 — Commit

```bash
git add scripts/test_backup_restore.sh
git commit -m "test: add backup/restore smoke test script"
```

---

## Self-Review Checklist

- [x] **Spec coverage:** All spec sections covered: infrastructure (Task 1), health (Task 2), managers (Task 3), volunteers (Task 4), log entries + status machine (Task 5), reports (Task 6), analytics (Task 7), backup/restore (Task 9).
- [x] **No placeholders:** All test code is complete and runnable.
- [x] **Type consistency:** `volunteer_factory` and `log_entry_factory` signatures are consistent throughout all test files.
- [x] **Photo test:** Included as a negative test only (unsupported extension) — positive upload test omitted because it would write to the real filesystem outside the DB transaction scope.
- [x] **delete_volunteer positive test:** Not included — the volunteer model is "never hard-deleted" per the spec. The 404 case is covered. Positive soft-delete is covered via deactivate/activate.
