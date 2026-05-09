"""Add manager_notified_at column to log_entries.

Revision ID: 008
Revises: 007
Create Date: 2026-05-08

Tracks when the manager was last notified about a pending entry.
Used to ensure only one active notification at a time.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE log_entries ADD COLUMN IF NOT EXISTS manager_notified_at TIMESTAMPTZ")
    op.execute("CREATE INDEX IF NOT EXISTS idx_entries_manager_notified ON log_entries (manager_notified_at)")


def downgrade() -> None:
    op.drop_index("idx_entries_manager_notified", table_name="log_entries")
    op.drop_column("log_entries", "manager_notified_at")
