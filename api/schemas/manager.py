"""Pydantic schemas for the Manager entity."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
