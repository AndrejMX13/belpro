"""Managers router — single-manager setup and profile."""
from __future__ import annotations

import logging
import secrets
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import Settings, get_settings
from db.session import get_db
from models.manager import Manager
from schemas.manager import ConfigInfoResponse, ManagerCreate, ManagerResponse, ManagerUpdate, PasswordChangeRequest
from services.evolution import EvolutionClient
from services.password import hash_password, verify_password
from utils.env_writer import write_env_key

router = APIRouter(prefix="/managers", tags=["managers"])

logger = logging.getLogger(__name__)


@router.get("/me", response_model=ManagerResponse, dependencies=[Depends(require_manager)])
async def get_manager(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ManagerResponse:
    """Return the single manager profile, or 404 if setup has not been completed."""
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not configured.")
    return manager


@router.post(
    "",
    response_model=ManagerResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_manager)],
)
async def create_manager(
    payload: ManagerCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ManagerResponse:
    """Seed the manager profile (first-time setup). Returns 409 if already configured."""
    existing = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Manager is already configured.",
        )
    manager = Manager(
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        email=str(payload.email),
        ngo_name=payload.ngo_name,
        ngo_street=payload.ngo_street,
        ngo_postal_code=payload.ngo_postal_code,
        ngo_city=payload.ngo_city,
    )
    db.add(manager)
    await db.commit()
    await db.refresh(manager)
    return manager


@router.patch("/me", response_model=ManagerResponse, dependencies=[Depends(require_manager)])
async def update_manager(
    payload: ManagerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ManagerResponse:
    """Update manager and/or NGO fields.  Only provided (non-None) fields are written."""
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not configured.")

    for field, value in payload.model_dump(exclude_none=True).items():
        if field == "email":
            value = str(value)
        setattr(manager, field, value)

    await db.commit()
    await db.refresh(manager)
    return manager


@router.get("/me/config-info", dependencies=[Depends(require_manager)])
async def get_config_info(
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ConfigInfoResponse:
    """Return config status for the settings UI; auto-syncs WhatsApp phone if connected."""
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not configured.")

    client = EvolutionClient(
        base_url=settings.evolution_api_url,
        api_key=settings.authentication_api_key,
        instance_name=settings.evolution_instance_name,
    )
    live_phone, wa_state = await client.get_connected_phone()

    wa_synced = False
    wa_env_write_ok = True

    if wa_state == "open" and live_phone and live_phone != manager.ngo_whatsapp_phone:
        logger.info(
            "WhatsApp phone auto-sync: DB=%s → Evolution API=%s",
            manager.ngo_whatsapp_phone,
            live_phone,
        )
        manager.ngo_whatsapp_phone = live_phone
        await db.commit()
        wa_synced = True
        wa_env_write_ok = write_env_key("NGO_WHATSAPP_PHONE", live_phone, Path(".env"))
        if not wa_env_write_ok:
            logger.warning("Failed to write NGO_WHATSAPP_PHONE to .env after auto-sync")

    wa_phone = live_phone if wa_state == "open" else manager.ngo_whatsapp_phone
    smtp_configured = bool(manager.smtp_host and manager.smtp_user and settings.smtp_password)

    return ConfigInfoResponse(
        smtp_host=manager.smtp_host or "",
        smtp_port=manager.smtp_port or 587,
        smtp_user=manager.smtp_user or "",
        smtp_from_name=manager.smtp_from_name or "",
        smtp_configured=smtp_configured,
        evolution_api_admin_url=manager.evolution_api_admin_url or "http://localhost:8180/manager/login",
        wa_phone=wa_phone,
        wa_state=wa_state,
        wa_synced=wa_synced,
        wa_env_write_ok=wa_env_write_ok,
    )


@router.post(
    "/me/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_manager)],
)
async def change_password(
    payload: PasswordChangeRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Response:
    """Change the manager password.  Verifies the current password before updating."""
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not configured.")

    if manager.password_hash:
        current_ok = verify_password(payload.current_password, manager.password_hash)
    else:
        current_ok = secrets.compare_digest(
            payload.current_password.encode("utf-8"),
            settings.manager_password.encode("utf-8"),
        )

    if not current_ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trenutno geslo ni pravilno.",
        )

    manager.password_hash = hash_password(payload.new_password)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
