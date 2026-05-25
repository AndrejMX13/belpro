"""Tests for the public config endpoint consumed by n8n workflows."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_evolution_instance_no_auth_required(client: AsyncClient) -> None:
    """GET /api/config/evolution-instance is publicly accessible."""
    r = await client.get("/api/config/evolution-instance")
    assert r.status_code == 200


@pytest.mark.anyio
async def test_get_evolution_instance_returns_instance_name(client: AsyncClient) -> None:
    """Response contains a non-empty instance_name string matching the seeded default."""
    r = await client.get("/api/config/evolution-instance")
    data = r.json()
    assert "instance_name" in data
    assert isinstance(data["instance_name"], str)
    assert len(data["instance_name"]) > 0


@pytest.mark.anyio
async def test_get_evolution_instance_reflects_db_value(
    client: AsyncClient,
    auth: dict,
) -> None:
    """Config endpoint reflects value updated via PATCH /api/admin/settings."""
    await client.patch(
        "/api/admin/settings",
        json={"evolution_instance_name": "reflected"},
        headers=auth,
    )
    r = await client.get("/api/config/evolution-instance")
    assert r.json()["instance_name"] == "reflected"
