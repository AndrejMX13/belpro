"""Managers router — single-manager setup and profile."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.manager import Manager
from schemas.manager import ManagerCreate, ManagerResponse

router = APIRouter(prefix="/managers", tags=["managers"])


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
