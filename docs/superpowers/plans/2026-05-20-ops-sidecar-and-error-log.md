# Ops Sidecar & Error Logging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a persistent error log (ISS-004), an ops sidecar container for automated backups and photo retention (ISS-014 + ISS-007), a detailed health endpoint (ISS-012 Part A), a health widget on the dashboard (ISS-012 Part B), and an App log page for the manager (ISS-004 Part B).

**Architecture:** A new `error_log` DB table receives structured failures from the API, n8n, and the ops sidecar via a `POST /api/errors` endpoint authenticated with `API_SECRET_KEY`. The ops sidecar is a lightweight Alpine/Python container running internal crond — it handles daily PostgreSQL backups, periodic photo retention cleanup, and writes its own failures to the error log. The enhanced `/api/health/detailed` endpoint queries all services directly on each call and is consumed by a polling dashboard widget. The manager views and dismisses errors via a new App log page in the SPA.

**Tech Stack:** Python 3.11-alpine (ops container), psycopg2-binary, httpx (health checks), FastAPI, SQLAlchemy async, Alembic, vanilla JS

---

## File Structure

**New files:**
- `ops/Dockerfile` — Alpine + Python + postgresql-client ops container
- `ops/entrypoint.sh` — starts crond in foreground, logs to stdout
- `ops/crontab` — cron schedule (backup daily 02:00, cleanup daily 03:00)
- `ops/scripts/backup.sh` — pg_dump + tar photos, prune old backups, report failure
- `ops/scripts/photo_cleanup.py` — delete expired approved-entry photos from disk + DB
- `ops/requirements.txt` — psycopg2-binary, requests
- `api/models/error_log.py` — ErrorLog ORM model
- `api/schemas/error_log.py` — ErrorLogCreate, ErrorLogResponse Pydantic schemas
- `api/routers/errors.py` — POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge
- `api/db/migrations/versions/013_error_log_table.py` — Alembic migration
- `api/tests/test_errors.py` — tests for all three endpoints
- `frontend/js/errors.js` — App log page JS + health widget JS

**Modified files:**
- `docker-compose.yml` — add `ops` service + `backups` volume
- `api/main.py` — register errors router; add `/api/health/detailed` endpoint
- `frontend/index.html` — add App log nav item + page section + health widget panel

---

## Task 1: error_log migration + ORM model

**Files:**
- Create: `api/db/migrations/versions/013_error_log_table.py`
- Create: `api/models/error_log.py`
- Modify: `api/models/__init__.py`

- [ ] **Step 1: Write the migration**

```python
# api/db/migrations/versions/013_error_log_table.py
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
```

- [ ] **Step 2: Write the ORM model**

```python
# api/models/error_log.py
"""ErrorLog ORM model — structured record of operational failures."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ErrorLog(Base):
    """One row per operational failure. Written by API, n8n, and ops sidecar."""

    __tablename__ = "error_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    service: Mapped[str] = mapped_column(Text, nullable=False)
    operation: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
```

- [ ] **Step 3: Register model in `api/models/__init__.py`**

Add `from .error_log import ErrorLog` alongside the other model imports so Alembic autogenerate sees it.

- [ ] **Step 4: Run migration in the test DB**

Run inside the API container:
```bash
docker compose exec api alembic upgrade head
```

Expected: `Running upgrade 012 -> 013, Add error_log table`

- [ ] **Step 5: Commit**

```bash
git add api/db/migrations/versions/013_error_log_table.py api/models/error_log.py api/models/__init__.py
git commit -m "feat(iss-004): add error_log table migration and ORM model"
```

---

## Task 2: Error log API endpoints + schemas + tests

**Files:**
- Create: `api/schemas/error_log.py`
- Create: `api/routers/errors.py`
- Create: `api/tests/test_errors.py`
- Modify: `api/main.py`

The `POST /api/errors` endpoint is called by internal services (n8n, ops sidecar) — it authenticates via `X-Internal-Key: {API_SECRET_KEY}` header, not manager session. `GET /api/errors` and `PATCH /api/errors/{id}/acknowledge` use manager session auth (same `require_manager` dependency used everywhere else).

- [ ] **Step 1: Write the failing tests**

