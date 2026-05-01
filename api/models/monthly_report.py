"""MonthlyReport ORM model — tracks generated PDF reports."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, SmallInteger, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .volunteer import Volunteer


class MonthlyReport(Base):
    """Tracks generated PDF reports for audit and re-delivery purposes.

    volunteer_id is NULL for the consolidated manager report covering all volunteers.
    """

    __tablename__ = "monthly_reports"
    __table_args__ = (
        CheckConstraint("period_month BETWEEN 1 AND 12", name="ck_reports_month"),
        Index("idx_reports_volunteer", "volunteer_id"),
        Index("idx_reports_period", "period_year", "period_month"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    # NULL → consolidated manager report for all volunteers
    volunteer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("volunteers.id", ondelete="RESTRICT")
    )
    period_year: Mapped[int] = mapped_column(SmallInteger)
    period_month: Mapped[int] = mapped_column(SmallInteger)
    pdf_path: Mapped[str] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    volunteer: Mapped[Volunteer | None] = relationship(
        "Volunteer", lazy="select", foreign_keys=[volunteer_id]
    )
