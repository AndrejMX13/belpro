"""Add ngo_davcna column to managers.

Revision ID: 007
Revises: 006
Create Date: 2026-05-04

Adds one nullable column to managers:
  ngo_davcna — Slovenian 8-digit tax number (davčna številka)

Optional; existing rows get NULL.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add ngo_davcna column to managers."""
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS ngo_davcna VARCHAR(8)")


def downgrade() -> None:
    """Drop ngo_davcna column from managers."""
    op.drop_column("managers", "ngo_davcna")
