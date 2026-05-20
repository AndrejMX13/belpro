"""Log entries CRUD router — volunteer work diary entries."""
from __future__ import annotations

import base64 as b64
import io
import uuid
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi import status as http_status
from fastapi.responses import FileResponse, Response
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

import logging

from core.auth import require_manager
from db.session import get_db
from services.app_settings import AppSettings, get_app_settings
from models.log_entry import EntryStatus, LogEntry
from models.log_entry_photo import LogEntryPhoto
from models.manager import Manager
from models.volunteer import Volunteer
from schemas.log_entry import LogEntryCreate, LogEntryListResponse, LogEntryResponse, LogEntryUpdate
from schemas.log_entry import PhotoBase64Request, PhotoResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/log-entries", tags=["log-entries"])




_PHOTOS_ROOT = Path("/app/photos")
_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _extract_exif(content: bytes) -> tuple[datetime | None, Decimal | None, Decimal | None]:
    """Extract timestamp and GPS from image EXIF. All best-effort — never raises."""
    try:
        import piexif
        from PIL import Image

        with Image.open(io.BytesIO(content)) as img:
            raw = img.info.get("exif")
        if not raw:
            return None, None, None
        d = piexif.load(raw)

        ts = None
        dt_bytes = d.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal)
        if dt_bytes:
            try:
                ts = datetime.strptime(
                    dt_bytes.decode("ascii", errors="ignore"), "%Y:%m:%d %H:%M:%S"
                ).replace(tzinfo=UTC)
            except ValueError:
                pass

        lat = lon = None
        gps = d.get("GPS", {})
        if gps:
            def _rat(r: tuple[int, int]) -> float:
                return r[0] / r[1] if r[1] else 0.0

            def _dms(dms: tuple, ref: bytes) -> Decimal | None:
                try:
                    val = _rat(dms[0]) + _rat(dms[1]) / 60 + _rat(dms[2]) / 3600
                    if ref in (b"S", b"W"):
                        val = -val
                    return Decimal(str(round(val, 7)))
                except Exception:
                    return None

            lat_d = gps.get(piexif.GPSIFD.GPSLatitude)
            lat_r = gps.get(piexif.GPSIFD.GPSLatitudeRef)
            lon_d = gps.get(piexif.GPSIFD.GPSLongitude)
            lon_r = gps.get(piexif.GPSIFD.GPSLongitudeRef)
            if lat_d and lat_r and lon_d and lon_r:
                lat = _dms(lat_d, lat_r)
                lon = _dms(lon_d, lon_r)

        return ts, lat, lon
    except Exception:
        return None, None, None


