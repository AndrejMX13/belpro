"""Seed evolution_instance_name setting row.

Revision ID: 015
Revises: 014
Create Date: 2026-05-25
"""
from __future__ import annotations
from typing import Sequence, Union
from alembic import op

revision: str = "015"
down_revision: Union[str, None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the evolution_instance_name settings row with default value belpro."""
    op.execute(
        "INSERT INTO settings (name, type, value) "
        "VALUES ('evolution_instance_name', 'str', 'belpro') "
        "ON CONFLICT (name) DO NOTHING"
    )


def downgrade() -> None:
    """Remove the evolution_instance_name settings row."""
    op.execute("DELETE FROM settings WHERE name = 'evolution_instance_name'")
