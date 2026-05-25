"""Admin router — runtime-tunable settings management."""
from __future__ import annotations

import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import Settings, get_settings
from db.session import AsyncSessionLocal, get_db
from models.app_setting import AppSetting
from models.error_log import ErrorLog
from schemas.admin import AdminSettingsResponse, AdminSettingsUpdate
from services.app_settings import AppSettings

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


async def _notify_ops(env: Settings, s: AppSettings) -> None:
    """POST /reconfigure to ops. Logs and persists error on failure; never raises."""
    payload = {
        "report_auto_day": s.report_auto_day,
        "report_auto_period": s.report_auto_period,
        "report_auto_hour": s.report_auto_hour,
        "backup_hour": s.backup_hour,
        "photo_cleanup_hour": s.photo_cleanup_hour,
        "backup_retention_days": s.backup_retention_days,
    }
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(
                f"{env.ops_url}/reconfigure",
                json=payload,
                headers={"X-Internal-Key": env.api_secret_key},
            )
            r.raise_for_status()
    except Exception as exc:
        logger.warning("ops notification failed: %s", exc)
        async with AsyncSessionLocal() as error_session:
            async with error_session.begin():
                error_session.add(ErrorLog(
                    service="api",
                    operation="notify_ops_reconfigure",
                    message="Ops service notification failed",
                    detail=str(exc),
                ))


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
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
        report_auto_hour=s.report_auto_hour,
        backup_hour=s.backup_hour,
        photo_cleanup_hour=s.photo_cleanup_hour,
        backup_retention_days=s.backup_retention_days,
        evolution_instance_name=s.evolution_instance_name,
    )


@router.patch(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def update_admin_settings(
    body: AdminSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    env: Annotated[Settings, Depends(get_settings)],
) -> AdminSettingsResponse:
    """Update one or more runtime-tunable settings. Returns updated state."""
    raw_updates = body.model_dump(exclude_none=True)
    # Infer value_type from Python type so string settings are stored correctly.
    updates = {
        k: (str(v), "str" if isinstance(v, str) else "int")
        for k, v in raw_updates.items()
    }

    for name, (value, vtype) in updates.items():
        row = (
            await db.execute(select(AppSetting).where(AppSetting.name == name))
        ).scalar_one_or_none()
        if row is None:
            db.add(AppSetting(name=name, value_type=vtype, value=value))
        else:
            row.value = value

    if updates:
        await db.commit()

    rows = (await db.execute(select(AppSetting))).scalars().all()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})

    if updates:
        await _notify_ops(env, s)

    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
        report_auto_hour=s.report_auto_hour,
        backup_hour=s.backup_hour,
        photo_cleanup_hour=s.photo_cleanup_hour,
        backup_retention_days=s.backup_retention_days,
        evolution_instance_name=s.evolution_instance_name,
    )
