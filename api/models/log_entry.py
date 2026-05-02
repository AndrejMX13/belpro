"""LogEntry ORM model — core audit trail for volunteer work diary entries."""
from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .log_entry_photo import LogEntryPhoto
    from .volunteer import Volunteer


class EntryStatus(str, enum.Enum):
    """Volunteer diary entry status.  Flows one way only — never backwards."""

    PENDING_VOLUNTEER = "pending_volunteer"
    PENDING_MANAGER = "pending_manager"
    APPROVED = "approved"
    REJECTED = "rejected"


class LogEntry(Base):
    """Individual work diary entry submitted by a volunteer."""

    __tablename__ = "log_entries"
    __table_args__ = (
        Index("idx_entries_volunteer", "volunteer_id"),
        Index("idx_entries_status", "status"),
        Index("idx_entries_date", "entry_date"),
        Index("idx_entries_location", "location"),
        Index("idx_entries_created", "created_at"),
        Index("idx_entries_vol_date", "volunteer_id", "entry_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    volunteer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("volunteers.id", ondelete="RESTRICT")
    )
    entry_date: Mapped[date] = mapped_column(Date)
    activity_description: Mapped[str] = mapped_column(Text)
    raw_transcript: Mapped[str | None] = mapped_column(Text)
    hours: Mapped[Decimal] = mapped_column(Numeric(4, 1))
    location: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[EntryStatus] = mapped_column(
        # create_type=False — the 'entry_status' enum already exists via init.sql
        # values_callable — use .value ("approved") not .name ("APPROVED") for DB binding
        SAEnum(EntryStatus, name="entry_status", create_type=False, values_callable=lambda objs: [e.value for e in objs]),
        server_default="pending_volunteer",
    )
    volunteer_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    manager_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    # updated_at is maintained by the trg_entries_updated_at DB trigger — no onupdate needed here.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )

    volunteer: Mapped[Volunteer] = relationship(
        "Volunteer", back_populates="log_entries", lazy="select"
    )
    photos: Mapped[list[LogEntryPhoto]] = relationship(
        "LogEntryPhoto", back_populates="log_entry", lazy="selectin", cascade="all, delete-orphan"
    )
