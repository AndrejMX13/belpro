"""Add gdpr_additional_clauses to managers.

Revision ID: 011
Revises: 010
Create Date: 2026-05-20
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add gdpr_additional_clauses nullable text column to managers."""
    op.add_column("managers", sa.Column("gdpr_additional_clauses", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove gdpr_additional_clauses column from managers."""
    op.drop_column("managers", "gdpr_additional_clauses")
