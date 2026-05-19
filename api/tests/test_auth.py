"""Tests for auth helpers and endpoints."""
import pytest

from core.auth import _make_session_token, _verify_session_token

_SECRET = "test-secret-key-32-bytes-padding!"


def test_make_and_verify_session_token() -> None:
    token = _make_session_token(_SECRET)
    assert isinstance(token, str)
    assert len(token) > 10
    assert _verify_session_token(token, _SECRET, duration_hours=24) is True


def test_verify_session_token_wrong_secret() -> None:
    token = _make_session_token(_SECRET)
    assert _verify_session_token(token, "wrong-secret", duration_hours=24) is False


def test_verify_session_token_garbage() -> None:
    assert _verify_session_token("notavalidtoken", _SECRET, duration_hours=24) is False


def test_verify_session_token_empty() -> None:
    assert _verify_session_token("", _SECRET, duration_hours=24) is False


def test_verify_session_token_expired() -> None:
    token = _make_session_token(_SECRET)
    # duration_hours=-1 means max_age=-3600 seconds — token expired 1 hour ago
    assert _verify_session_token(token, _SECRET, duration_hours=-1) is False


import base64

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success_sets_cookie(client: AsyncClient) -> None:
    r = await client.post("/api/auth/login", json={"password": "testpass123"})
    assert r.status_code == 200
    assert r.json() == {"ok": True}
    assert "belpro_session" in r.cookies


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client: AsyncClient) -> None:
    r = await client.post("/api/auth/login", json={"password": "wrongpassword"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_logout_clears_cookie(client: AsyncClient) -> None:
    await client.post("/api/auth/login", json={"password": "testpass123"})
    r = await client.post("/api/auth/logout")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


@pytest.mark.asyncio
async def test_cookie_auth_grants_access_to_protected_route(client: AsyncClient) -> None:
    # Login — httpx stores the cookie automatically
    await client.post("/api/auth/login", json={"password": "testpass123"})
    # No Authorization header — cookie is sent automatically by httpx
    r = await client.get("/api/managers/me")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_no_auth_returns_401_without_www_authenticate(client: AsyncClient) -> None:
    r = await client.get("/api/managers/me")
    assert r.status_code == 401
    # Must NOT trigger the browser's native Basic Auth dialog
    assert "WWW-Authenticate" not in r.headers
