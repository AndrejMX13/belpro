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
