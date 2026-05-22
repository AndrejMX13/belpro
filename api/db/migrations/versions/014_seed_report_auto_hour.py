"""Seed report_auto_hour setting row.

Revision ID: 014
Revises: 013
Create Date: 2026-05-22
"""
from __future__ import annotations
from typing import Sequence, Union
from alembic import op

revision: str = "014"
down_revision: Union[str, None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the report_auto_hour settings row with default value 7."""
    op.execute(
        "INSERT INTO settings (name, type, value) "
        "VALUES ('report_auto_hour', 'int', '7') "
        "ON CONFLICT (name) DO NOTHING"
    )


def downgrade() -> None:
    """Remove the report_auto_hour settings row."""
    op.execute("DELETE FROM settings WHERE name = 'report_auto_hour'")
