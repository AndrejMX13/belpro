# Load test env BEFORE any app imports — must be the very first thing.
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env.test", override=True)

# ── stdlib / third-party ──────────────────────────────────────────────────────
import base64
import itertools
import subprocess
import sys
import uuid
from decimal import Decimal
from datetime import date
from typing import AsyncGenerator

_volunteer_seq = itertools.count(1)

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

# ── app imports (Settings already reads the overridden env vars) ──────────────
from core.settings import get_settings

# Clear lru_cache so Settings() re-reads the overridden env vars.
get_settings.cache_clear()

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
            existing = (await session.execute(select(Manager).limit(1))).scalar_one_or_none()
            if existing is None:
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
    creds = base64.b64encode(f"manager:{_TEST_PASS}".encode()).decode()
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
        emso: str | None = None,
        phone: str | None = None,
        active: bool = True,
        **overrides,
    ) -> Volunteer:
        seq = next(_volunteer_seq)
        resolved_emso = emso if emso is not None else f"{seq:013d}"
        resolved_phone = phone if phone is not None else f"+3864{seq:07d}"
        v = Volunteer(
            first_name=first_name,
            last_name=last_name,
            street="Testna 1",
            postal_code="1000",
            city="Ljubljana",
            emso=encrypt_emso(resolved_emso, key),
            emso_hash=hash_emso(resolved_emso, key),
            phone=resolved_phone,
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
        volunteer_id: uuid.UUID,
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