@router.get("", response_model=LogEntryListResponse, dependencies=[Depends(require_manager)])
async def list_log_entries(
    volunteer_id: uuid.UUID | None = Query(default=None),
    status: EntryStatus | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    date_field: Literal["work_date", "created_at"] = Query(default="work_date"),
    search_q: str | None = Query(default=None, max_length=200),
    sort_by: Literal["work_date", "hours", "created_at", "status", "activity_description", "location"] = Query(default="work_date"),
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
    date_col = LogEntry.work_date if date_field == "work_date" else LogEntry.created_at
    if date_from is not None:
        stmt = stmt.where(date_col >= date_from)
        count_stmt = count_stmt.where(date_col >= date_from)
    if date_to is not None:
        stmt = stmt.where(date_col <= date_to)
        count_stmt = count_stmt.where(date_col <= date_to)
    if search_q is not None:
        pattern = f"%{search_q}%"
        search_filter = or_(
            LogEntry.activity_description.ilike(pattern),
            LogEntry.location.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    col = getattr(LogEntry, sort_by)
    stmt = stmt.order_by(col.asc() if sort_dir == "asc" else col.desc())
    stmt = stmt.offset(offset).limit(limit)

    total = (await db.execute(count_stmt)).scalar_one()
    rows = (await db.execute(stmt)).scalars().all()
    return LogEntryListResponse(items=list(rows), total=total)


@router.get("/photo-limit")
async def get_photo_limit(
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> dict:
    """Return the configured maximum photos per log entry. Used by n8n workflows."""
    return {"max_photos": settings.max_photos_per_entry}


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
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
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
            detail="Ne najdem prostovoljca",
        )
    if not volunteer.active:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Neaktivnemu prostovoljcu ni mogoče dodati vnosa.",
        )

    entry = LogEntry(
        volunteer_id=payload.volunteer_id,
        work_date=payload.work_date,
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
    "/{entry_id}",
    response_model=LogEntryResponse,
    dependencies=[Depends(require_manager)],
)
async def update_log_entry(
    entry_id: uuid.UUID,
    payload: LogEntryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Update activity_description, hours, location, and/or work_date. Blocked once approved."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status == EntryStatus.APPROVED:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Odobrenega vnosa ni mogoče urejati.",
        )
    if payload.activity_description is not None:
        entry.activity_description = payload.activity_description
    if payload.hours is not None:
        entry.hours = payload.hours
    # location is nullable, so model_fields_set distinguishes "not sent" from "explicitly cleared to null"
    if 'location' in payload.model_fields_set:
        entry.location = payload.location
    if payload.work_date is not None:
        entry.work_date = payload.work_date
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.post(
    "/{entry_id}/photos",
    response_model=PhotoResponse,
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(require_manager)],
)
async def upload_photo(
    entry_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[AppSettings, Depends(get_app_settings)] = ...,
) -> PhotoResponse:
    """Upload a photo for a log entry. Blocked if entry is approved."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status == EntryStatus.APPROVED:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Odobrenega vnosa ni mogoče urejati.",
        )

    max_photos = settings.max_photos_per_entry
    existing_count = (
        await db.execute(
            select(func.count()).where(LogEntryPhoto.log_entry_id == entry_id)
        )
    ).scalar()
    if existing_count >= max_photos:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos že vsebuje {existing_count} od {max_photos} dovoljenih slik. Nova slika ni bila dodana.",
        )

    ext = Path(file.filename or "").suffix.lower()
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Nepodprt format. Dovoljeni: jpg, jpeg, png, webp, gif.",
        )

    content = await file.read()
    photo_id = uuid.uuid4()
    dir_path = _PHOTOS_ROOT / str(entry_id)
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / f"{photo_id}{ext}").write_bytes(content)

    ts, lat, lon = _extract_exif(content)
    photo = LogEntryPhoto(
        id=photo_id,
        log_entry_id=entry_id,
        photo_path=f"{entry_id}/{photo_id}{ext}",
        photo_exif_timestamp=ts,
        photo_exif_lat=lat,
        photo_exif_lon=lon,
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    count_q = select(func.count()).select_from(LogEntryPhoto).where(
        LogEntryPhoto.log_entry_id == entry_id
    )
    photo_count_val: int = (await db.execute(count_q)).scalar() or 0
    resp = PhotoResponse.model_validate(photo)
    resp.photo_count = photo_count_val
    resp.max_photos = settings.max_photos_per_entry
    return resp


@router.post(
    "/{entry_id}/photos/base64",
    response_model=PhotoResponse,
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(require_manager)],
)
async def upload_photo_base64(
    entry_id: uuid.UUID,
    body: PhotoBase64Request,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
    settings: Annotated[AppSettings, Depends(get_app_settings)] = ...,
) -> PhotoResponse:
    """Upload a photo from a base64-encoded string. Used by n8n workflows."""
    entry = (
        await db.execute(
            select(LogEntry).where(LogEntry.id == entry_id).with_for_update()
        )
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status == EntryStatus.APPROVED:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Odobrenega vnosa ni mogoče urejati.",
        )

    max_photos = settings.max_photos_per_entry
    existing_count = (
        await db.execute(
            select(func.count()).where(LogEntryPhoto.log_entry_id == entry_id)
        )
    ).scalar()
    if existing_count >= max_photos:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos že vsebuje {existing_count} od {max_photos} dovoljenih slik. Nova slika ni bila dodana.",
        )

    ext = Path(body.filename or "").suffix.lower()
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Nepodprt format. Dovoljeni: jpg, jpeg, png, webp, gif.",
        )

    try:
        content = b64.b64decode(body.image_base64)
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Neveljaven base64 podatkovni niz.",
        )

    photo_id = uuid.uuid4()
    dir_path = _PHOTOS_ROOT / str(entry_id)
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / f"{photo_id}{ext}").write_bytes(content)

    ts, lat, lon = _extract_exif(content)
    photo = LogEntryPhoto(
        id=photo_id,
        log_entry_id=entry_id,
        photo_path=f"{entry_id}/{photo_id}{ext}",
        photo_exif_timestamp=ts,
        photo_exif_lat=lat,
        photo_exif_lon=lon,
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    count_q = select(func.count()).select_from(LogEntryPhoto).where(
        LogEntryPhoto.log_entry_id == entry_id
    )
    photo_count: int = (await db.execute(count_q)).scalar() or 0
    resp = PhotoResponse.model_validate(photo)
    resp.photo_count = photo_count
    resp.max_photos = max_photos
    return resp


@router.get(
    "/{entry_id}/photos/{photo_id}/file",
    dependencies=[Depends(require_manager)],
)
async def get_photo_file(
    entry_id: uuid.UUID,
    photo_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> FileResponse:
    """Serve a photo file with authentication."""
    photo = (
        await db.execute(
            select(LogEntryPhoto).where(
                LogEntryPhoto.id == photo_id,
                LogEntryPhoto.log_entry_id == entry_id,
            )
        )
    ).scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem slike")
    file_path = _PHOTOS_ROOT / photo.photo_path
    if not file_path.exists():
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Datoteke s sliko ni na disku")
    return FileResponse(str(file_path))


@router.delete(
    "/{entry_id}/photos/{photo_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_manager)],
)
async def delete_photo(
    entry_id: uuid.UUID,
    photo_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> Response:
    """Delete a photo. Blocked if entry is approved."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status == EntryStatus.APPROVED:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Odobrenega vnosa ni mogoče urejati.",
        )
    photo = (
        await db.execute(
            select(LogEntryPhoto).where(
                LogEntryPhoto.id == photo_id,
                LogEntryPhoto.log_entry_id == entry_id,
            )
        )
    ).scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem slike")

    try:
        (_PHOTOS_ROOT / photo.photo_path).unlink(missing_ok=True)
    except Exception:
        pass

    await db.delete(photo)
    await db.commit()
    return Response(status_code=http_status.HTTP_204_NO_CONTENT)


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
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status != EntryStatus.PENDING_MANAGER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_manager (trenutni status: {entry.status.value}).",
        )
    entry.status = EntryStatus.APPROVED
    entry.manager_approved_at = datetime.now(UTC)
    entry.manager_notified_at = None
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
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status != EntryStatus.PENDING_MANAGER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_manager (trenutni status: {entry.status.value}).",
        )
    entry.status = EntryStatus.REJECTED
    entry.manager_approved_at = datetime.now(UTC)
    entry.manager_notified_at = None
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.patch(
    "/{entry_id}/notify",
    response_model=LogEntryResponse,
    dependencies=[Depends(require_manager)],
)
async def notify_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Mark a pending_manager entry as notified (sets manager_notified_at).

    Only one entry should have manager_notified_at set at a time.
    The caller (n8n) must check no other entry is already notified before calling this.
    """
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status != EntryStatus.PENDING_MANAGER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_manager (trenutni status: {entry.status.value}).",
        )
    entry.manager_notified_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.post(
    "/{entry_id}/confirm",
    response_model=LogEntryResponse,
    dependencies=[Depends(require_manager)],
)
async def confirm_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Volunteer confirmed the entry. Transitions pending_volunteer → pending_manager."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status != EntryStatus.PENDING_VOLUNTEER:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnos ni v statusu pending_volunteer (trenutni status: {entry.status.value}).",
        )
    entry.status = EntryStatus.PENDING_MANAGER
    entry.volunteer_confirmed_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)


@router.delete(
    "/{entry_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(require_manager)],
)
async def delete_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> None:
    """Delete a pending_volunteer or pending_manager log entry and its associated photo files."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status not in (EntryStatus.PENDING_VOLUNTEER, EntryStatus.PENDING_MANAGER):
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnosa v statusu '{entry.status.value}' ni mogoče izbrisati.",
        )

    photos = (
        await db.execute(select(LogEntryPhoto).where(LogEntryPhoto.log_entry_id == entry_id))
    ).scalars().all()
    for photo in photos:
        try:
            (_PHOTOS_ROOT / photo.photo_path).unlink(missing_ok=True)
        except Exception:
            pass
    try:
        (_PHOTOS_ROOT / str(entry_id)).rmdir()
    except Exception:
        pass

    await db.delete(entry)
    await db.commit()
