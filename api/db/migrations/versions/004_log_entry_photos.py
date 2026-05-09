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
    op.execute("""
        CREATE TABLE IF NOT EXISTS log_entry_photos (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            log_entry_id UUID NOT NULL REFERENCES log_entries(id) ON DELETE CASCADE,
            photo_path VARCHAR(500) NOT NULL,
            photo_exif_timestamp TIMESTAMPTZ,
            photo_exif_lat NUMERIC(10, 7),
            photo_exif_lon NUMERIC(10, 7),
            uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_photos_entry ON log_entry_photos (log_entry_id)
    """)

    op.execute("ALTER TABLE log_entries DROP COLUMN IF EXISTS photo_path")
    op.execute("ALTER TABLE log_entries DROP COLUMN IF EXISTS photo_exif_timestamp")
    op.execute("ALTER TABLE log_entries DROP COLUMN IF EXISTS photo_exif_lat")
    op.execute("ALTER TABLE log_entries DROP COLUMN IF EXISTS photo_exif_lon")


def downgrade() -> None:
    """Drop log_entry_photos; restore single-photo columns on log_entries."""
    op.drop_index("idx_photos_entry", table_name="log_entry_photos")
    op.drop_table("log_entry_photos")

    op.add_column("log_entries", sa.Column("photo_path", sa.String(500), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_timestamp", sa.DateTime(timezone=True), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_lat", sa.Numeric(10, 7), nullable=True))
    op.add_column("log_entries", sa.Column("photo_exif_lon", sa.Numeric(10, 7), nullable=True))
