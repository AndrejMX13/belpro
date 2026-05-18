import uuid
from decimal import Decimal
from datetime import date

import pytest
from httpx import AsyncClient

from models.log_entry import EntryStatus


_WORK_DATE = "2026-01-15"


async def test_list_entries_empty(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/log-entries", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


async def test_list_entries_returns_created_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id)
    r = await client.get("/api/log-entries", headers=auth)
    assert r.status_code == 200
    assert r.json()["total"] == 1


async def test_list_entries_filter_by_volunteer(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v1 = await volunteer_factory()
    v2 = await volunteer_factory()
    await log_entry_factory(v1.id)
    await log_entry_factory(v2.id)
    r = await client.get(f"/api/log-entries?volunteer_id={v1.id}", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["volunteer_id"] == str(v1.id)


async def test_list_entries_filter_by_status(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.get("/api/log-entries?status=approved", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["status"] == "approved"


async def test_create_entry_success(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    payload = {
        "volunteer_id": str(v.id),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoc pri prireditvi",
        "hours": "3.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 201
    data = r.json()
    assert data["volunteer_id"] == str(v.id)
    assert data["status"] == "pending_manager"


async def test_create_entry_inactive_volunteer_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory(active=False)
    payload = {
        "volunteer_id": str(v.id),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoc",
        "hours": "1.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 409


async def test_create_entry_unknown_volunteer_returns_404(
    client: AsyncClient, auth: dict
) -> None:
    payload = {
        "volunteer_id": str(uuid.uuid4()),
        "work_date": _WORK_DATE,
        "activity_description": "Pomoc",
        "hours": "1.0",
    }
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 404


async def test_create_entry_missing_required_field_returns_422(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v = await volunteer_factory()
    payload = {"volunteer_id": str(v.id), "work_date": _WORK_DATE}
    r = await client.post("/api/log-entries", json=payload, headers=auth)
    assert r.status_code == 422


async def test_get_entry_found(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.get(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 200
    assert r.json()["id"] == str(e.id)


async def test_get_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.get(f"/api/log-entries/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


async def test_update_entry_success(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.patch(
        f"/api/log-entries/{e.id}",
        json={"activity_description": "Azurirano delo", "hours": "4.0",
              "work_date": _WORK_DATE},
        headers=auth,
    )
    assert r.status_code == 200
    assert r.json()["activity_description"] == "Azurirano delo"


async def test_update_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(
        f"/api/log-entries/{uuid.uuid4()}",
        json={"activity_description": "X", "hours": "1.0", "work_date": _WORK_DATE},
        headers=auth,
    )
    assert r.status_code == 404


async def test_approve_pending_manager_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "approved"


async def test_approve_already_approved_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_approve_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(f"/api/log-entries/{uuid.uuid4()}/approve", headers=auth)
    assert r.status_code == 404


async def test_reject_pending_manager_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    r = await client.patch(f"/api/log-entries/{e.id}/reject", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"


async def test_reject_approved_entry_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/reject", headers=auth)
    assert r.status_code == 409


async def test_reject_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.patch(f"/api/log-entries/{uuid.uuid4()}/reject", headers=auth)
    assert r.status_code == 404


async def test_confirm_pending_volunteer_entry(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_VOLUNTEER)
    r = await client.post(f"/api/log-entries/{e.id}/confirm", headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "pending_manager"


async def test_confirm_already_approved_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.post(f"/api/log-entries/{e.id}/confirm", headers=auth)
    assert r.status_code == 409


async def test_confirm_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.post(f"/api/log-entries/{uuid.uuid4()}/confirm", headers=auth)
    assert r.status_code == 404


async def test_status_cannot_go_from_approved_to_pending_manager(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_status_cannot_go_from_rejected_to_approved(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.REJECTED)
    r = await client.patch(f"/api/log-entries/{e.id}/approve", headers=auth)
    assert r.status_code == 409


async def test_delete_entry_not_found(client: AsyncClient, auth: dict) -> None:
    r = await client.delete(f"/api/log-entries/{uuid.uuid4()}", headers=auth)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_entry_happy_path(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_VOLUNTEER)
    r = await client.delete(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 204
    r2 = await client.get(f"/api/log-entries/{e.id}", headers=auth)
    assert r2.status_code == 404


@pytest.mark.asyncio
async def test_delete_entry_wrong_status_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.delete(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_update_approved_entry_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.patch(
        f"/api/log-entries/{e.id}",
        headers=auth,
        json={"activity_description": "Nova vsebina"},
    )
    assert r.status_code == 409


async def test_photo_upload_unsupported_extension_returns_400_or_422(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id)
    r = await client.post(
        f"/api/log-entries/{e.id}/photos",
        files={"file": ("test.exe", b"fake content", "application/octet-stream")},
        headers=auth,
    )
    assert r.status_code in (400, 422)


async def test_photo_limit_returns_default(client: AsyncClient) -> None:
    r = await client.get("/api/log-entries/photo-limit")
    assert r.status_code == 200
    assert r.json() == {"max_photos": 5}
