"""Admin router — runtime-tunable settings management."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.app_setting import AppSetting
from schemas.admin import AdminSettingsResponse, AdminSettingsUpdate
from services.app_settings import AppSettings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def get_admin_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AdminSettingsResponse:
    """Return current values of all runtime-tunable settings."""
    rows = (await db.execute(select(AppSetting))).scalars().all()
    env = get_settings()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
    )


@router.patch(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def update_admin_settings(
    body: AdminSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AdminSettingsResponse:
    """Update one or more runtime-tunable settings. Returns updated state."""
    updates = {k: str(v) for k, v in body.model_dump(exclude_none=True).items()}

    for name, value in updates.items():
        row = (
            await db.execute(select(AppSetting).where(AppSetting.name == name))
        ).scalar_one_or_none()
        if row is None:
            db.add(AppSetting(name=name, value_type="int", value=value))
        else:
            row.value = value

    if updates:
        await db.commit()

    rows = (await db.execute(select(AppSetting))).scalars().all()
    env = get_settings()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
    )
