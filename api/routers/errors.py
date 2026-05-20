"""Error log router — write endpoint for internal services, read endpoints for manager."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.error_log import ErrorLog
from schemas.error_log import ErrorLogCreate, ErrorLogResponse, UnacknowledgedCountResponse

router = APIRouter(prefix="/errors", tags=["errors"])


def _require_internal_key(x_internal_key: Annotated[str | None, Header()] = None) -> None:
    """Validate X-Internal-Key header against API_SECRET_KEY."""
    if x_internal_key != get_settings().api_secret_key:
        raise HTTPException(status_code=401, detail="Invalid internal key.")


@router.post(
    "",
    response_model=ErrorLogResponse,
    status_code=201,
    dependencies=[Depends(_require_internal_key)],
)
async def write_error(
    body: ErrorLogCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ErrorLogResponse:
    """Record an operational failure. Called by API exception handlers, n8n, and the ops sidecar."""
    row = ErrorLog(
        service=body.service,
        operation=body.operation,
        message=body.message,
        detail=body.detail,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return ErrorLogResponse.model_validate(row)


@router.get(
    "/unacknowledged-count",
    response_model=UnacknowledgedCountResponse,
    dependencies=[Depends(require_manager)],
)
async def unacknowledged_count(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UnacknowledgedCountResponse:
    """Return count of unacknowledged errors. Used by nav badge."""
    count = (
        await db.execute(
            select(func.count()).where(ErrorLog.acknowledged.is_(False))
        )
    ).scalar_one()
    return UnacknowledgedCountResponse(count=count)


@router.get(
    "",
    response_model=list[ErrorLogResponse],
    dependencies=[Depends(require_manager)],
)
async def list_errors(
    db: Annotated[AsyncSession, Depends(get_db)],
    unacknowledged: bool = Query(False),
) -> list[ErrorLogResponse]:
    """List error log entries, newest first. Optionally filter to unacknowledged only."""
    q = select(ErrorLog).order_by(ErrorLog.created_at.desc())
    if unacknowledged:
        q = q.where(ErrorLog.acknowledged.is_(False))
    rows = (await db.execute(q)).scalars().all()
    return [ErrorLogResponse.model_validate(r) for r in rows]


@router.patch(
    "/{error_id}/acknowledge",
    response_model=ErrorLogResponse,
    dependencies=[Depends(require_manager)],
)
async def acknowledge_error(
    error_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ErrorLogResponse:
    """Mark an error as acknowledged (read by manager)."""
    row = (
        await db.execute(select(ErrorLog).where(ErrorLog.id == error_id))
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Error record not found.")
    row.acknowledged = True
    await db.commit()
    await db.refresh(row)
    return ErrorLogResponse.model_validate(row)
