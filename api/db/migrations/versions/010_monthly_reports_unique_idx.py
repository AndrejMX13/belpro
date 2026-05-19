"""Add unique partial indexes to monthly_reports.

One row per volunteer per month; one consolidated row per month.
Uses partial indexes to handle nullable volunteer_id correctly.

Revision ID: 010
Revises: 009
Create Date: 2026-05-19
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create unique partial indexes on monthly_reports."""
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reports_unique_vol'
            ) THEN
                CREATE UNIQUE INDEX idx_reports_unique_vol
                ON monthly_reports (volunteer_id, period_year, period_month)
                WHERE volunteer_id IS NOT NULL;
            END IF;
        END$$
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reports_unique_consolidated'
            ) THEN
                CREATE UNIQUE INDEX idx_reports_unique_consolidated
                ON monthly_reports (period_year, period_month)
                WHERE volunteer_id IS NULL;
            END IF;
        END$$
    """)


def downgrade() -> None:
    """Drop unique partial indexes from monthly_reports."""
    op.execute("DROP INDEX IF EXISTS idx_reports_unique_vol")
    op.execute("DROP INDEX IF EXISTS idx_reports_unique_consolidated")
