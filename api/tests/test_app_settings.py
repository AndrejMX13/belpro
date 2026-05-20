"""Tests for the settings table, AppSettings service, and admin settings router."""
from __future__ import annotations

import pytest
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
