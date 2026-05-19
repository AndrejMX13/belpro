"""Schemas for the auth endpoints."""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Body for POST /api/auth/login."""

    password: str


class LoginResponse(BaseModel):
    """Response for login and logout endpoints."""

    ok: bool
