"""Tests for report auto-delivery settings."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient


async def test_get_settings_returns_report_defaults(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns defaults for report_auto_day and report_auto_period."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["report_auto_day"] == 28
    assert data["report_auto_period"] == "current"


async def test_patch_settings_saves_report_fields(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists report_auto_day and report_auto_period."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 5, "report_auto_period": "previous"},
            headers=auth,
        )

    assert r.status_code == 200
    data = r.json()
    assert data["report_auto_day"] == 5
    assert data["report_auto_period"] == "previous"


async def test_patch_settings_notifies_ops(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings calls ops /reconfigure with updated values."""
    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))

    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 1},
            headers=auth,
        )

    assert r.status_code == 200
    mock_http.post.assert_called_once()
    call_args = mock_http.post.call_args
    assert "/reconfigure" in call_args[0][0]
    assert call_args[1]["json"]["report_auto_day"] == 1


async def test_patch_settings_ops_failure_does_not_break_save(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH /api/admin/settings still returns 200 when ops service is unreachable."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(side_effect=Exception("ops unreachable"))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 10},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["report_auto_day"] == 10
