import base64
from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.manager import Manager


async def test_get_manager_returns_profile(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/managers/me", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Manager"
    assert data["email"] == "test@belpro.si"


async def test_create_manager_returns_409_when_already_configured(
    client: AsyncClient, auth: dict
) -> None:
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
    bad = base64.b64encode(b"manager:wrongpassword").decode()
    r = await client.get("/api/managers/me", headers={"Authorization": f"Basic {bad}"})
    assert r.status_code == 401


async def test_auth_missing_credentials_returns_401(client: AsyncClient) -> None:
    r = await client.get("/api/managers/me")
    assert r.status_code == 401


async def test_seed_whatsapp_phone_populates_null_db_field(db_session):
    """seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null."""
    from main import seed_whatsapp_phone_from_env
    from core.settings import Settings

    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = None
    await db_session.commit()

    fake_settings = Settings.model_construct(ngo_whatsapp_phone="+386 40 999 888")
    await seed_whatsapp_phone_from_env(db_session, fake_settings)

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640999888"


async def test_seed_whatsapp_phone_does_not_overwrite_existing_value(db_session):
    """seed_whatsapp_phone_from_env leaves existing DB value untouched."""
    from main import seed_whatsapp_phone_from_env
    from core.settings import Settings

    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640111222"
    await db_session.commit()

    fake_settings = Settings.model_construct(ngo_whatsapp_phone="38640999888")
    await seed_whatsapp_phone_from_env(db_session, fake_settings)

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640111222"


@pytest.mark.asyncio
async def test_config_info_includes_wa_fields(client, auth):
    with patch(
        "routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=(None, "unreachable")),
    ):
        resp = await client.get("/api/managers/me/config-info", headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert "wa_phone" in data
    assert "wa_state" in data
    assert "wa_synced" in data
    assert "wa_env_write_ok" in data
    assert data["wa_state"] == "unreachable"
    assert data["wa_synced"] is False


@pytest.mark.asyncio
async def test_config_info_auto_syncs_when_evolution_reports_new_phone(
    client, auth, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = None
    await db_session.commit()

    with patch(
        "routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=("38640111222", "open")),
    ):
        resp = await client.get("/api/managers/me/config-info", headers=auth)

    assert resp.status_code == 200
    data = resp.json()
    assert data["wa_phone"] == "38640111222"
    assert data["wa_state"] == "open"
    assert data["wa_synced"] is True

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640111222"


@pytest.mark.asyncio
async def test_config_info_no_sync_when_phone_already_matches(
    client, auth, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640111222"
    await db_session.commit()

    with patch(
        "routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=("38640111222", "open")),
    ):
        resp = await client.get("/api/managers/me/config-info", headers=auth)

    assert resp.json()["wa_synced"] is False


@pytest.mark.asyncio
async def test_config_info_shows_db_phone_when_disconnected(
    client, auth, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640999888"
    await db_session.commit()

    with patch(
        "routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=(None, "close")),
    ):
        resp = await client.get("/api/managers/me/config-info", headers=auth)

    data = resp.json()
    assert data["wa_phone"] == "38640999888"
    assert data["wa_state"] == "close"


@pytest.mark.asyncio
async def test_update_manager_normalizes_whatsapp_phone(client, auth):
    resp = await client.patch(
        "/api/managers/me",
        json={"ngo_whatsapp_phone": "+386 40 123 456"},
        headers=auth,
    )
    assert resp.status_code == 200
    assert resp.json()["ngo_whatsapp_phone"] == "38640123456"


@pytest.mark.asyncio
async def test_update_manager_rejects_too_short_phone(client, auth):
    resp = await client.patch(
        "/api/managers/me",
        json={"ngo_whatsapp_phone": "+123"},
        headers=auth,
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_update_manager_empty_phone_not_stored_as_empty_string(client, auth):
    # Empty string normalizes to None, which is excluded from the PATCH (no 422)
    resp = await client.patch(
        "/api/managers/me",
        json={"ngo_whatsapp_phone": ""},
        headers=auth,
    )
    assert resp.status_code == 200
    assert resp.json()["ngo_whatsapp_phone"] != ""
