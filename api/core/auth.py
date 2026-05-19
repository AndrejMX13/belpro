"""Manager authentication — httpOnly session cookie with Basic Auth fallback.

Auth priority on every protected request:
  1. belpro_session httpOnly cookie (signed with API_SECRET_KEY)
  2. HTTP Basic Auth (Authorization header) — used by n8n and scripts

Password verification priority:
  1. manager.password_hash in DB (set via the settings UI)
  2. MANAGER_PASSWORD env var (initial / fallback)
"""
from __future__ import annotations

import secrets
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import get_db
from services.password import verify_password

_security = HTTPBasic(auto_error=False)


def _make_session_token(secret_key: str) -> str:
    """Create a signed, self-expiring session token."""
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps({"sub": "manager"})


def _verify_session_token(token: str, secret_key: str, duration_hours: int) -> bool:
    """Return True if the token signature is valid and not expired."""
    if not token:
        return False
    s = URLSafeTimedSerializer(secret_key)
    try:
        s.loads(token, max_age=duration_hours * 3600)
        return True
    except (BadSignature, SignatureExpired):
        return False


async def _verify_password(
    password: str,
    settings: Settings,
    db: AsyncSession,
) -> bool:
    """Verify password against DB hash or env var fallback."""
    from models.manager import Manager  # local import avoids circular dependency

    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()

    if manager and manager.password_hash:
        return verify_password(password, manager.password_hash)
    return secrets.compare_digest(
        password.encode("utf-8"),
        settings.manager_password.encode("utf-8"),
    )


async def require_manager(
    request: Request,
    credentials: Annotated[Optional[HTTPBasicCredentials], Depends(_security)],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Reject requests without a valid session cookie or Basic Auth credentials."""
    # 1. Cookie path (browser dashboard)
    session_cookie = request.cookies.get("belpro_session")
    if session_cookie and _verify_session_token(
        session_cookie, settings.api_secret_key, settings.session_duration_hours
    ):
        return

    # 2. Basic Auth fallback (n8n, scripts)
    if credentials and await _verify_password(credentials.password, settings, db):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nepravilni podatki za prijavo.",
    )
