"""Volunteers CRUD router."""
from __future__ import annotations

import calendar
import uuid
from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.auth import require_manager
from core.settings import Settings, get_settings
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.manager import Manager
from models.volunteer import Volunteer
from schemas.volunteer import (
    EmsoCheckRequest,
    EmsoCheckResponse,
    VolunteerCreate,
    VolunteerDetailResponse,
    VolunteerListResponse,
    VolunteerResponse,
    VolunteerUpdate,
)
from services.encryption import decrypt_emso, encrypt_emso, hash_emso, load_key, mask_emso

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

# Columns allowed as sort targets — explicit whitelist prevents injection via query param.
_SORTABLE = frozenset({"last_name", "first_name", "registered_at", "city"})


def _to_response(volunteer: Volunteer, key: bytes, hours_this_month: float = 0.0) -> VolunteerResponse:
    """Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object."""
    masked = mask_emso(decrypt_emso(volunteer.emso, key))
    return VolunteerResponse(
        id=volunteer.id,
        first_name=volunteer.first_name,
        last_name=volunteer.last_name,
        street=volunteer.street,
        postal_code=volunteer.postal_code,
        city=volunteer.city,
        emso_masked=masked,
        phone=volunteer.phone,
        email=volunteer.email,
        active=volunteer.active,
        registered_at=volunteer.registered_at,
        manager_id=volunteer.manager_id,
        hours_this_month=hours_this_month,
        report_whatsapp=volunteer.report_whatsapp,
        report_email=volunteer.report_email,
    )


def _to_detail_response(volunteer: Volunteer, key: bytes) -> VolunteerDetailResponse:
    """Same as _to_response but includes sorted log_entries and computed hours for the current month."""
    masked = mask_emso(decrypt_emso(volunteer.emso, key))
    volunteer.log_entries.sort(key=lambda e: e.entry_date, reverse=True)
    today = date.today()
    hours_this_month = float(sum(
        e.hours for e in volunteer.log_entries
        if e.status == EntryStatus.APPROVED
        and e.entry_date.year == today.year
        and e.entry_date.month == today.month
    ))
    return VolunteerDetailResponse(
        id=volunteer.id,
        first_name=volunteer.first_name,
        last_name=volunteer.last_name,
        street=volunteer.street,
        postal_code=volunteer.postal_code,
        city=volunteer.city,
        emso_masked=masked,
        phone=volunteer.phone,
        email=volunteer.email,
        active=volunteer.active,
        registered_at=volunteer.registered_at,
        manager_id=volunteer.manager_id,
        hours_this_month=hours_this_month,
        report_whatsapp=volunteer.report_whatsapp,
        report_email=volunteer.report_email,
        log_entries=volunteer.log_entries,
    )


