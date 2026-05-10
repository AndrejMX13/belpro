import asyncio
import base64
import itertools
import os
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

    # Teardown: delete volunteer (cascades to log entries).
    await api_client.delete(f"/api/volunteers/{volunteer['id']}")
