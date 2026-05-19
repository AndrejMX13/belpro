"""Auth endpoints — login sets an httpOnly session cookie, logout clears it."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import _make_session_token, _verify_password
from core.settings import Settings, get_settings
from db.session import get_db
from schemas.auth import LoginRequest, LoginResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Verify manager password and set an httpOnly session cookie."""
    if not await _verify_password(body.password, settings, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Napačno geslo.",
        )
    token = _make_session_token(settings.api_secret_key)
    response.set_cookie(
        key="belpro_session",
        value=token,
        httponly=True,
        samesite="strict",
        secure=settings.cookie_secure,
        max_age=settings.session_duration_hours * 3600,
    )
    return LoginResponse(ok=True)


@router.post("/auth/logout", response_model=LoginResponse)
async def logout(response: Response) -> LoginResponse:
    """Clear the session cookie."""
    response.delete_cookie(key="belpro_session", samesite="strict")
    return LoginResponse(ok=True)
