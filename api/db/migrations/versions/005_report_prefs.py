"""Add report channel preferences to managers and volunteers.

Revision ID: 005
Revises: 004
Create Date: 2026-05-04

Adds six boolean columns:
  managers.report_whatsapp         — manager receives consolidated report via WhatsApp
  managers.report_email            — manager receives consolidated report via email
  managers.default_report_whatsapp — default for newly registered volunteers
  managers.default_report_email    — default for newly registered volunteers
  volunteers.report_whatsapp       — this volunteer receives report via WhatsApp
  volunteers.report_email          — this volunteer receives report via email

Defaults: email=TRUE, whatsapp=FALSE (safe for existing rows).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add report preference columns to managers and volunteers."""
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS report_whatsapp BOOLEAN NOT NULL DEFAULT FALSE")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS report_email BOOLEAN NOT NULL DEFAULT TRUE")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS default_report_whatsapp BOOLEAN NOT NULL DEFAULT FALSE")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS default_report_email BOOLEAN NOT NULL DEFAULT TRUE")
    op.execute("ALTER TABLE volunteers ADD COLUMN IF NOT EXISTS report_whatsapp BOOLEAN NOT NULL DEFAULT FALSE")
    op.execute("ALTER TABLE volunteers ADD COLUMN IF NOT EXISTS report_email BOOLEAN NOT NULL DEFAULT TRUE")


def downgrade() -> None:
    """Drop report preference columns from managers and volunteers."""
    op.drop_column("volunteers", "report_email")
    op.drop_column("volunteers", "report_whatsapp")
    op.drop_column("managers", "default_report_email")
    op.drop_column("managers", "default_report_whatsapp")
    op.drop_column("managers", "report_email")
    op.drop_column("managers", "report_whatsapp")
