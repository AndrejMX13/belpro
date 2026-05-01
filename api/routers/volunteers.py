"""Volunteers CRUD router."""
from __future__ import annotations

import uuid
from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.auth import require_manager
from core.settings import Settings, get_settings
from db.session import get_db
from models.log_entry import LogEntry
from models.manager import Manager
from models.volunteer import Volunteer
from schemas.volunteer import (
    VolunteerCreate,
    VolunteerDetailResponse,
    VolunteerListResponse,
    VolunteerResponse,
)
from services.encryption import decrypt_emso, encrypt_emso, load_key, mask_emso

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

# Columns allowed as sort targets — explicit whitelist prevents injection via query param.
_SORTABLE = frozenset({"last_name", "first_name", "registered_at", "city"})


def _to_response(volunteer: Volunteer, key: bytes) -> VolunteerResponse:
    """Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object."""
    masked = mask_emso(decrypt_emso(volunteer.emso, key))
    return VolunteerResponse.model_validate(volunteer, update={"emso_masked": masked})


def _to_detail_response(volunteer: Volunteer, key: bytes) -> VolunteerDetailResponse:
    """Same as _to_response but includes sorted log_entries."""
    masked = mask_emso(decrypt_emso(volunteer.emso, key))
    # Sort entries newest-first in Python (entries are already loaded via selectinload).
    volunteer.log_entries.sort(key=lambda e: e.entry_date, reverse=True)
    return VolunteerDetailResponse.model_validate(volunteer, update={"emso_masked": masked})


@router.get("", response_model=VolunteerListResponse)
async def list_volunteers(
    active: bool | None = Query(default=None, description="True=active only, False=inactive, omit=all"),
    city: str | None = Query(default=None, description="Case-insensitive partial match"),
    registered_after: date | None = Query(default=None),
    registered_before: date | None = Query(default=None),
    sort_by: Literal["last_name", "first_name", "registered_at", "city"] = Query(default="last_name"),
    sort_dir: Literal["asc", "desc"] = Query(default="asc"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerListResponse:
    """List volunteers with optional filters, sorting, and pagination."""
    stmt = select(Volunteer)
    count_stmt = select(func.count()).select_from(Volunteer)

    if active is not None:
        stmt = stmt.where(Volunteer.active == active)
        count_stmt = count_stmt.where(Volunteer.active == active)
    if city:
        stmt = stmt.where(Volunteer.city.ilike(f"%{city}%"))
        count_stmt = count_stmt.where(Volunteer.city.ilike(f"%{city}%"))
    if registered_after:
        stmt = stmt.where(Volunteer.registered_at >= registered_after)
        count_stmt = count_stmt.where(Volunteer.registered_at >= registered_after)
    if registered_before:
        stmt = stmt.where(Volunteer.registered_at <= registered_before)
        count_stmt = count_stmt.where(Volunteer.registered_at <= registered_before)

    col = getattr(Volunteer, sort_by)
    stmt = stmt.order_by(col.asc() if sort_dir == "asc" else col.desc())
    stmt = stmt.offset(offset).limit(limit)

    total = (await db.execute(count_stmt)).scalar_one()
    volunteers = (await db.execute(stmt)).scalars().all()

    key = load_key(settings.emso_encryption_key)
    return VolunteerListResponse(
        items=[_to_response(v, key) for v in volunteers],
        total=total,
    )


@router.post(
    "",
    response_model=VolunteerResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_manager)],
)
async def create_volunteer(
    payload: VolunteerCreate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerResponse:
    """Register a new volunteer.  Encrypts EMŠO before storing."""
    # Single-tenant: resolve the one manager row.
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No manager configured — complete setup first.",
        )

    key = load_key(settings.emso_encryption_key)
    volunteer = Volunteer(
        first_name=payload.first_name,
        last_name=payload.last_name,
        street=payload.street,
        postal_code=payload.postal_code,
        city=payload.city,
        emso=encrypt_emso(payload.emso, key),
        phone=payload.phone,
        email=str(payload.email) if payload.email else None,
        manager_id=manager.id,
    )
    db.add(volunteer)
    try:
        await db.commit()
        await db.refresh(volunteer)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A volunteer with this phone number already exists.",
        )
    return _to_response(volunteer, key)


@router.patch(
    "/{volunteer_id}/deactivate",
    response_model=VolunteerResponse,
    dependencies=[Depends(require_manager)],
)
async def deactivate_volunteer(
    volunteer_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerResponse:
    """Soft-delete a volunteer by setting active=False."""
    volunteer = (
        await db.execute(select(Volunteer).where(Volunteer.id == volunteer_id))
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")

    volunteer.active = False
    await db.commit()
    await db.refresh(volunteer)

    key = load_key(settings.emso_encryption_key)
    return _to_response(volunteer, key)


@router.get("/{volunteer_id}", response_model=VolunteerDetailResponse)
async def get_volunteer(
    volunteer_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerDetailResponse:
    """Get a single volunteer with full log entry history (newest first)."""
    volunteer = (
        await db.execute(
            select(Volunteer)
            .where(Volunteer.id == volunteer_id)
            .options(selectinload(Volunteer.log_entries))
        )
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")

    key = load_key(settings.emso_encryption_key)
    return _to_detail_response(volunteer, key)
