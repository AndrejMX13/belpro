"""Tests for report auto-delivery settings."""
from __future__ import annotations

from httpx import AsyncClient


async def test_get_settings_returns_report_defaults(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns defaults for report_auto_day and report_auto_period."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["report_auto_day"] == 28
    assert data["report_auto_period"] == "current"
