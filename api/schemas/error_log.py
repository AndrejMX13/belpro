"""Pydantic schemas for the error_log endpoint."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class ErrorLogCreate(BaseModel):
    """Payload sent by internal services (API, n8n, ops sidecar)."""

    service: str
    operation: str
    message: str
    detail: str | None = None


class ErrorLogResponse(BaseModel):
    """Single error log row returned to the dashboard."""

    id: uuid.UUID
    service: str
    operation: str
    message: str
    detail: str | None
    acknowledged: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UnacknowledgedCountResponse(BaseModel):
    count: int
