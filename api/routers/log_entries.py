"""Log entries CRUD router — volunteer work diary entries."""
from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.volunteer import Volunteer
from schemas.log_entry import LogEntryCreate, LogEntryListResponse, LogEntryResponse

router = APIRouter(prefix="/log-entries", tags=["log-entries"])


@router.get("", response_model=LogEntryListResponse, dependencies=[Depends(require_manager)])
async def list_log_entries(
    volunteer_id: uuid.UUID | None = Query(default=None),
    status: EntryStatus | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    sort_by: Literal["entry_date", "hours", "created_at", "status"] = Query(default="entry_date"),
    sort_dir: Literal["asc", "desc"] = Query(default="desc"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryListResponse:
    """List log entries with optional filters, sorting, and pagination."""
    stmt = select(LogEntry)
    count_stmt = select(func.count()).select_from(LogEntry)

    if volunteer_id is not None:
        stmt = stmt.where(LogEntry.volunteer_id == volunteer_id)
        count_stmt = count_stmt.where(LogEntry.volunteer_id == volunteer_id)
    if status is not None:
        stmt = stmt.where(LogEntry.status == status)
        count_stmt = count_stmt.where(LogEntry.status == status)
    if date_from is not None:
        stmt = stmt.where(LogEntry.entry_date >= date_from)
        count_stmt = count_stmt.where(LogEntry.entry_date >= date_from)
    if date_to is not None:
        stmt = stmt.where(LogEntry.entry_date <= date_to)
        count_stmt = count_stmt.where(LogEntry.entry_date <= date_to)

    col = getattr(LogEntry, sort_by)
    stmt = stmt.order_by(col.asc() if sort_dir == "asc" else col.desc())
    stmt = stmt.offset(offset).limit(limit)

    total = (await db.execute(count_stmt)).scalar_one()
    rows = (await db.execute(stmt)).scalars().all()
    return LogEntryListResponse(items=list(rows), total=total)


@router.get("/{entry_id}", response_model=LogEntryResponse, dependencies=[Depends(require_manager)])
async def get_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Get a single log entry by ID."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    return LogEntryResponse.model_validate(entry)


@router.post(
    "",
    response_model=LogEntryResponse,
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(require_manager)],
)
async def create_log_entry(
    payload: LogEntryCreate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Create a new log entry.  Volunteer must exist and be active."""
    volunteer = (
        await db.execute(select(Volunteer).where(Volunteer.id == payload.volunteer_id))
    ).scalar_one_or_none()
    if volunteer is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Volunteer not found",
        )
    if not volunteer.active:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Neaktivnemu prostovoljcu ni mogoče dodati vnosa.",
        )

    entry = LogEntry(
        volunteer_id=payload.volunteer_id,
        entry_date=payload.entry_date,
        activity_description=payload.activity_description,
        hours=payload.hours,
        location=payload.location,
        raw_transcript=payload.raw_transcript,
        status=payload.status,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.patch(
    "/{entry_id}/approve",
    response_model=LogEntryResponse,
    dependencies=[Depends(require_manager)],
)
async def approve_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Approve a pending_manager log entry."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    if entry.status != EntryStatus.PENDING_MANAGER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_manager (trenutni status: {entry.status.value}).",
        )
    entry.status = EntryStatus.APPROVED
    entry.manager_approved_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.patch(
    "/{entry_id}/reject",
    response_model=LogEntryResponse,
    dependencies=[Depends(require_manager)],
)
async def reject_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Reject a pending_manager log entry."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    if entry.status != EntryStatus.PENDING_MANAGER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_manager (trenutni status: {entry.status.value}).",
        )
    entry.status = EntryStatus.REJECTED
    entry.manager_approved_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)
