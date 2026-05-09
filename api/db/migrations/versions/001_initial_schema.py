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
    """Create the full Belpro schema from scratch (idempotent — safe to re-run)."""
    # ── entry_status enum ────────────────────────────────────────────────────
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'entry_status') THEN
                CREATE TYPE entry_status AS ENUM (
                    'pending_volunteer',
                    'pending_manager',
                    'approved',
                    'rejected'
                );
            END IF;
        END$$
    """)

    # ── managers ─────────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE IF NOT EXISTS managers (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            ngo_name VARCHAR(255) NOT NULL,
            ngo_street VARCHAR(255) NOT NULL,
            ngo_postal_code VARCHAR(4) NOT NULL,
            ngo_city VARCHAR(100) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

    # ── volunteers ───────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            street VARCHAR(255) NOT NULL,
            postal_code VARCHAR(4) NOT NULL,
            city VARCHAR(100) NOT NULL,
            emso TEXT NOT NULL,
            phone VARCHAR(30) NOT NULL UNIQUE,
            email VARCHAR(255),
            active BOOLEAN NOT NULL DEFAULT TRUE,
            registered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            manager_id UUID NOT NULL REFERENCES managers(id) ON DELETE RESTRICT
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_volunteers_manager ON volunteers (manager_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_volunteers_active ON volunteers (active)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_volunteers_phone ON volunteers (phone)")

    # ── log_entries ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE IF NOT EXISTS log_entries (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            volunteer_id UUID NOT NULL REFERENCES volunteers(id) ON DELETE RESTRICT,
            entry_date DATE NOT NULL,
            activity_description TEXT NOT NULL,
            raw_transcript TEXT,
            hours NUMERIC(4, 1) NOT NULL,
            location VARCHAR(255),
            status entry_status NOT NULL DEFAULT 'pending_volunteer',
            photo_path VARCHAR(500),
            photo_exif_timestamp TIMESTAMPTZ,
            photo_exif_lat NUMERIC(10, 7),
            photo_exif_lon NUMERIC(10, 7),
            volunteer_confirmed_at TIMESTAMPTZ,
            manager_approved_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_entries_volunteer ON log_entries (volunteer_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_entries_status ON log_entries (status)")
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'log_entries' AND column_name = 'entry_date'
            ) THEN
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_date') THEN
                    CREATE INDEX idx_entries_date ON log_entries (entry_date);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_vol_date') THEN
                    CREATE INDEX idx_entries_vol_date ON log_entries (volunteer_id, entry_date);
                END IF;
            END IF;
        END$$
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_entries_location ON log_entries (location)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_entries_created ON log_entries (created_at)")

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
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger WHERE tgname = 'trg_entries_updated_at'
            ) THEN
                CREATE TRIGGER trg_entries_updated_at
                    BEFORE UPDATE ON log_entries
                    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
            END IF;
        END$$
    """)

    # ── monthly_reports ──────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE IF NOT EXISTS monthly_reports (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            volunteer_id UUID REFERENCES volunteers(id) ON DELETE RESTRICT,
            period_year SMALLINT NOT NULL,
            period_month SMALLINT NOT NULL,
            pdf_path VARCHAR(500) NOT NULL,
            generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            sent_at TIMESTAMPTZ,
            CONSTRAINT ck_reports_month CHECK (period_month BETWEEN 1 AND 12)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_reports_volunteer ON monthly_reports (volunteer_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_reports_period ON monthly_reports (period_year, period_month)")
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_reports_unique_vol_period
            ON monthly_reports(volunteer_id, period_year, period_month)
            WHERE volunteer_id IS NOT NULL
    """)
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_reports_unique_consolidated_period
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
