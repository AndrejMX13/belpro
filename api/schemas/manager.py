"""Pydantic schemas for the Manager entity."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ManagerCreate(BaseModel):
    """Fields required for first-time manager setup."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    phone: Annotated[str, Field(min_length=1, max_length=30)]
    email: EmailStr
    ngo_name: Annotated[str, Field(min_length=1, max_length=200)]
    ngo_street: Annotated[str, Field(min_length=1, max_length=255)]
    ngo_postal_code: Annotated[str, Field(pattern=r"^\d{4}$")]
    ngo_city: Annotated[str, Field(min_length=1, max_length=100)]


class ManagerResponse(BaseModel):
    """Manager profile returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    first_name: str
    last_name: str
    phone: str
    email: str
    ngo_name: str
    ngo_street: str
    ngo_postal_code: str
    ngo_city: str
    created_at: datetime
