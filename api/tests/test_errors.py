"""Tests for POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge."""
from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from core.settings import get_settings


def _internal_header() -> dict[str, str]:
    return {"X-Internal-Key": get_settings().api_secret_key}


async def test_post_error_valid_internal_key(client: AsyncClient) -> None:
    """POST with valid internal key creates a record."""
    r = await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={
            "service": "ops",
            "operation": "backup",
            "message": "pg_dump failed",
            "detail": "exit code 1",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["service"] == "ops"
    assert data["acknowledged"] is False


async def test_post_error_missing_key_rejected(client: AsyncClient) -> None:
    """POST without internal key is rejected."""
    r = await client.post(
        "/api/errors",
        json={"service": "ops", "operation": "backup", "message": "fail"},
    )
    assert r.status_code == 401


async def test_post_error_wrong_key_rejected(client: AsyncClient) -> None:
    """POST with wrong internal key is rejected."""
    r = await client.post(
        "/api/errors",
        headers={"X-Internal-Key": "not-the-right-key"},
        json={"service": "ops", "operation": "backup", "message": "fail"},
    )
    assert r.status_code == 401


async def test_get_errors_requires_manager_auth(client: AsyncClient) -> None:
    """GET /api/errors without manager auth is rejected."""
    r = await client.get("/api/errors")
    assert r.status_code == 401


async def test_get_errors_returns_list(client: AsyncClient, auth: dict) -> None:
    """GET returns all error log entries, newest first."""
    for i in range(2):
        await client.post(
            "/api/errors",
            headers=_internal_header(),
            json={"service": "api", "operation": "email_delivery", "message": f"err{i}"},
        )
    r = await client.get("/api/errors", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 2


async def test_get_errors_filter_unacknowledged(client: AsyncClient, auth: dict) -> None:
    """GET ?unacknowledged=true filters to unacknowledged only."""
    await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "n8n", "operation": "whatsapp_send", "message": "err"},
    )
    r = await client.get("/api/errors?unacknowledged=true", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert all(not e["acknowledged"] for e in data)


async def test_acknowledge_error(client: AsyncClient, auth: dict) -> None:
    """PATCH /{id}/acknowledge sets acknowledged to True."""
    r_post = await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "api", "operation": "report_generation", "message": "fail"},
    )
    error_id = r_post.json()["id"]

    r_ack = await client.patch(f"/api/errors/{error_id}/acknowledge", headers=auth)
    assert r_ack.status_code == 200
    assert r_ack.json()["acknowledged"] is True


async def test_acknowledge_nonexistent_returns_404(client: AsyncClient, auth: dict) -> None:
    """PATCH /{id}/acknowledge on unknown id returns 404."""
    r = await client.patch(f"/api/errors/{uuid.uuid4()}/acknowledge", headers=auth)
    assert r.status_code == 404


async def test_unacknowledged_count(client: AsyncClient, auth: dict) -> None:
    """GET /api/errors/unacknowledged-count returns integer count."""
    await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "ops", "operation": "photo_cleanup", "message": "err"},
    )
    r = await client.get("/api/errors/unacknowledged-count", headers=auth)
    assert r.status_code == 200
    assert isinstance(r.json()["count"], int)
    assert r.json()["count"] >= 1
