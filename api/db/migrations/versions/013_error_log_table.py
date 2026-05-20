"""Add error_log table for structured operational failure records.

Revision ID: 013
Revises: 012
Create Date: 2026-05-20
"""
from __future__ import annotations
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create error_log table."""
    op.create_table(
        "error_log",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("service", sa.Text(), nullable=False),
        sa.Column("operation", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("acknowledged", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("idx_error_log_acknowledged", "error_log", ["acknowledged"])
    op.create_index("idx_error_log_created_at", "error_log", ["created_at"])


def downgrade() -> None:
    """Drop error_log table."""
    op.drop_index("idx_error_log_created_at")
    op.drop_index("idx_error_log_acknowledged")
    op.drop_table("error_log")
