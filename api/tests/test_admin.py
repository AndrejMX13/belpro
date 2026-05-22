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


async def test_get_settings_returns_backup_retention_default(
    client: AsyncClient, auth: dict
) -> None:
    """GET /api/admin/settings returns default backup_retention_days of 30."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["backup_retention_days"] == 30


async def test_patch_settings_saves_backup_retention(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH /api/admin/settings persists backup_retention_days."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"backup_retention_days": 14},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["backup_retention_days"] == 14


async def test_get_settings_returns_report_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns report_auto_hour default of 7."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["report_auto_hour"] == 7


async def test_patch_settings_saves_report_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists report_auto_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 9},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["report_auto_hour"] == 9


async def test_patch_settings_report_hour_boundary_zero(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings accepts report_auto_hour=0."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 0},
            headers=auth,
        )

    assert r.status_code == 200


async def test_patch_settings_report_hour_boundary_23(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings accepts report_auto_hour=23."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 23},
            headers=auth,
        )

    assert r.status_code == 200


async def test_patch_settings_report_hour_rejects_24(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings rejects report_auto_hour=24."""
    r = await client.patch(
        "/api/admin/settings",
        json={"report_auto_hour": 24},
        headers=auth,
    )
    assert r.status_code == 422


async def test_patch_settings_report_hour_rejects_negative(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings rejects report_auto_hour=-1."""
    r = await client.patch(
        "/api/admin/settings",
        json={"report_auto_hour": -1},
        headers=auth,
    )
    assert r.status_code == 422


async def test_patch_settings_ops_payload_includes_report_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings includes report_auto_hour in ops /reconfigure payload."""
    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))

    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_hour": 9},
            headers=auth,
        )

    assert r.status_code == 200
    call_args = mock_http.post.call_args
    assert "report_auto_hour" in call_args[1]["json"]


# ── Missing coverage for existing hour-type settings ──────────────────────────

async def test_get_settings_returns_backup_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns backup_hour default of 2."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["backup_hour"] == 2


async def test_patch_settings_saves_backup_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists backup_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"backup_hour": 4},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["backup_hour"] == 4


async def test_get_settings_returns_photo_cleanup_hour_default(client: AsyncClient, auth: dict) -> None:
    """GET /api/admin/settings returns photo_cleanup_hour default of 3."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    assert r.json()["photo_cleanup_hour"] == 3


async def test_patch_settings_saves_photo_cleanup_hour(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings persists photo_cleanup_hour."""
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"photo_cleanup_hour": 5},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["photo_cleanup_hour"] == 5


async def test_patch_settings_ops_payload_includes_all_fields(client: AsyncClient, auth: dict) -> None:
    """PATCH /api/admin/settings sends all tunable fields to ops /reconfigure."""
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
    payload = mock_http.post.call_args[1]["json"]
    for field in ("report_auto_day", "report_auto_period", "backup_hour",
                  "photo_cleanup_hour", "backup_retention_days", "report_auto_hour"):
        assert field in payload, f"Missing field in ops payload: {field}"
