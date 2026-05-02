"""Create log_entry_photos table; drop single-photo columns from log_entries.

Revision ID: 004
Revises: 003
Create Date: 2026-05-02

Replaces the four single-photo columns on log_entries (photo_path,
photo_exif_timestamp, photo_exif_lat, photo_exif_lon) with a dedicated
log_entry_photos table that allows many photos per entry.  All four columns
were always NULL — zero data loss.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create log_entry_photos; drop single-photo columns from log_entries."""
    op.create_table(
        "log_entry_photos",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "log_entry_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("log_entries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("photo_path", sa.String(500), nullable=False),
        sa.Column("photo_exif_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("photo_exif_lat", sa.Numeric(10, 7), nullable=True),
        sa.Column("photo_exif_lon", sa.Numeric(10, 7), nullable=True),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("idx_photos_entry", "log_entry_photos", ["log_entry_id"])

    op.drop_column("log_entries", "photo_path")
    op.drop_column("log_entries", "photo_exif_timestamp")
    op.drop_column("log_entries", "photo_exif_lat")
    op.drop_column("log_entries", "photo_exif_lon")


def downgrade() -> None:
    """Drop log_entry_photos; restore single-photo columns on log_entries."""
    op.drop_index("idx_photos_entry", table_name="log_entry_photos")
    op.drop_table("log_entry_photos")

    op.add_column("log_entries", sa.Column("photo_path", sa.String(500), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_timestamp", sa.DateTime(timezone=True), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_lat", sa.Numeric(10, 7), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_lon", sa.Numeric(10, 7), nullable=True))
