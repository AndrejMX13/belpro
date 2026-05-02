"""Manager authentication — HTTP Basic Auth.

Password priority:
  1. manager.password_hash in DB (set via the settings UI change-password flow)
  2. MANAGER_PASSWORD env var (initial / fallback when no hash is stored yet)
"""
from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import get_db
from services.password import verify_password

_security = HTTPBasic()


async def require_manager(
    credentials: Annotated[HTTPBasicCredentials, Depends(_security)],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """FastAPI dependency — rejects requests without the correct manager password.

    Checks the DB-stored scrypt hash first (set via UI).  Falls back to the
    MANAGER_PASSWORD env var for deployments that have never changed their
    password through the settings page.
    """
    from models.manager import Manager  # local import avoids circular dependency

    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()

    if manager and manager.password_hash:
        ok = verify_password(credentials.password, manager.password_hash)
    else:
        ok = secrets.compare_digest(
            credentials.password.encode("utf-8"),
            settings.manager_password.encode("utf-8"),
        )

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
