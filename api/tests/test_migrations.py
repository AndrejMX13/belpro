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
