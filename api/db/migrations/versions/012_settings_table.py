"""Add settings table for runtime-tunable configuration.

Revision ID: 012
Revises: 011
Create Date: 2026-05-20
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create settings table and seed default values."""
    op.create_table(
        "settings",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.UniqueConstraint("name", name="uq_settings_name"),
    )
    op.execute(
        """
        INSERT INTO settings (name, type, value) VALUES
            ('max_photos_per_entry',  'int', '5'),
            ('photo_retention_days',  'int', '730'),
            ('session_duration_hours','int', '24')
        ON CONFLICT (name) DO NOTHING
        """
    )


def downgrade() -> None:
    """Drop settings table."""
    op.drop_table("settings")
