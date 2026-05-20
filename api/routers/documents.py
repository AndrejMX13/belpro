"""Documents router — downloadable compliance documents."""
from __future__ import annotations

import io
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.manager import Manager
from services.app_settings import AppSettings, get_app_settings
from services.consent_pdf import render_consent_pdf

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/consent-pdf", response_model=None, dependencies=[Depends(require_manager)])
async def download_consent_pdf(
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> StreamingResponse:
    """Generate and stream the GDPR Article 13 consent notice PDF."""
    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")
    pdf_bytes = render_consent_pdf(manager, settings.photo_retention_days)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="soglasje_gdpr.pdf"'},
    )
