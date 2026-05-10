import asyncio
import base64
import itertools
import os
import subprocess
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
import httpx

load_dotenv(Path(__file__).parent.parent.parent / ".env", override=False)

_API_BASE = "http://localhost:8100"
_N8N_BASE = "http://localhost:5678"
_WEBHOOK_PATH = "/webhook/volunteer-message"

_phone_seq = itertools.count(1)


def _manager_password() -> str:
    pw = os.getenv("MANAGER_PASSWORD", "")
    if not pw:
        raise RuntimeError("MANAGER_PASSWORD not set — is .env loaded?")
    return pw


def _auth_header() -> dict[str, str]:
    creds = base64.b64encode(f"manager:{_manager_password()}".encode()).decode()
    return {"Authorization": f"Basic {creds}"}


@pytest_asyncio.fixture(scope="session")
async def api_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable."""
    async with httpx.AsyncClient(
        base_url=_API_BASE, headers=_auth_header(), timeout=30.0
    ) as client:
        try:
            r = await client.get("/api/health")
            r.raise_for_status()
        except Exception as exc:
            pytest.skip(f"FastAPI not reachable at {_API_BASE}: {exc}")
        yield client


@pytest_asyncio.fixture(scope="session")
async def n8n_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Session-scoped AsyncClient against n8n. Skips all tests if unreachable."""
    async with httpx.AsyncClient(base_url=_N8N_BASE, timeout=30.0) as client:
        try:
            r = await client.get("/healthz")
            if r.status_code >= 500:
                raise RuntimeError(f"n8n returned {r.status_code}")
        except Exception as exc:
            pytest.skip(f"n8n not reachable at {_N8N_BASE}: {exc}")
        yield client


@pytest_asyncio.fixture
async def test_volunteer(api_client: httpx.AsyncClient) -> AsyncGenerator[dict, None]:
    """
    Creates a volunteer with a unique phone, yields the volunteer dict,
    deletes it (and cascade-deletes entries) on teardown.
    """
    seq = next(_phone_seq)
    # Range 38640900001–38640999999 — unlikely to match the real manager phone.
    phone = f"38640900{seq:03d}"

    payload = {
        "first_name": "Test",
        "last_name": f"Prostovoljec{seq}",
        "street": "Testna ulica 1",
        "postal_code": "1000",
        "city": "Ljubljana",
        "emso": f"{seq:013d}",
        "phone": phone,
        "report_whatsapp": True,
        "report_email": False,
    }
    r = await api_client.post("/api/volunteers", json=payload)
    assert r.status_code == 201, f"Failed to create test volunteer: {r.text}"
    volunteer = r.json()

    yield volunteer

    # Teardown: clean up via direct DB access.
    # Can't use DELETE /api/volunteers/{id} — it blocks if any log entries exist.
    # Can't use DELETE /api/log-entries/{id} — only works for pending_volunteer status.
    # Direct SQL is the only reliable approach for integration test cleanup.
    vol_id = volunteer["id"]
    subprocess.run(
        [
            "docker", "compose", "exec", "-T", "db",
            "psql", "-U", "belpro", "-d", "belpro", "-c",
            f"DELETE FROM log_entry_photos WHERE entry_id IN "
            f"(SELECT id FROM log_entries WHERE volunteer_id = '{vol_id}'); "
            f"DELETE FROM log_entries WHERE volunteer_id = '{vol_id}'; "
            f"DELETE FROM volunteers WHERE id = '{vol_id}';",
        ],
        capture_output=True,
        cwd=str(Path(__file__).parent.parent.parent),
    )