```python
# api/tests/test_errors.py
"""Tests for POST /api/errors, GET /api/errors, PATCH /api/errors/{id}/acknowledge."""
from __future__ import annotations
import pytest
from httpx import AsyncClient
from core.settings import get_settings


def _internal_header() -> dict[str, str]:
    return {"X-Internal-Key": get_settings().api_secret_key}


async def test_post_error_valid_internal_key(client: AsyncClient) -> None:
    """POST with valid internal key creates a record."""
    r = await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={
            "service": "ops",
            "operation": "backup",
            "message": "pg_dump failed",
            "detail": "exit code 1",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["service"] == "ops"
    assert data["acknowledged"] is False


async def test_post_error_missing_key_rejected(client: AsyncClient) -> None:
    """POST without internal key is rejected."""
    r = await client.post(
        "/api/errors",
        json={"service": "ops", "operation": "backup", "message": "fail"},
    )
    assert r.status_code == 401


async def test_post_error_wrong_key_rejected(client: AsyncClient) -> None:
    """POST with wrong internal key is rejected."""
    r = await client.post(
        "/api/errors",
        headers={"X-Internal-Key": "not-the-right-key"},
        json={"service": "ops", "operation": "backup", "message": "fail"},
    )
    assert r.status_code == 401


async def test_get_errors_requires_manager_auth(client: AsyncClient) -> None:
    """GET /api/errors without manager auth is rejected."""
    r = await client.get("/api/errors")
    assert r.status_code == 401


async def test_get_errors_returns_list(client: AsyncClient, auth: dict) -> None:
    """GET returns all error log entries, newest first."""
    # seed two entries
    for i in range(2):
        await client.post(
            "/api/errors",
            headers=_internal_header(),
            json={"service": "api", "operation": "email_delivery", "message": f"err{i}"},
        )
    r = await client.get("/api/errors", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 2
    # newest first
    assert data[0]["created_at"] >= data[1]["created_at"]


async def test_get_errors_filter_unacknowledged(client: AsyncClient, auth: dict) -> None:
    """GET ?unacknowledged=true filters to unacknowledged only."""
    await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "n8n", "operation": "whatsapp_send", "message": "err"},
    )
    r = await client.get("/api/errors?unacknowledged=true", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert all(not e["acknowledged"] for e in data)


async def test_acknowledge_error(client: AsyncClient, auth: dict) -> None:
    """PATCH /{id}/acknowledge sets acknowledged to True."""
    r_post = await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "api", "operation": "report_generation", "message": "fail"},
    )
    error_id = r_post.json()["id"]

    r_ack = await client.patch(f"/api/errors/{error_id}/acknowledge", headers=auth)
    assert r_ack.status_code == 200
    assert r_ack.json()["acknowledged"] is True


async def test_acknowledge_nonexistent_returns_404(client: AsyncClient, auth: dict) -> None:
    """PATCH /{id}/acknowledge on unknown id returns 404."""
    import uuid
    r = await client.patch(f"/api/errors/{uuid.uuid4()}/acknowledge", headers=auth)
    assert r.status_code == 404


async def test_unacknowledged_count(client: AsyncClient, auth: dict) -> None:
    """GET /api/errors/unacknowledged-count returns integer count."""
    await client.post(
        "/api/errors",
        headers=_internal_header(),
        json={"service": "ops", "operation": "photo_cleanup", "message": "err"},
    )
    r = await client.get("/api/errors/unacknowledged-count", headers=auth)
    assert r.status_code == 200
    assert isinstance(r.json()["count"], int)
    assert r.json()["count"] >= 1
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
docker compose exec api pytest tests/test_errors.py -v
```

Expected: collection errors or `404 Not Found` — endpoints don't exist yet.

- [ ] **Step 3: Write schemas**

```python
# api/schemas/error_log.py
"""Pydantic schemas for the error_log endpoint."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class ErrorLogCreate(BaseModel):
    """Payload sent by internal services (API, n8n, ops sidecar)."""
    service: str
    operation: str
    message: str
    detail: str | None = None


class ErrorLogResponse(BaseModel):
    """Single error log row returned to the dashboard."""
    id: uuid.UUID
    service: str
    operation: str
    message: str
    detail: str | None
    acknowledged: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UnacknowledgedCountResponse(BaseModel):
    count: int
```

- [ ] **Step 4: Write the router**

