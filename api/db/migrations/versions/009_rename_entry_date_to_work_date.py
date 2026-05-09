"""Rename entry_date to work_date in log_entries.

'work_date' is clearer than 'entry_date' and prevents confusion with
'created_at' (submission timestamp). Also renames associated indexes.

Revision ID: 009
Revises: 008
Create Date: 2026-05-09
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename entry_date to work_date and update index names."""
    op.alter_column("log_entries", "entry_date", new_column_name="work_date")
    op.execute("ALTER INDEX idx_entries_date RENAME TO idx_entries_work_date")
    op.execute("ALTER INDEX idx_entries_vol_date RENAME TO idx_entries_vol_work_date")


def downgrade() -> None:
    """Reverse rename: work_date back to entry_date and restore index names."""
    op.alter_column("log_entries", "work_date", new_column_name="entry_date")
    op.execute("ALTER INDEX idx_entries_work_date RENAME TO idx_entries_date")
    op.execute("ALTER INDEX idx_entries_vol_work_date RENAME TO idx_entries_vol_date")
