"""Logo router — public GET + authenticated POST and DELETE."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse

from core.auth import require_manager
from services.logo import LOGO_PATH, delete_logo, logo_exists, save_logo

router = APIRouter(prefix="/logo", tags=["logo"])


@router.get("")
async def get_logo() -> FileResponse:
    """Return the NGO logo as PNG, or 404 if none has been uploaded."""
    if not logo_exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logo ni naložen.")
    return FileResponse(str(LOGO_PATH), media_type="image/png")


@router.post("", status_code=status.HTTP_204_NO_CONTENT, response_model=None, dependencies=[Depends(require_manager)])
async def upload_logo(file: UploadFile = File(...)) -> Response:
    """Upload or replace the NGO logo. Accepts JPEG, PNG, WebP, GIF, BMP, TIFF."""
    data = await file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datoteka je prazna.")
    try:
        save_logo(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_model=None, dependencies=[Depends(require_manager)])
async def remove_logo() -> Response:
    """Delete the current NGO logo."""
    if not logo_exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logo ni naložen.")
    delete_logo()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