```python
# api/routers/errors.py
"""Error log router — write endpoint for internal services, read endpoints for manager."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.error_log import ErrorLog
from schemas.error_log import ErrorLogCreate, ErrorLogResponse, UnacknowledgedCountResponse

router = APIRouter(prefix="/errors", tags=["errors"])


def _require_internal_key(x_internal_key: Annotated[str | None, Header()] = None) -> None:
    """Validate X-Internal-Key header against API_SECRET_KEY."""
    if x_internal_key != get_settings().api_secret_key:
        raise HTTPException(status_code=401, detail="Invalid internal key.")


@router.post(
    "",
    response_model=ErrorLogResponse,
    status_code=201,
    dependencies=[Depends(_require_internal_key)],
)
async def write_error(
    body: ErrorLogCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ErrorLogResponse:
    """Record an operational failure. Called by API exception handlers, n8n, and the ops sidecar."""
    row = ErrorLog(
        service=body.service,
        operation=body.operation,
        message=body.message,
        detail=body.detail,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return ErrorLogResponse.model_validate(row)


@router.get(
    "/unacknowledged-count",
    response_model=UnacknowledgedCountResponse,
    dependencies=[Depends(require_manager)],
)
async def unacknowledged_count(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UnacknowledgedCountResponse:
    """Return count of unacknowledged errors. Used by nav badge."""
    count = (
        await db.execute(
            select(func.count()).where(ErrorLog.acknowledged.is_(False))
        )
    ).scalar_one()
    return UnacknowledgedCountResponse(count=count)


@router.get(
    "",
    response_model=list[ErrorLogResponse],
    dependencies=[Depends(require_manager)],
)
async def list_errors(
    db: Annotated[AsyncSession, Depends(get_db)],
    unacknowledged: bool = Query(False),
) -> list[ErrorLogResponse]:
    """List error log entries, newest first. Optionally filter to unacknowledged only."""
    q = select(ErrorLog).order_by(ErrorLog.created_at.desc())
    if unacknowledged:
        q = q.where(ErrorLog.acknowledged.is_(False))
    rows = (await db.execute(q)).scalars().all()
    return [ErrorLogResponse.model_validate(r) for r in rows]


@router.patch(
    "/{error_id}/acknowledge",
    response_model=ErrorLogResponse,
    dependencies=[Depends(require_manager)],
)
async def acknowledge_error(
    error_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ErrorLogResponse:
    """Mark an error as acknowledged (read by manager)."""
    row = (
        await db.execute(select(ErrorLog).where(ErrorLog.id == error_id))
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Error record not found.")
    row.acknowledged = True
    await db.commit()
    await db.refresh(row)
    return ErrorLogResponse.model_validate(row)
```

- [ ] **Step 5: Register router in `api/main.py`**

Add to the imports:
```python
from routers.errors import router as errors_router
```

Add below the other `app.include_router` calls:
```python
app.include_router(errors_router, prefix="/api")
```

- [ ] **Step 6: Run tests — verify they pass**

```bash
docker compose exec api pytest tests/test_errors.py -v
```

Expected: all 8 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add api/schemas/error_log.py api/routers/errors.py api/tests/test_errors.py api/main.py
git commit -m "feat(iss-004): add error_log endpoints and tests"
```

---

## Task 3: Ops sidecar container shell

**Files:**
- Create: `ops/Dockerfile`
- Create: `ops/entrypoint.sh`
- Create: `ops/crontab`
- Create: `ops/requirements.txt`
- Modify: `docker-compose.yml`

The ops container runs Alpine Linux with Python 3, postgresql-client (for pg_dump), and crond. It mounts the same photos and pdfs volumes as the API. A new `backups` volume receives backup archives.

- [ ] **Step 1: Write the Dockerfile**

```dockerfile
# ops/Dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash \
    tzdata

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY scripts/ /app/scripts/
COPY entrypoint.sh /app/entrypoint.sh
COPY crontab /etc/crontabs/root

