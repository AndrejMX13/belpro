"""Add WhatsApp bot number and SMTP config columns to managers.

Revision ID: 006
Revises: 005
Create Date: 2026-05-04

Adds six nullable columns to managers:
  ngo_whatsapp_phone      — dedicated bot phone number linked to Evolution API
  smtp_host               — SMTP server hostname (e.g. smtp.gmail.com)
  smtp_port               — SMTP port (default 587)
  smtp_user               — SMTP login / from-address
  smtp_from_name          — display name for outgoing emails
  evolution_api_admin_url — URL of Evolution API admin UI (for settings link)

All nullable; existing rows get NULL.  Non-sensitive — smtp_password stays in .env.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add WhatsApp bot number and SMTP config columns to managers."""
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS ngo_whatsapp_phone VARCHAR(30)")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS smtp_host VARCHAR(255)")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS smtp_port INTEGER DEFAULT 587")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS smtp_user VARCHAR(255)")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS smtp_from_name VARCHAR(100)")
    op.execute("ALTER TABLE managers ADD COLUMN IF NOT EXISTS evolution_api_admin_url VARCHAR(255)")


def downgrade() -> None:
    """Drop WhatsApp bot number and SMTP config columns from managers."""
    op.drop_column("managers", "evolution_api_admin_url")
    op.drop_column("managers", "smtp_from_name")
    op.drop_column("managers", "smtp_user")
    op.drop_column("managers", "smtp_port")
    op.drop_column("managers", "smtp_host")
    op.drop_column("managers", "ngo_whatsapp_phone")
