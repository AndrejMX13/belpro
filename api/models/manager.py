"""Manager ORM model — one row per deployment (single-tenant)."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .volunteer import Volunteer


class Manager(Base):
    """NGO manager.  Single row expected per deployment."""

    __tablename__ = "managers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    ngo_name: Mapped[str] = mapped_column(String(255))
    ngo_street: Mapped[str] = mapped_column(String(255))
    ngo_postal_code: Mapped[str] = mapped_column(String(4))
    ngo_city: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )

    volunteers: Mapped[list[Volunteer]] = relationship(
        "Volunteer", back_populates="manager", lazy="select"
    )
