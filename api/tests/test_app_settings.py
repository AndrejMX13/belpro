"""Tests for the settings table, AppSettings service, and admin settings router."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ── Migration smoke test ──────────────────────────────────────────────────────

async def test_settings_table_seeded(db_session: AsyncSession) -> None:
    """Migration seeds the three default settings rows."""
    from models.app_setting import AppSetting

    rows = (await db_session.execute(select(AppSetting))).scalars().all()
    names = {r.name for r in rows}
    assert {"max_photos_per_entry", "photo_retention_days", "session_duration_hours"}.issubset(names)

    by_name = {r.name: r for r in rows}
    assert by_name["max_photos_per_entry"].value_type == "int"
    assert by_name["max_photos_per_entry"].value == "5"
    assert by_name["photo_retention_days"].value == "730"
    assert by_name["session_duration_hours"].value == "24"


# ── Unit tests for AppSettings ────────────────────────────────────────────────

def test_appsettings_uses_db_int_value() -> None:
    """DB value overrides env default for integer settings."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {"max_photos_per_entry": "10"})
    assert settings.max_photos_per_entry == 10


def test_appsettings_falls_back_to_env_when_row_missing() -> None:
    """Env default is used when the DB row is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {})
    assert settings.max_photos_per_entry == env.max_photos_per_entry
    assert settings.photo_retention_days == env.photo_retention_days
    assert settings.session_duration_hours == env.session_duration_hours


def test_appsettings_passthrough_to_env() -> None:
    """Non-tunable attributes delegate to the underlying env Settings."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {})
    assert settings.emso_encryption_key == env.emso_encryption_key
    assert settings.api_secret_key == env.api_secret_key


def test_appsettings_bool_helper_parses_truthy_strings() -> None:
    """_bool() accepts 'true', '1', 'yes' as True."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    for truthy in ("true", "True", "TRUE", "1", "yes"):
        s = AppSettings(env, {"flag": truthy})
        assert s._bool("flag", False) is True, f"Expected True for {truthy!r}"


def test_appsettings_bool_helper_parses_falsy_strings() -> None:
    """_bool() returns False for any non-truthy string."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    for falsy in ("false", "False", "0", "no"):
        s = AppSettings(env, {"flag": falsy})
        assert s._bool("flag", True) is False, f"Expected False for {falsy!r}"


def test_appsettings_bool_helper_falls_back_to_default() -> None:
    """_bool() returns the default when the key is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {})
    assert s._bool("missing", True) is True
    assert s._bool("missing", False) is False


def test_appsettings_str_helper_returns_db_value() -> None:
    """_str() returns the DB string when present."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {"some_text": "hello"})
    assert s._str("some_text", None) == "hello"


def test_appsettings_str_helper_falls_back_to_default() -> None:
    """_str() returns the default when key is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {})
    assert s._str("missing", "default") == "default"
    assert s._str("missing", None) is None


# ── Integration tests for GET/PATCH /api/admin/settings ──────────────────────


async def test_get_admin_settings_returns_seeded_defaults(
    client: AsyncClient, auth: dict
) -> None:
    """GET /api/admin/settings returns the seeded default values."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["max_photos_per_entry"] == 5
    assert data["photo_retention_days"] == 730
    assert data["session_duration_hours"] == 24


async def test_get_admin_settings_requires_auth(client: AsyncClient) -> None:
    """Unauthenticated request is rejected."""
    r = await client.get("/api/admin/settings")
    assert r.status_code == 401


async def test_patch_admin_settings_updates_single_field(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH updates a single field; others are unchanged."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 10}
    )
    assert r.status_code == 200
    data = r.json()
    assert data["max_photos_per_entry"] == 10
    assert data["photo_retention_days"] == 730   # unchanged
    assert data["session_duration_hours"] == 24  # unchanged


async def test_patch_admin_settings_get_reflects_change(
    client: AsyncClient, auth: dict
) -> None:
    """Subsequent GET reflects a PATCHed value."""
    r_patch = await client.patch(
        "/api/admin/settings", headers=auth, json={"session_duration_hours": 48}
    )
    assert r_patch.status_code == 200
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.json()["session_duration_hours"] == 48


async def test_patch_admin_settings_rejects_zero(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH rejects zero (ge=1 constraint)."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 0}
    )
    assert r.status_code == 422


async def test_patch_admin_settings_rejects_negative(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH rejects negative values."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"photo_retention_days": -1}
    )
    assert r.status_code == 422


async def test_patch_admin_settings_requires_auth(client: AsyncClient) -> None:
    """Unauthenticated PATCH is rejected."""
    r = await client.patch(
        "/api/admin/settings", json={"max_photos_per_entry": 5}
    )
    assert r.status_code == 401


# ── Integration: route handlers read tunables from DB ────────────────────────


async def test_photo_upload_respects_db_max_photos_setting(
    client: AsyncClient,
    auth: dict,
    db_session,
    volunteer_factory,
    log_entry_factory,
) -> None:
    """upload_photo rejects a second photo when max_photos_per_entry is patched to 1 in DB."""
    import io
    from models.app_setting import AppSetting
    from sqlalchemy import select

    # Patch max_photos_per_entry to 1 via the admin API
    r_patch = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 1}
    )
    assert r_patch.status_code == 200
    assert r_patch.json()["max_photos_per_entry"] == 1

    v = await volunteer_factory()
    e = await log_entry_factory(v.id)

    # First photo upload — should succeed
    fake_image = b"\xff\xd8\xff\xe0" + b"\x00" * 100  # minimal JPEG magic bytes
    r1 = await client.post(
        f"/api/log-entries/{e.id}/photos",
        headers=auth,
        files={"file": ("photo1.jpg", io.BytesIO(fake_image), "image/jpeg")},
    )
    assert r1.status_code == 201, f"First upload failed: {r1.text}"

    # Second photo upload — should be rejected (limit is 1)
    r2 = await client.post(
        f"/api/log-entries/{e.id}/photos",
        headers=auth,
        files={"file": ("photo2.jpg", io.BytesIO(fake_image), "image/jpeg")},
    )
    assert r2.status_code == 409, f"Expected 409 but got {r2.status_code}: {r2.text}"
    assert "1" in r2.json()["detail"]


async def test_login_cookie_max_age_reflects_db_session_duration(
    client: AsyncClient,
    auth: dict,
) -> None:
    """Login sets a cookie whose max_age matches the session_duration_hours DB setting."""
    # Patch session_duration_hours to 2 via the admin API
    r_patch = await client.patch(
        "/api/admin/settings", headers=auth, json={"session_duration_hours": 2}
    )
    assert r_patch.status_code == 200
    assert r_patch.json()["session_duration_hours"] == 2

    # Login and inspect the Set-Cookie header for max-age
    r = await client.post("/api/auth/login", json={"password": "testpass123"})
    assert r.status_code == 200
    assert "belpro_session" in r.cookies

    set_cookie = r.headers.get("set-cookie", "")
    # max-age=7200 (2 hours * 3600 seconds)
    assert "max-age=7200" in set_cookie.lower(), (
        f"Expected max-age=7200 in Set-Cookie, got: {set_cookie}"
    )
