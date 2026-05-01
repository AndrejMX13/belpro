"""Initial schema — baseline migration reflecting db/init.sql.

Revision ID: 001
Revises:
Create Date: 2025-05-01

IMPORTANT — do NOT run this migration on a fresh deployment.
init.sql already creates the full schema when the postgres container first
starts.  After docker compose up, stamp the DB as migrated:

    docker compose exec api alembic stamp head

All future schema changes go through new Alembic migrations only.
This file exists so that the schema history is self-contained and
autogenerate can diff against it correctly.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the full Belpro schema from scratch."""
    # ── entry_status enum ────────────────────────────────────────────────────
    op.execute("""
        CREATE TYPE entry_status AS ENUM (
            'pending_volunteer',
            'pending_manager',
            'approved',
            'rejected'
        )
    """)

    # ── managers ─────────────────────────────────────────────────────────────
    op.create_table(
        "managers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(30), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("ngo_name", sa.String(255), nullable=False),
        sa.Column("ngo_street", sa.String(255), nullable=False),
        sa.Column("ngo_postal_code", sa.String(4), nullable=False),
        sa.Column("ngo_city", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
    )

    # ── volunteers ───────────────────────────────────────────────────────────
    op.create_table(
        "volunteers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("street", sa.String(255), nullable=False),
        sa.Column("postal_code", sa.String(4), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("emso", sa.Text(), nullable=False),
        sa.Column("phone", sa.String(30), nullable=False, unique=True),
        sa.Column("email", sa.String(255)),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("manager_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("managers.id", ondelete="RESTRICT"), nullable=False),
    )
    op.create_index("idx_volunteers_manager", "volunteers", ["manager_id"])
    op.create_index("idx_volunteers_active", "volunteers", ["active"])
    op.create_index("idx_volunteers_phone", "volunteers", ["phone"])

    # ── log_entries ──────────────────────────────────────────────────────────
    op.create_table(
        "log_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("volunteer_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("volunteers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("activity_description", sa.Text(), nullable=False),
        sa.Column("raw_transcript", sa.Text()),
        sa.Column("hours", sa.Numeric(4, 1), nullable=False),
        sa.Column("location", sa.String(255)),
        sa.Column("status",
                  sa.Enum("pending_volunteer", "pending_manager", "approved", "rejected",
                          name="entry_status", create_type=False),
                  nullable=False, server_default="pending_volunteer"),
        sa.Column("photo_path", sa.String(500)),
        sa.Column("photo_exif_timestamp", sa.DateTime(timezone=True)),
        sa.Column("photo_exif_lat", sa.Numeric(10, 7)),
        sa.Column("photo_exif_lon", sa.Numeric(10, 7)),
        sa.Column("volunteer_confirmed_at", sa.DateTime(timezone=True)),
        sa.Column("manager_approved_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
    )
    op.create_index("idx_entries_volunteer", "log_entries", ["volunteer_id"])
    op.create_index("idx_entries_status", "log_entries", ["status"])
    op.create_index("idx_entries_date", "log_entries", ["entry_date"])
    op.create_index("idx_entries_location", "log_entries", ["location"])
    op.create_index("idx_entries_created", "log_entries", ["created_at"])
    op.create_index("idx_entries_vol_date", "log_entries", ["volunteer_id", "entry_date"])

    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)
    op.execute("""
        CREATE TRIGGER trg_entries_updated_at
            BEFORE UPDATE ON log_entries
            FOR EACH ROW EXECUTE FUNCTION set_updated_at()
    """)

    # ── monthly_reports ──────────────────────────────────────────────────────
    op.create_table(
        "monthly_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("volunteer_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("volunteers.id", ondelete="RESTRICT")),
        sa.Column("period_year", sa.SmallInteger(), nullable=False),
        sa.Column("period_month", sa.SmallInteger(), nullable=False),
        sa.Column("pdf_path", sa.String(500), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("period_month BETWEEN 1 AND 12", name="ck_reports_month"),
    )
    op.create_index("idx_reports_volunteer", "monthly_reports", ["volunteer_id"])
    op.create_index("idx_reports_period", "monthly_reports", ["period_year", "period_month"])
    op.execute("""
        CREATE UNIQUE INDEX idx_reports_unique_vol_period
            ON monthly_reports(volunteer_id, period_year, period_month)
            WHERE volunteer_id IS NOT NULL
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_reports_unique_consolidated_period
            ON monthly_reports(period_year, period_month)
            WHERE volunteer_id IS NULL
    """)


def downgrade() -> None:
    """Drop all Belpro tables and the entry_status enum."""
    op.drop_table("monthly_reports")
    op.execute("DROP TRIGGER IF EXISTS trg_entries_updated_at ON log_entries")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at")
    op.drop_table("log_entries")
    op.drop_table("volunteers")
    op.drop_table("managers")
    op.execute("DROP TYPE IF EXISTS entry_status")
