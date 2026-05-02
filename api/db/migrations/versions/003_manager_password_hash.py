"""Add password_hash column to managers table.

Revision ID: 003
Revises: 002
Create Date: 2026-05-02

Adds a nullable TEXT column for storing a scrypt-hashed password set via
the settings UI.  Nullable so existing rows are unaffected.  Auth falls back
to the MANAGER_PASSWORD env var when this column is NULL.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add password_hash to managers."""
    op.add_column("managers", sa.Column("password_hash", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove password_hash from managers."""
    op.drop_column("managers", "password_hash")
