"""Add emso_hash column for EMŠO uniqueness enforcement.

Revision ID: 002
Revises: 001
Create Date: 2026-05-02

Adds a nullable HMAC-SHA256 column alongside the encrypted emso field.
Nullable so existing rows are unaffected; all new rows will have it set.
NULLs don't violate the unique constraint in PostgreSQL.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE volunteers ADD COLUMN IF NOT EXISTS emso_hash VARCHAR(64)")
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'uq_volunteers_emso_hash'
            ) THEN
                ALTER TABLE volunteers ADD CONSTRAINT uq_volunteers_emso_hash UNIQUE (emso_hash);
            END IF;
        END$$
    """)


def downgrade() -> None:
    op.drop_constraint("uq_volunteers_emso_hash", "volunteers", type_="unique")
    op.drop_column("volunteers", "emso_hash")