@router.get("", response_model=VolunteerListResponse)
async def list_volunteers(
    active: bool | None = Query(default=None, description="True=active only, False=inactive, omit=all"),
    search_by: Literal["first_name", "last_name", "name", "city", "phone"] | None = Query(default=None),
    search_q: str | None = Query(default=None, description="Case-insensitive partial match"),
    registered_after: date | None = Query(default=None),
    registered_before: date | None = Query(default=None),
    sort_by: Literal["last_name", "first_name", "registered_at", "city", "phone", "active"] = Query(default="last_name"),
    sort_dir: Literal["asc", "desc"] = Query(default="asc"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerListResponse:
    """List volunteers with optional filters, sorting, and pagination."""
    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    hours_subq = (
        select(func.coalesce(func.sum(LogEntry.hours), 0))
        .where(
            LogEntry.volunteer_id == Volunteer.id,
            LogEntry.status == EntryStatus.APPROVED,
            LogEntry.entry_date >= first_day,
            LogEntry.entry_date <= last_day,
        )
        .correlate(Volunteer)
        .scalar_subquery()
    )

    stmt = select(Volunteer, hours_subq.label("hours_this_month"))
    count_stmt = select(func.count()).select_from(Volunteer)

    if active is not None:
        stmt = stmt.where(Volunteer.active == active)
        count_stmt = count_stmt.where(Volunteer.active == active)
    if search_by and search_q:
        q = f"%{search_q}%"
        _SEARCH_COL = {
            "first_name": Volunteer.first_name,
            "last_name":  Volunteer.last_name,
            "city":       Volunteer.city,
            "phone":      Volunteer.phone,
        }
        if search_by == "name":
            cond = or_(Volunteer.first_name.ilike(q), Volunteer.last_name.ilike(q))
        else:
            cond = _SEARCH_COL[search_by].ilike(q)
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)
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
    rows = (await db.execute(stmt)).all()

    key = load_key(settings.emso_encryption_key)
    return VolunteerListResponse(
        items=[_to_response(v, key, float(h)) for v, h in rows],
        total=total,
    )


@router.post(
    "/check-emso",
    response_model=EmsoCheckResponse,
    dependencies=[Depends(require_manager)],
)
async def check_emso(
    payload: EmsoCheckRequest,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> EmsoCheckResponse:
    """Check whether an EMŠO is already registered.  Used by the frontend before form submit."""
    key = load_key(settings.emso_encryption_key)
    emso_h = hash_emso(payload.emso, key)
    existing = (
        await db.execute(select(Volunteer).where(Volunteer.emso_hash == emso_h))
    ).scalar_one_or_none()
    return EmsoCheckResponse(exists=existing is not None)


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

    emso_h = hash_emso(payload.emso, key)
    existing = (
        await db.execute(select(Volunteer).where(Volunteer.emso_hash == emso_h))
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Prostovoljec s tem EMŠO-jem že obstaja.",
        )

    volunteer = Volunteer(
        first_name=payload.first_name,
        last_name=payload.last_name,
        street=payload.street,
        postal_code=payload.postal_code,
        city=payload.city,
        emso=encrypt_emso(payload.emso, key),
        emso_hash=emso_h,
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
            detail="Prostovoljec s to telefonsko številko že obstaja.",
        )
    return _to_response(volunteer, key)


@router.patch(
    "/{volunteer_id}/activate",
    response_model=VolunteerResponse,
    dependencies=[Depends(require_manager)],
)
async def activate_volunteer(
    volunteer_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
) -> VolunteerResponse:
    """Re-activate a previously deactivated volunteer."""
    volunteer = (
        await db.execute(select(Volunteer).where(Volunteer.id == volunteer_id))
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")

    volunteer.active = True
    await db.commit()
    await db.refresh(volunteer)

    key = load_key(settings.emso_encryption_key)
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


@router.delete(
    "/{volunteer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_manager)],
)
async def delete_volunteer(
    volunteer_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> Response:
    """Hard-delete a volunteer only if they have zero log entries."""
    volunteer = (
        await db.execute(
            select(Volunteer)
            .where(Volunteer.id == volunteer_id)
            .options(selectinload(Volunteer.log_entries))
        )
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")
    if volunteer.log_entries:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Prostovoljca z vnosi ni mogoče izbrisati. Namesto tega ga deaktivirajte.",
        )
    await db.delete(volunteer)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.patch("/{volunteer_id}", response_model=VolunteerResponse)
async def update_volunteer(
    volunteer_id: uuid.UUID,
    payload: VolunteerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[Settings, Depends(get_settings)] = ...,
    _manager: Annotated[Manager, Depends(require_manager)] = ...,
) -> VolunteerResponse:
    """Update mutable fields on a volunteer (report channel preferences)."""
    volunteer = (
        await db.execute(select(Volunteer).where(Volunteer.id == volunteer_id))
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(volunteer, field, value)

    await db.commit()
    await db.refresh(volunteer)

    key = load_key(settings.emso_encryption_key)
    return _to_response(volunteer, key)
