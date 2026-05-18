import uuid

import pytest
from httpx import AsyncClient


_VALID_PAYLOAD = {
    "first_name": "Ana",
    "last_name": "Novak",
    "street": "Testna 1",
    "postal_code": "1000",
    "city": "Ljubljana",
    "emso": "1234567890125",
    "phone": "+38641111111",
}


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
    await volunteer_factory(emso="1234567890125")
    r = await client.post("/api/volunteers", json=_VALID_PAYLOAD, headers=auth)
    assert r.status_code == 409
# Phone uniqueness is enforced by IntegrityError, which rolls back the
# savepoint before the 409 response can be returned. Not testable via HTTP
# in this isolation setup.


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


async def test_create_volunteer_invalid_emso_checksum_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    payload = {**_VALID_PAYLOAD, "emso": "1234567890123"}  # valid format, bad checksum
    r = await client.post("/api/volunteers", json=payload, headers=auth)
    assert r.status_code == 422


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


async def test_update_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    r = await client.patch(
        f"/api/volunteers/{v.id}",
        json={"report_email": False, "report_whatsapp": True},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["report_email"] is False
    assert r.json()["report_whatsapp"] is True


async def test_update_volunteer_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(
        f"/api/volunteers/{uuid.uuid4()}",
        json={"report_email": True},
        headers=auth,
    )
    assert r.status_code == 404


async def test_deactivate_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=True)
    r = await client.patch(f"/api/volunteers/{v.id}/deactivate", headers=auth)
    assert r.status_code == 200
    assert r.json()["active"] is False


async def test_deactivate_volunteer_not_found(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.patch(f"/api/volunteers/{uuid.uuid4()}/deactivate", headers=auth)
    assert r.status_code == 404


async def test_activate_volunteer_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=False)
    r = await client.patch(f"/api/volunteers/{v.id}/activate", headers=auth)
    assert r.status_code == 200
    assert r.json()["active"] is True


async def test_delete_volunteer_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.delete(f"/api/volunteers/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_volunteer_happy_path(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    r = await client.delete(f"/api/volunteers/{v.id}", headers=auth)
    assert r.status_code == 204
    r2 = await client.get(f"/api/volunteers/{v.id}", headers=auth)
    assert r2.status_code == 404


@pytest.mark.asyncio
async def test_delete_volunteer_with_entries_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id)
    r = await client.delete(f"/api/volunteers/{v.id}", headers=auth)
    assert r.status_code == 409


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
    await volunteer_factory(emso="1234567890125")
    r = await client.post(
        "/api/volunteers/check-emso",
        json={"emso": "1234567890125"},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["exists"] is True
