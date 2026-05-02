"""Volunteer ORM model."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .log_entry import LogEntry
    from .manager import Manager


class Volunteer(Base):
    """Registered volunteer.  Soft-deleted via active=False — never hard-deleted."""

    __tablename__ = "volunteers"
    __table_args__ = (
        Index("idx_volunteers_manager", "manager_id"),
        Index("idx_volunteers_active", "active"),
        Index("idx_volunteers_phone", "phone"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    # first_name used in informal WhatsApp messages; last_name in formal documents.
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(4))
    city: Mapped[str] = mapped_column(String(100))
    # Stores AES-256-GCM ciphertext (base64-encoded). Encryption handled in services/encryption.py.
    emso: Mapped[str] = mapped_column(Text)
    # HMAC-SHA256 of plaintext EMŠO — deterministic, used for uniqueness enforcement.
    emso_hash: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str | None] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"))
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    manager_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("managers.id", ondelete="RESTRICT")
    )

    manager: Mapped[Manager] = relationship(
        "Manager", back_populates="volunteers", lazy="select"
    )
    log_entries: Mapped[list[LogEntry]] = relationship(
        "LogEntry", back_populates="volunteer", lazy="select"
    )