RUN chmod +x /app/entrypoint.sh /app/scripts/*.sh /app/scripts/*.py

WORKDIR /app
CMD ["/app/entrypoint.sh"]
```

- [ ] **Step 2: Write requirements.txt**

```
# ops/requirements.txt
psycopg2-binary==2.9.10
requests==2.32.3
```

- [ ] **Step 3: Write entrypoint.sh**

```bash
#!/bin/bash
# ops/entrypoint.sh
# Forward cron stdout/stderr to container stdout (visible via docker compose logs ops)
exec crond -f -l 2
```

- [ ] **Step 4: Write crontab**

```
# ops/crontab
# m h dom mon dow command
0 2 * * * /app/scripts/backup.sh >> /proc/1/fd/1 2>&1
0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1
```

Note: `>> /proc/1/fd/1 2>&1` forwards cron job output to the container's PID 1 stdout, making it visible in `docker compose logs ops`.

- [ ] **Step 5: Create empty script placeholders (will be filled in Tasks 4 and 5)**

```bash
# ops/scripts/backup.sh — placeholder
#!/bin/bash
echo "[backup] not yet implemented"
```

```python
#!/usr/bin/env python3
# ops/scripts/photo_cleanup.py — placeholder
print("[photo_cleanup] not yet implemented")
```

Make both executable: `chmod +x ops/scripts/backup.sh ops/scripts/photo_cleanup.py`

- [ ] **Step 6: Add the `ops` service to docker-compose.yml**

Add this service block (after the `api` service):

```yaml
  # ─────────────────────────────────────────────────────────────
  # Ops sidecar — automated backups, photo retention cleanup
  # ─────────────────────────────────────────────────────────────
  ops:
    build: ./ops
    restart: unless-stopped
    environment:
      TZ: Europe/Ljubljana
      DATABASE_URL: ${DATABASE_URL}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: postgres
      API_URL: http://api:8000
      API_SECRET_KEY: ${API_SECRET_KEY}
      PHOTO_RETENTION_DAYS: ${PHOTO_RETENTION_DAYS:-730}
      BACKUP_RETENTION_DAYS: ${BACKUP_RETENTION_DAYS:-30}
    volumes:
      - api_photos:/app/photos:ro
      - api_pdfs:/app/pdfs:ro
      - backups:/backups
    depends_on:
      api:
        condition: service_healthy
      postgres:
        condition: service_healthy
```

Add `backups:` to the `volumes:` section at the bottom of docker-compose.yml:

```yaml
volumes:
  postgres_data:
  redis_data:
  n8n_data:
  whisper_models:
  api_photos:
  api_pdfs:
  evolution_instances:
  backups:
```

Also add two new env vars to `.env.example` (no defaults — manager must set if non-default):

```bash
# Ops sidecar
PHOTO_RETENTION_DAYS=730     # days to keep photos for approved entries (2 years default)
BACKUP_RETENTION_DAYS=30     # days to keep local backup archives
```

- [ ] **Step 7: Build the ops container and verify it starts**

```bash
docker compose up -d --build ops
docker compose logs ops
```

Expected: container starts, crond runs. No errors in logs.

- [ ] **Step 8: Commit**

```bash
git add ops/ docker-compose.yml .env.example
git commit -m "feat(iss-014): add ops sidecar container shell"
```

---

## Task 4: Automated backup job

**Files:**
- Modify: `ops/scripts/backup.sh`

The backup script dumps PostgreSQL and archives the photos and pdfs directories. Old archives beyond `BACKUP_RETENTION_DAYS` are pruned. Any failure is reported to the API error log via `curl`.

- [ ] **Step 1: Write backup.sh**

```bash
#!/bin/bash
# ops/scripts/backup.sh
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/${DATE}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"

report_error() {
  local message="$1"
  local detail="$2"
  curl -sf -X POST "${API_URL}/api/errors" \
    -H "Content-Type: application/json" \
    -H "X-Internal-Key: ${API_SECRET_KEY}" \
    -d "{\"service\":\"ops\",\"operation\":\"backup\",\"message\":\"${message}\",\"detail\":\"${detail}\"}" \
    || true   # don't fail if API is also down
}

echo "[backup] Starting backup: ${DATE}"

mkdir -p "${BACKUP_DIR}"

# PostgreSQL dump
echo "[backup] Dumping database..."
if ! PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
    -h "${POSTGRES_HOST}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -f "${BACKUP_DIR}/db.sql"; then
  report_error "pg_dump failed" "exit code $?"
  rm -rf "${BACKUP_DIR}"
  exit 1
fi

# Photos archive
echo "[backup] Archiving photos..."
if ! tar -czf "${BACKUP_DIR}/photos.tar.gz" -C /app photos 2>/dev/null; then
  echo "[backup] Warning: photos archive failed (directory may be empty)"
fi

# PDFs archive
echo "[backup] Archiving PDFs..."
if ! tar -czf "${BACKUP_DIR}/pdfs.tar.gz" -C /app pdfs 2>/dev/null; then
  echo "[backup] Warning: PDFs archive failed (directory may be empty)"
fi

# Compress DB dump
gzip "${BACKUP_DIR}/db.sql"

echo "[backup] Backup complete: ${BACKUP_DIR}"

# Prune old backups
echo "[backup] Pruning backups older than ${RETENTION_DAYS} days..."
find /backups -maxdepth 1 -type d -mtime "+${RETENTION_DAYS}" -exec rm -rf {} + || true

echo "[backup] Done."
```

- [ ] **Step 2: Rebuild ops container**

```bash
docker compose up -d --build ops
```

- [ ] **Step 3: Manually trigger the backup job and verify**

```bash
docker compose exec ops /app/scripts/backup.sh
```

Expected output:
```
[backup] Starting backup: 20260520_020000
[backup] Dumping database...
[backup] Archiving photos...
[backup] Archiving PDFs...
[backup] Backup complete: /backups/20260520_020000
[backup] Pruning backups older than 30 days...
[backup] Done.
```

Verify backup file exists:
```bash
docker compose exec ops ls /backups/
```

Expected: one timestamped directory containing `db.sql.gz`, `photos.tar.gz`, `pdfs.tar.gz`.

- [ ] **Step 4: Test failure reporting — simulate pg_dump failure**

Temporarily break the DB credentials in the exec call:
```bash
docker compose exec -e POSTGRES_PASSWORD=wrong ops /app/scripts/backup.sh || true
```

Then verify an error was written:
```bash
curl -s http://localhost:8100/api/errors \
  -H "Authorization: Basic $(echo -n 'manager:<your_password>' | base64)" | python -m json.tool
```

Expected: JSON array containing a record with `service=ops`, `operation=backup`.

- [ ] **Step 5: Commit**

```bash
git add ops/scripts/backup.sh
git commit -m "feat(iss-014): add automated backup job to ops sidecar"
```

---

## Task 5: Photo retention cleanup job

**Files:**
- Modify: `ops/scripts/photo_cleanup.py`

The cleanup job queries `log_entry_photos` joined with `log_entries` for approved entries older than `PHOTO_RETENTION_DAYS`. For each matching photo, it deletes the file from disk and the DB row in a single transaction.

- [ ] **Step 1: Write photo_cleanup.py**

```python
#!/usr/bin/env python3
# ops/scripts/photo_cleanup.py
"""Delete photos for approved entries older than PHOTO_RETENTION_DAYS."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
import requests


DATABASE_URL = os.environ["DATABASE_URL"]
API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
RETENTION_DAYS = int(os.environ.get("PHOTO_RETENTION_DAYS", "730"))


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={"service": "ops", "operation": "photo_cleanup", "message": message, "detail": detail},
            timeout=10,
        )
    except Exception:
        pass  # can't do much if API is also down


def dsn_from_url(url: str) -> str:
    """Convert asyncpg DATABASE_URL to psycopg2 DSN."""
    return url.replace("postgresql+asyncpg://", "postgresql://")


def main() -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    print(f"[photo_cleanup] Retention cutoff: {cutoff.date()} ({RETENTION_DAYS} days)")

    try:
        conn = psycopg2.connect(dsn_from_url(DATABASE_URL))
    except Exception as e:
        report_error("DB connection failed", str(e))
        sys.exit(1)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id, p.photo_path
                FROM log_entry_photos p
                JOIN log_entries e ON e.id = p.log_entry_id
                WHERE e.status = 'approved'
                  AND e.created_at < %s
                """,
                (cutoff,),
            )
            rows = cur.fetchall()
            print(f"[photo_cleanup] Found {len(rows)} photos to delete.")

            deleted_files = 0
            deleted_rows = 0
            ids_to_delete = []

            for photo_id, photo_path in rows:
                path = Path(photo_path)
                if path.exists():
                    path.unlink()
                    deleted_files += 1
                else:
                    print(f"[photo_cleanup] File not found (skipping): {photo_path}")
                ids_to_delete.append(str(photo_id))

            if ids_to_delete:
                cur.execute(
                    "DELETE FROM log_entry_photos WHERE id = ANY(%s::uuid[])",
                    (ids_to_delete,),
                )
                deleted_rows = cur.rowcount

            conn.commit()
            print(f"[photo_cleanup] Deleted {deleted_files} files, {deleted_rows} DB rows.")

    except Exception as e:
        conn.rollback()
        report_error("Photo cleanup failed", str(e))
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rebuild ops container**

```bash
docker compose up -d --build ops
```

- [ ] **Step 3: Manually trigger cleanup and verify**

```bash
docker compose exec ops /app/scripts/photo_cleanup.py
```

Expected (with no expired photos):
```
[photo_cleanup] Retention cutoff: 2024-05-20 (730 days)
[photo_cleanup] Found 0 photos to delete.
[photo_cleanup] Deleted 0 files, 0 DB rows.
```

- [ ] **Step 4: Verify error reporting by simulating DB failure**

```bash
docker compose exec -e DATABASE_URL=postgresql+asyncpg://bad:bad@postgres:5432/bad ops /app/scripts/photo_cleanup.py || true
```

Check API errors endpoint shows a new record with `operation=photo_cleanup`.

- [ ] **Step 5: Commit**

```bash
git add ops/scripts/photo_cleanup.py
git commit -m "feat(iss-007): add photo retention cleanup job to ops sidecar"
```

---

## Task 6: Enhanced `/api/health/detailed` endpoint

**Files:**
- Modify: `api/main.py`

The new `/api/health/detailed` endpoint queries all services with a short timeout and returns structured status per service. The existing `/api/health` endpoint stays unchanged (used by Docker healthcheck — must stay fast and return `{"status": "ok"}`).

Services checked:
- **postgres** — execute `SELECT 1`, measure response time
- **whisper** — GET `http://whisper:8001/health`
- **n8n** — GET `http://n8n:5678/healthz`
- **evolution** — GET `http://evolution-api:8080/instance/fetchInstances` (with `apikey` header), parse instance connection state
- **disk** — `shutil.disk_usage("/app/photos")`
- **heartbeat** — `MAX(created_at)` from log_entries, `MAX(generated_at)` from monthly_reports

- [ ] **Step 1: Add the detailed health endpoint to `api/main.py`**

Add these imports at the top of `api/main.py`:

```python
import shutil
import time
from datetime import UTC, datetime

import httpx
from sqlalchemy import func, select

from models.log_entry import LogEntry
from models.monthly_report import MonthlyReport
from core.settings import get_settings
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
```

Add the endpoint after the existing `health()` function:

```python
@app.get("/api/health/detailed")
async def health_detailed(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Per-service health status for the manager dashboard widget."""
    result: dict = {}
    settings = get_settings()

    # PostgreSQL
    try:
        t0 = time.monotonic()
        await db.execute(text("SELECT 1"))
        result["postgres"] = {
            "status": "ok",
            "response_ms": round((time.monotonic() - t0) * 1000),
        }
    except Exception as exc:
        result["postgres"] = {"status": "error", "detail": str(exc)}

    # Whisper
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("http://whisper:8001/health")
        result["whisper"] = {"status": "ok" if r.status_code == 200 else "error"}
    except Exception as exc:
        result["whisper"] = {"status": "error", "detail": str(exc)}

    # n8n
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("http://n8n:5678/healthz")
        result["n8n"] = {"status": "ok" if r.status_code == 200 else "error"}
    except Exception as exc:
        result["n8n"] = {"status": "error", "detail": str(exc)}

    # Evolution API — fetch instance connection state
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(
                f"http://evolution-api:8080/instance/fetchInstances",
                headers={"apikey": settings.authentication_api_key},
            )
        if r.status_code == 200:
            instances = r.json()
            instance = next(
                (i for i in instances if i.get("name") == settings.evolution_instance_name),
                None,
            )
            state = instance.get("connectionStatus", "unknown") if instance else "not_found"
            result["evolution"] = {
                "status": "ok" if state == "open" else "warning",
                "connection_state": state,
            }
        else:
            result["evolution"] = {"status": "error", "detail": f"HTTP {r.status_code}"}
    except Exception as exc:
        result["evolution"] = {"status": "error", "detail": str(exc)}

    # Disk
    try:
        usage = shutil.disk_usage("/app/photos")
        free_pct = usage.free / usage.total * 100
        result["disk"] = {
            "status": "ok" if free_pct > 15 else ("warning" if free_pct > 5 else "error"),
            "free_gb": round(usage.free / 1_000_000_000, 1),
            "free_pct": round(free_pct, 1),
        }
    except Exception as exc:
        result["disk"] = {"status": "error", "detail": str(exc)}

    # Heartbeat
    try:
        last_entry = (
            await db.execute(select(func.max(LogEntry.created_at)))
        ).scalar()
        last_report = (
            await db.execute(select(func.max(MonthlyReport.generated_at)))
        ).scalar()
        result["heartbeat"] = {
            "last_entry": last_entry.isoformat() if last_entry else None,
            "last_report": last_report.isoformat() if last_report else None,
        }
    except Exception as exc:
        result["heartbeat"] = {"status": "error", "detail": str(exc)}

    return result
```

`MonthlyReport` needs to be imported — check `api/models/monthly_report.py` for the actual class name and `generated_at` field name; adjust the field name in the query if it differs.

- [ ] **Step 2: Add `httpx` to api requirements if not already present**

Check `api/requirements.txt`. If `httpx` is not listed, add it:
```
httpx==0.27.2
```

Then rebuild:
```bash
docker compose up -d --build api
```

- [ ] **Step 3: Smoke-test the endpoint**

```bash
curl -s http://localhost:8100/api/health/detailed | python -m json.tool
```

Expected: JSON with keys `postgres`, `whisper`, `n8n`, `evolution`, `disk`, `heartbeat`. Each has a `status` field (`ok`/`warning`/`error`).

- [ ] **Step 4: Commit**

```bash
git add api/main.py api/requirements.txt
git commit -m "feat(iss-012): add /api/health/detailed endpoint with per-service status"
```

---

## Task 7: Health widget on the dashboard

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/js/errors.js` (create this file — it handles both health widget and App log page)

The health widget is a compact panel shown at the top of the main dashboard view, polling `/api/health/detailed` every 30 seconds. Each service row shows a coloured dot (green/amber/red) and the key detail field inline.

- [ ] **Step 1: Add the health widget HTML to `frontend/index.html`**

Find the section where page content is rendered (look for `id="page-volunteers"` or similar). Add a health widget panel inside the volunteers page section (the default landing page) before the existing volunteer content:

```html
<!-- Health widget — shown on main landing page -->
<div id="health-widget" class="health-widget card" style="margin-bottom:1.5rem">
  <div class="card-header" style="display:flex;align-items:center;gap:0.5rem">
    <span style="font-weight:600">Stanje sistema</span>
    <span id="health-last-updated" style="font-size:0.78rem;color:#888;margin-left:auto"></span>
  </div>
  <div id="health-rows" class="health-rows">
    <span style="color:#888;font-size:0.9rem">Nalaganje...</span>
  </div>
</div>
```

- [ ] **Step 2: Add the App log nav item to the sidebar in `frontend/index.html`**

After the last existing nav item (documents/gdpr), add:

```html
      <a href="#applog" class="nav-item" data-page="applog">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        Dnevnik napak
        <span id="nav-error-badge" class="nav-badge" hidden></span>
      </a>
```

- [ ] **Step 3: Add the App log page section to `frontend/index.html`**

Add a new page section (alongside the other `id="page-*"` sections):

```html
<!-- App log page -->
<section id="page-applog" hidden>
  <div class="page-header">
    <h2>Dnevnik napak</h2>
    <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.9rem">
      <input type="checkbox" id="applog-filter-unacked"> Samo nepotrjene
    </label>
  </div>
  <div id="applog-list"></div>
</section>
```

- [ ] **Step 4: Add CSS for health widget and error badge**

In `frontend/css/main.css`, add at the end:

```css
/* Health widget */
.health-widget { padding: 1rem; }
.health-rows { display: flex; flex-direction: column; gap: 0.4rem; margin-top: 0.75rem; }
.health-row { display: flex; align-items: center; gap: 0.6rem; font-size: 0.9rem; }
.health-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.health-dot-ok { background: #22c55e; }
.health-dot-warning { background: #f59e0b; }
.health-dot-error { background: #ef4444; }
.health-label { min-width: 90px; font-weight: 500; }
.health-detail { color: #666; font-size: 0.82rem; }

/* Nav error badge */
.nav-badge {
  margin-left: auto;
  background: #ef4444;
  color: #fff;
  border-radius: 999px;
  font-size: 0.7rem;
  padding: 1px 6px;
  font-weight: 700;
}

/* App log */
.error-row { border: 1px solid #e5e7eb; border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; }
.error-row.acknowledged { opacity: 0.5; }
.error-meta { font-size: 0.78rem; color: #888; margin-bottom: 0.25rem; }
.error-message { font-weight: 500; margin-bottom: 0.25rem; }
.error-detail { font-size: 0.82rem; color: #555; white-space: pre-wrap; }
```

- [ ] **Step 5: Create `frontend/js/errors.js`**

```javascript
// frontend/js/errors.js
// Health widget (shown on volunteers/main page) + App log page

const SERVICE_LABELS = {
  postgres: 'PostgreSQL',
  whisper: 'Whisper',
  n8n: 'n8n',
  evolution: 'WhatsApp',
  disk: 'Disk',
  heartbeat: 'Heartbeat',
};

// ── Health widget ─────────────────────────────────────────────────────────────

let _healthInterval = null;

function renderHealthWidget(data) {
  const rows = document.getElementById('health-rows');
  if (!rows) return;
  rows.innerHTML = '';

  for (const [key, val] of Object.entries(data)) {
    const label = SERVICE_LABELS[key] || key;
    const status = val.status || 'ok';
    const dotClass = status === 'ok' ? 'health-dot-ok'
                   : status === 'warning' ? 'health-dot-warning'
                   : 'health-dot-error';

    let detail = '';
    if (key === 'postgres' && val.response_ms != null) detail = `${val.response_ms} ms`;
    else if (key === 'evolution' && val.connection_state) detail = val.connection_state;
    else if (key === 'disk' && val.free_gb != null) detail = `${val.free_gb} GB free (${val.free_pct}%)`;
    else if (key === 'heartbeat') {
      const lastEntry = val.last_entry ? new Date(val.last_entry).toLocaleString('sl-SI') : '—';
      detail = `zadnji vnos: ${lastEntry}`;
    } else if (val.detail) detail = val.detail;

    rows.insertAdjacentHTML('beforeend', `
      <div class="health-row">
        <span class="health-dot ${dotClass}"></span>
        <span class="health-label">${label}</span>
        <span class="health-detail">${detail}</span>
      </div>
    `);
  }

  const updated = document.getElementById('health-last-updated');
  if (updated) updated.textContent = `Posodobljeno: ${new Date().toLocaleTimeString('sl-SI')}`;
}

async function loadHealthWidget() {
  try {
    const data = await apiFetch('/api/health/detailed');
    renderHealthWidget(data);
  } catch (e) {
    const rows = document.getElementById('health-rows');
    if (rows) rows.innerHTML = '<span style="color:#ef4444">Napaka pri nalaganju stanja.</span>';
  }
}

export function startHealthWidget() {
  loadHealthWidget();
  _healthInterval = setInterval(loadHealthWidget, 30_000);
}

export function stopHealthWidget() {
  if (_healthInterval) clearInterval(_healthInterval);
}

// ── Nav badge (unacknowledged error count) ────────────────────────────────────

export async function refreshErrorBadge() {
  try {
    const data = await apiFetch('/api/errors/unacknowledged-count');
    const badge = document.getElementById('nav-error-badge');
    if (!badge) return;
    if (data.count > 0) {
      badge.textContent = data.count;
      badge.hidden = false;
    } else {
      badge.hidden = true;
    }
  } catch (_) { /* ignore */ }
}

// ── App log page ──────────────────────────────────────────────────────────────

let _applogUnackedOnly = false;

async function loadAppLog() {
  const list = document.getElementById('applog-list');
  if (!list) return;
  list.innerHTML = '<p style="color:#888">Nalaganje...</p>';

  const url = _applogUnackedOnly ? '/api/errors?unacknowledged=true' : '/api/errors';
  try {
    const errors = await apiFetch(url);
    if (errors.length === 0) {
      list.innerHTML = '<p style="color:#888">Ni vnosov.</p>';
      return;
    }
    list.innerHTML = errors.map(e => `
      <div class="error-row ${e.acknowledged ? 'acknowledged' : ''}" data-id="${e.id}">
        <div class="error-meta">
          ${e.service} · ${e.operation} · ${new Date(e.created_at).toLocaleString('sl-SI')}
          ${e.acknowledged ? '' : `<button class="btn btn-sm" onclick="acknowledgeError('${e.id}')" style="margin-left:0.5rem">Potrdi</button>`}
        </div>
        <div class="error-message">${e.message}</div>
        ${e.detail ? `<div class="error-detail">${e.detail}</div>` : ''}
      </div>
    `).join('');
  } catch (err) {
    list.innerHTML = '<p style="color:#ef4444">Napaka pri nalaganju.</p>';
  }
}

window.acknowledgeError = async function(id) {
  try {
    await apiFetch(`/api/errors/${id}/acknowledge`, { method: 'PATCH' });
    await loadAppLog();
    await refreshErrorBadge();
  } catch (e) {
    alert('Napaka pri potrditvi.');
  }
};

export function initAppLogPage() {
  const filter = document.getElementById('applog-filter-unacked');
  if (filter) {
    filter.addEventListener('change', () => {
      _applogUnackedOnly = filter.checked;
      loadAppLog();
    });
  }
  loadAppLog();
}
```

Note: `apiFetch` is assumed to be a global helper already in the project (check `frontend/js/api.js`). If it doesn't exist by that name, use the pattern already in use in other JS files for authenticated API calls.

- [ ] **Step 6: Wire `errors.js` into `index.html` and the page router**

Add the script tag in `index.html` alongside other JS imports:
```html
<script type="module" src="/js/errors.js"></script>
```

Find where the page router dispatches to page-specific init functions (look for the `hashchange` handler or similar routing logic in existing JS files). Add:
- Call `startHealthWidget()` after login succeeds (so health shows immediately)
- Call `refreshErrorBadge()` after login and periodically (every 60 seconds)
- Call `initAppLogPage()` when navigating to `#applog`

The exact wiring depends on how the existing router is structured — follow its pattern exactly.

- [ ] **Step 7: Verify in browser**

Open `http://localhost:80`, log in. Verify:
- Health widget appears on the volunteers page showing coloured dots for each service
- Widget refreshes every 30 seconds (check Network tab)
- Nav shows "Dnevnik napak" link; badge appears if there are unacknowledged errors

- [ ] **Step 8: Commit**

```bash
git add frontend/index.html frontend/js/errors.js frontend/css/main.css
git commit -m "feat(iss-012, iss-004): add health widget and App log nav item to dashboard"
```

---

## Task 8: App log page

The App log page HTML section and nav item were added in Task 7. This task completes the wiring — verifying the page works end-to-end.

**Files:**
- Modify: `frontend/index.html` (page router wiring, if not done in Task 7)

- [ ] **Step 1: Navigate to App log page and verify**

In the dashboard, click "Dnevnik napak" in the nav. Verify:
- The page shows all error_log entries (or "Ni vnosov" if empty)
- The "Samo nepotrjene" checkbox filters correctly
- The "Potrdi" button acknowledges an error and the row dims
- The nav badge count decreases on acknowledge

To generate test errors for verification:
```bash
curl -s -X POST http://localhost:8100/api/errors \
  -H "X-Internal-Key: $(grep API_SECRET_KEY .env | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"service":"ops","operation":"backup","message":"Test napaka za preverjanje"}'
```

- [ ] **Step 2: Run the full test suite**

```bash
docker compose exec api pytest tests/ -v
```

Expected: all existing tests pass + all new tests in `test_errors.py` pass.

- [ ] **Step 3: Final commit**

```bash
git add frontend/index.html
git commit -m "feat(iss-004): complete App log page wiring and end-to-end verification"
```

---

## Self-Review

**Spec coverage:**
- ISS-004 Part A (error_log table + endpoints): Tasks 1–2 ✓
- ISS-004 Part B (manager App log page + badge): Tasks 7–8 ✓
- ISS-014 (ops sidecar container + backups): Tasks 3–4 ✓
- ISS-007 (photo retention cleanup): Task 5 ✓
- ISS-012 Part A (detailed health endpoint): Task 6 ✓
- ISS-012 Part B (dashboard health widget): Task 7 ✓

**Known implementation detail to resolve at coding time:**
- Task 6: check `api/models/monthly_report.py` for the exact field name used for the report generation timestamp — use that name in the `func.max()` query.
- Task 7: check `frontend/js/api.js` for the exact name of the authenticated fetch helper and follow its pattern in `errors.js`.
- Task 7: find the existing page router (likely a `hashchange` listener in a main JS file) and wire `startHealthWidget`, `refreshErrorBadge`, and `initAppLogPage` into it following the existing pattern.
