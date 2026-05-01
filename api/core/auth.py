"""Manager authentication — HTTP Basic Auth using MANAGER_PASSWORD env var."""
from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.settings import Settings, get_settings

_security = HTTPBasic()


def require_manager(
    credentials: Annotated[HTTPBasicCredentials, Depends(_security)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    """FastAPI dependency — rejects requests without the correct manager password.

    Uses secrets.compare_digest to prevent timing-based side-channel attacks.
    The username field is ignored; only the password is verified.
    """
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
