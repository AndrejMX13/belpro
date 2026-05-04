"""Manager ORM model — one row per deployment (single-tenant)."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, Text, text
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
    ngo_davcna: Mapped[str | None] = mapped_column(String(8), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(Text(), nullable=True)
    report_whatsapp: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    report_email: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"))
    default_report_whatsapp: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    default_report_email: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"))
    ngo_whatsapp_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    smtp_host: Mapped[str | None] = mapped_column(String(255), nullable=True)
    smtp_port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    smtp_user: Mapped[str | None] = mapped_column(String(255), nullable=True)
    smtp_from_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    evolution_api_admin_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )

    volunteers: Mapped[list[Volunteer]] = relationship(
        "Volunteer", back_populates="manager", lazy="select"
    )
