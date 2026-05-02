"""LogEntryPhoto ORM model — one row per photo, many per log entry."""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .log_entry import LogEntry


class LogEntryPhoto(Base):
    """A photo attached to a log entry."""

    __tablename__ = "log_entry_photos"
    __table_args__ = (Index("idx_photos_entry", "log_entry_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    log_entry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("log_entries.id", ondelete="CASCADE"), nullable=False
    )
    photo_path: Mapped[str] = mapped_column(String(500))
    photo_exif_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    photo_exif_lat: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    photo_exif_lon: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )

    log_entry: Mapped[LogEntry] = relationship("LogEntry", back_populates="photos")
