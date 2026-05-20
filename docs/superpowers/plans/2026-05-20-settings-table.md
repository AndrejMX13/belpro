# ISS-026: Settings Table Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce a `settings` DB table and `AppSettings` central authority so all configuration — env-based and DB-tunable — comes from one `Depends(get_app_settings)` dependency, and add a new Administracija frontend page where the manager can edit the three runtime-tunable values.

**Architecture:** `AppSettings` wraps the existing env-only `Settings` class, resolves `max_photos_per_entry`, `photo_retention_days`, and `session_duration_hours` from the DB with env fallback, and delegates all other attribute access to the env layer via `__getattr__`. All routes currently calling `get_settings()` switch to `get_app_settings`. A new `GET/PATCH /api/admin/settings` endpoint and Administracija frontend page complete the loop.

**Tech Stack:** Python 3.11 / FastAPI / SQLAlchemy 2.x async / Alembic / Pydantic v2 / Vanilla JS

---

## File Map

**Create:**
- `api/models/app_setting.py` — AppSetting ORM model
- `api/db/migrations/versions/012_settings_table.py` — creates table, seeds 3 rows
- `api/services/app_settings.py` — AppSettings class + get_app_settings dependency
- `api/schemas/admin.py` — AdminSettingsResponse + AdminSettingsUpdate Pydantic models
- `api/routers/admin.py` — GET /api/admin/settings + PATCH /api/admin/settings
- `api/tests/test_app_settings.py` — unit tests for AppSettings + integration tests for admin router
- `frontend/js/admin.js` — Administracija page (load, edit, explicit save)

**Modify:**
- `api/models/__init__.py` — add AppSetting to imports and `__all__`
- `api/main.py` — import and register admin router
- `api/routers/log_entries.py` — replace 4 direct `get_settings()` calls with `get_app_settings` dependency
- `api/routers/auth.py` — switch login and logout to `get_app_settings`
- `api/routers/documents.py` — switch consent PDF handler to `get_app_settings`
- `frontend/js/api.js` — add `admin` namespace after `documents`
- `frontend/index.html` — add Administracija nav item + `admin.js` script tag
- `frontend/js/volunteers.js` — add `#admin` hash routing after `#documents` branch (line 218)

---

## Task 1: AppSetting ORM model + Alembic migration

**Files:**
- Create: `api/models/app_setting.py`
- Create: `api/db/migrations/versions/012_settings_table.py`
- Modify: `api/models/__init__.py`
- Test: `api/tests/test_app_settings.py`

- [ ] **Step 1: Write the failing test**

Create `api/tests/test_app_settings.py` with a migration smoke test:

```python
"""Tests for AppSettings service and admin settings router."""
from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ── Migration smoke test ──────────────────────────────────────────────────────

async def test_settings_table_seeded(db_session: AsyncSession) -> None:
    """Migration seeds the three default settings rows."""
    from models.app_setting import AppSetting

    rows = (await db_session.execute(select(AppSetting))).scalars().all()
    names = {r.name for r in rows}
    assert {"max_photos_per_entry", "photo_retention_days", "session_duration_hours"}.issubset(names)

    by_name = {r.name: r for r in rows}
    assert by_name["max_photos_per_entry"].type == "int"
    assert by_name["max_photos_per_entry"].value == "5"
    assert by_name["photo_retention_days"].value == "730"
    assert by_name["session_duration_hours"].value == "24"
```

- [ ] **Step 2: Run test to verify it fails**

```
docker compose exec api pytest tests/test_app_settings.py::test_settings_table_seeded -v
```

Expected: FAIL — `ImportError: cannot import name 'AppSetting'`

- [ ] **Step 3: Create the ORM model**

Create `api/models/app_setting.py`:

```python
"""AppSetting ORM model — runtime-tunable key-value configuration."""
from __future__ import annotations

import uuid

from sqlalchemy import Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AppSetting(Base):
    """One row per named setting. All values stored as TEXT."""

    __tablename__ = "settings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
```

- [ ] **Step 4: Register the model in `api/models/__init__.py`**

Replace the entire file:

```python
"""SQLAlchemy ORM models — import all to ensure they register with Base.metadata."""
from .base import Base
from .app_setting import AppSetting
from .log_entry import EntryStatus, LogEntry
from .log_entry_photo import LogEntryPhoto
from .manager import Manager
from .monthly_report import MonthlyReport
from .volunteer import Volunteer

__all__ = [
    "AppSetting",
    "Base",
    "EntryStatus",
    "LogEntry",
    "LogEntryPhoto",
    "Manager",
    "MonthlyReport",
    "Volunteer",
]
```

- [ ] **Step 5: Create the Alembic migration**

Create `api/db/migrations/versions/012_settings_table.py`:

```python
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
```

- [ ] **Step 6: Run the migration**

```
docker compose exec api alembic upgrade head
```

Expected: `Running upgrade 011 -> 012, Add settings table for runtime-tunable configuration`

- [ ] **Step 7: Run the test to verify it passes**

```
docker compose exec api pytest tests/test_app_settings.py::test_settings_table_seeded -v
```

Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add api/models/app_setting.py api/models/__init__.py api/db/migrations/versions/012_settings_table.py api/tests/test_app_settings.py
git commit -m "feat(iss-026): add AppSetting ORM model and settings table migration"
```

---

## Task 2: AppSettings central authority + unit tests

**Files:**
- Create: `api/services/app_settings.py`
- Modify: `api/tests/test_app_settings.py` (add unit tests)

- [ ] **Step 1: Add failing unit tests to `api/tests/test_app_settings.py`**

Append after the migration smoke test:

```python
# ── Unit tests for AppSettings ────────────────────────────────────────────────

def test_appsettings_uses_db_int_value() -> None:
    """DB value overrides env default for integer settings."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {"max_photos_per_entry": "10"})
    assert settings.max_photos_per_entry == 10


def test_appsettings_falls_back_to_env_when_row_missing() -> None:
    """Env default is used when the DB row is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {})
    assert settings.max_photos_per_entry == env.max_photos_per_entry
    assert settings.photo_retention_days == env.photo_retention_days
    assert settings.session_duration_hours == env.session_duration_hours


def test_appsettings_passthrough_to_env() -> None:
    """Non-tunable attributes delegate to the underlying env Settings."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    settings = AppSettings(env, {})
    assert settings.emso_encryption_key == env.emso_encryption_key
    assert settings.api_secret_key == env.api_secret_key


def test_appsettings_bool_helper_parses_truthy_strings() -> None:
    """_bool() accepts 'true', '1', 'yes' as True."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    for truthy in ("true", "True", "TRUE", "1", "yes"):
        s = AppSettings(env, {"flag": truthy})
        assert s._bool("flag", False) is True, f"Expected True for {truthy!r}"


def test_appsettings_bool_helper_parses_falsy_strings() -> None:
    """_bool() returns False for any non-truthy string."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    for falsy in ("false", "False", "0", "no"):
        s = AppSettings(env, {"flag": falsy})
        assert s._bool("flag", True) is False, f"Expected False for {falsy!r}"


def test_appsettings_bool_helper_falls_back_to_default() -> None:
    """_bool() returns the default when the key is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {})
    assert s._bool("missing", True) is True
    assert s._bool("missing", False) is False


def test_appsettings_str_helper_returns_db_value() -> None:
    """_str() returns the DB string when present."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {"some_text": "hello"})
    assert s._str("some_text", None) == "hello"


def test_appsettings_str_helper_falls_back_to_default() -> None:
    """_str() returns the default when key is absent."""
    from core.settings import get_settings
    from services.app_settings import AppSettings

    env = get_settings()
    s = AppSettings(env, {})
    assert s._str("missing", "default") == "default"
    assert s._str("missing", None) is None
```

- [ ] **Step 2: Run tests to verify they fail**

```
docker compose exec api pytest tests/test_app_settings.py -k "appsettings" -v
```

Expected: FAIL — `ImportError: cannot import name 'AppSettings'`

- [ ] **Step 3: Create `api/services/app_settings.py`**

```python
"""AppSettings — central authority for all configuration.

Wraps the env-only Settings class. The three DB-tunable fields are resolved
from the settings table with env fallback. All other attributes delegate
transparently to the underlying Settings instance via __getattr__.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import get_db
from models.app_setting import AppSetting


class AppSettings:
    """Central authority for all configuration — env base + DB runtime overrides."""

    def __init__(self, env: Settings, db_overrides: dict[str, str]) -> None:
        self._env = env
        self._db = db_overrides

    # ── typed helpers ──────────────────────────────────────────────────────────
    # All values are stored as TEXT in the DB. Each helper converts to the
    # correct Python type, falling back to the env default when the row is absent.

    def _int(self, name: str, default: int) -> int:
        """Resolve an integer setting: DB value first, env default fallback."""
        raw = self._db.get(name)
        return int(raw) if raw is not None else default

    def _bool(self, name: str, default: bool) -> bool:
        """Resolve a boolean setting: 'true'/'1'/'yes' → True, else False."""
        raw = self._db.get(name)
        return raw.lower() in ("true", "1", "yes") if raw is not None else default

    def _str(self, name: str, default: str | None) -> str | None:
        """Resolve a string setting: DB value first, default fallback."""
        raw = self._db.get(name)
        return raw if raw is not None else default

    # ── DB-tunable properties ──────────────────────────────────────────────────

    @property
    def max_photos_per_entry(self) -> int:
        """Maximum photos allowed per log entry."""
        return self._int("max_photos_per_entry", self._env.max_photos_per_entry)

    @property
    def photo_retention_days(self) -> int:
        """Number of days approved entry photos are retained on disk."""
        return self._int("photo_retention_days", self._env.photo_retention_days)

    @property
    def session_duration_hours(self) -> int:
        """Manager session cookie lifetime in hours."""
        return self._int("session_duration_hours", self._env.session_duration_hours)

    # ── passthrough for all other env settings ─────────────────────────────────

    def __getattr__(self, name: str) -> object:
        """Delegate any non-overridden attribute to the underlying env Settings."""
        return getattr(self._env, name)


async def get_app_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    env: Annotated[Settings, Depends(get_settings)],
) -> AppSettings:
    """FastAPI dependency — returns the central settings authority for this request."""
    rows = (await db.execute(select(AppSetting))).scalars().all()
    return AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
```

- [ ] **Step 4: Run tests to verify they pass**

```
docker compose exec api pytest tests/test_app_settings.py -k "appsettings" -v
```

Expected: all 8 unit tests PASS

- [ ] **Step 5: Commit**

```bash
git add api/services/app_settings.py api/tests/test_app_settings.py
git commit -m "feat(iss-026): add AppSettings central authority with typed helpers"
```

---

## Task 3: Admin router + integration tests

**Files:**
- Create: `api/schemas/admin.py`
- Create: `api/routers/admin.py`
- Modify: `api/main.py`
- Modify: `api/tests/test_app_settings.py` (add integration tests)

- [ ] **Step 1: Add failing integration tests to `api/tests/test_app_settings.py`**

Append after the unit tests:

```python
# ── Integration tests for GET/PATCH /api/admin/settings ──────────────────────

from httpx import AsyncClient


async def test_get_admin_settings_returns_seeded_defaults(
    client: AsyncClient, auth: dict
) -> None:
    """GET /api/admin/settings returns the seeded default values."""
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["max_photos_per_entry"] == 5
    assert data["photo_retention_days"] == 730
    assert data["session_duration_hours"] == 24


async def test_get_admin_settings_requires_auth(client: AsyncClient) -> None:
    """Unauthenticated request is rejected."""
    r = await client.get("/api/admin/settings")
    assert r.status_code == 401


async def test_patch_admin_settings_updates_single_field(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH updates a single field; others are unchanged."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 10}
    )
    assert r.status_code == 200
    data = r.json()
    assert data["max_photos_per_entry"] == 10
    assert data["photo_retention_days"] == 730   # unchanged
    assert data["session_duration_hours"] == 24  # unchanged


async def test_patch_admin_settings_get_reflects_change(
    client: AsyncClient, auth: dict
) -> None:
    """Subsequent GET reflects a PATCHed value."""
    await client.patch(
        "/api/admin/settings", headers=auth, json={"session_duration_hours": 48}
    )
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.json()["session_duration_hours"] == 48


async def test_patch_admin_settings_rejects_zero(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH rejects zero (ge=1 constraint)."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"max_photos_per_entry": 0}
    )
    assert r.status_code == 422


async def test_patch_admin_settings_rejects_negative(
    client: AsyncClient, auth: dict
) -> None:
    """PATCH rejects negative values."""
    r = await client.patch(
        "/api/admin/settings", headers=auth, json={"photo_retention_days": -1}
    )
    assert r.status_code == 422


async def test_patch_admin_settings_requires_auth(client: AsyncClient) -> None:
    """Unauthenticated PATCH is rejected."""
    r = await client.patch(
        "/api/admin/settings", json={"max_photos_per_entry": 5}
    )
    assert r.status_code == 401
```

- [ ] **Step 2: Run tests to verify they fail**

```
docker compose exec api pytest tests/test_app_settings.py -k "admin" -v
```

Expected: FAIL — `404 Not Found` (router not registered yet)

- [ ] **Step 3: Create `api/schemas/admin.py`**

```python
"""Pydantic schemas for the admin settings endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AdminSettingsResponse(BaseModel):
    """Current values of all runtime-tunable settings."""

    max_photos_per_entry: int
    photo_retention_days: int
    session_duration_hours: int


class AdminSettingsUpdate(BaseModel):
    """Partial update for runtime-tunable settings. Only provided fields are written."""

    max_photos_per_entry: int | None = Field(None, ge=1)
    photo_retention_days: int | None = Field(None, ge=1)
    session_duration_hours: int | None = Field(None, ge=1)
```

- [ ] **Step 4: Create `api/routers/admin.py`**

```python
"""Admin router — runtime-tunable settings management."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.app_setting import AppSetting
from schemas.admin import AdminSettingsResponse, AdminSettingsUpdate
from services.app_settings import AppSettings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def get_admin_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AdminSettingsResponse:
    """Return current values of all runtime-tunable settings."""
    rows = (await db.execute(select(AppSetting))).scalars().all()
    env = get_settings()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
    )


@router.patch(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def update_admin_settings(
    body: AdminSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AdminSettingsResponse:
    """Update one or more runtime-tunable settings. Returns updated state."""
    updates = {k: str(v) for k, v in body.model_dump(exclude_none=True).items()}

    for name, value in updates.items():
        row = (
            await db.execute(select(AppSetting).where(AppSetting.name == name))
        ).scalar_one_or_none()
        if row is None:
            db.add(AppSetting(name=name, value_type="int", value=value))
        else:
            row.value = value

    if updates:
        await db.commit()

    rows = (await db.execute(select(AppSetting))).scalars().all()
    env = get_settings()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
    )
```

- [ ] **Step 5: Register the admin router in `api/main.py`**

Add after the existing imports and registrations:

```python
from routers.admin import router as admin_router
```

Add after the last `app.include_router(...)` line:

```python
app.include_router(admin_router, prefix="/api")
```

The full imports block in `main.py` becomes:

```python
from routers.admin import router as admin_router
from routers.auth import router as auth_router
from routers.analytics import router as analytics_router
from routers.documents import router as documents_router
from routers.log_entries import router as log_entries_router
from routers.logo import router as logo_router
from routers.managers import router as managers_router
from routers.reports import router as reports_router
from routers.volunteers import router as volunteers_router
```

And the registrations:

```python
app.include_router(admin_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(log_entries_router, prefix="/api")
app.include_router(logo_router, prefix="/api")
app.include_router(managers_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(volunteers_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
```

- [ ] **Step 6: Run tests to verify they pass**

```
docker compose exec api pytest tests/test_app_settings.py -v
```

Expected: all tests PASS (migration smoke test + unit tests + integration tests)

- [ ] **Step 7: Commit**

```bash
git add api/schemas/admin.py api/routers/admin.py api/main.py api/tests/test_app_settings.py
git commit -m "feat(iss-026): add admin router with GET/PATCH /api/admin/settings"
```

---

## Task 4: Migrate call sites to get_app_settings

Replace all remaining direct `get_settings()` calls in routes with the `get_app_settings` dependency so every route uses the central authority.

**Files:**
- Modify: `api/routers/log_entries.py`
- Modify: `api/routers/auth.py`
- Modify: `api/routers/documents.py`

- [ ] **Step 1: Update `api/routers/log_entries.py`**

There are 4 call sites (lines 143, 258, 301, 330). All call `get_settings().max_photos_per_entry` directly.

Replace the import at the top of the file:

```python
# Remove:
from core.settings import get_settings

# Add:
from services.app_settings import AppSettings, get_app_settings
```

**Handler 1 — `get_photo_limit` (line ~140):**

```python
# Before:
@router.get("/photo-limit")
async def get_photo_limit() -> dict:
    """Return the configured maximum photos per log entry. Used by n8n workflows."""
    return {"max_photos": get_settings().max_photos_per_entry}

# After:
@router.get("/photo-limit")
async def get_photo_limit(
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> dict:
    """Return the configured maximum photos per log entry. Used by n8n workflows."""
    return {"max_photos": settings.max_photos_per_entry}
```

**Handlers 2, 3, 4 — the three photo upload/management handlers (lines ~255, ~298, ~327):**

Each handler that contains `max_photos = get_settings().max_photos_per_entry` or `resp.max_photos = get_settings().max_photos_per_entry`:

1. Add `settings: Annotated[AppSettings, Depends(get_app_settings)]` to the handler's parameter list (alongside the existing `db` parameter).
2. Replace `get_settings().max_photos_per_entry` with `settings.max_photos_per_entry`.

- [ ] **Step 2: Update `api/routers/auth.py`**

Replace imports:

```python
# Remove:
from core.settings import Settings, get_settings

# Add:
from services.app_settings import AppSettings, get_app_settings
```

Update `login` handler signature — change:

```python
settings: Annotated[Settings, Depends(get_settings)],
```

to:

```python
settings: Annotated[AppSettings, Depends(get_app_settings)],
```

Update `logout` handler signature — change:

```python
settings: Annotated[Settings, Depends(get_settings)],
```

to:

```python
settings: Annotated[AppSettings, Depends(get_app_settings)],
```

The body of both handlers is unchanged — `settings.api_secret_key`, `settings.cookie_secure`, `settings.session_duration_hours` all work via `AppSettings.__getattr__` or the typed property.

- [ ] **Step 3: Update `api/routers/documents.py`**

Replace imports:

```python
# Remove:
from core.settings import get_settings

# Add:
from services.app_settings import AppSettings, get_app_settings
```

Update `download_consent_pdf` handler — add `settings` parameter and remove the direct call:

```python
# Before:
@router.get("/consent-pdf", response_model=None, dependencies=[Depends(require_manager)])
async def download_consent_pdf(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StreamingResponse:
    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")
    settings = get_settings()
    pdf_bytes = render_consent_pdf(manager, settings.photo_retention_days)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="soglasje_gdpr.pdf"'},
    )

# After:
@router.get("/consent-pdf", response_model=None, dependencies=[Depends(require_manager)])
async def download_consent_pdf(
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> StreamingResponse:
    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")
    pdf_bytes = render_consent_pdf(manager, settings.photo_retention_days)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="soglasje_gdpr.pdf"'},
    )
```

- [ ] **Step 4: Run the full test suite**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS. If any test fails due to the Settings → AppSettings type change, update the relevant type annotation.

- [ ] **Step 5: Commit**

```bash
git add api/routers/log_entries.py api/routers/auth.py api/routers/documents.py
git commit -m "feat(iss-026): migrate all route call sites to get_app_settings"
```

---

## Task 5: Frontend — Administracija page

**Files:**
- Modify: `frontend/js/api.js`
- Modify: `frontend/index.html`
- Create: `frontend/js/admin.js`
- Modify: `frontend/js/volunteers.js`

- [ ] **Step 1: Add `admin` namespace to `frontend/js/api.js`**

After the `documents` block (around line 184), add:

```js
    admin: {
      getSettings:    ()     => request('/admin/settings'),
      updateSettings: (data) => request('/admin/settings', { method: 'PATCH', body: JSON.stringify(data) }),
    },
```

- [ ] **Step 2: Add Administracija nav item and script tag to `frontend/index.html`**

After the `#documents` nav item (around line 63), add:

```html
      <a href="#admin" class="nav-item" data-page="admin">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        Administracija
      </a>
```

Also add the script tag after the existing `documents.js` script tag:

```html
<script src="/js/admin.js"></script>
```

- [ ] **Step 3: Create `frontend/js/admin.js`**

```js
'use strict';

async function renderAdmin() {
  document.querySelector('.topbar-title').textContent = 'Administracija';
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.dataset.page === 'admin');
  });

  const main = document.getElementById('main-content');
  main.innerHTML = '<div class="spinner"></div>';

  let current;
  try {
    current = await API.admin.getSettings();
  } catch (err) {
    main.innerHTML = `<div class="error-banner">${err.message}</div>`;
    return;
  }

  main.innerHTML = `
    <div class="page-content">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Sistemske nastavitve</h2>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label for="admin-max-photos">Maksimalno število fotografij na vnos</label>
            <input id="admin-max-photos" type="number" min="1" class="form-control"
              value="${current.max_photos_per_entry}">
          </div>
          <div class="form-group">
            <label for="admin-retention">Čas hrambe fotografij (dni)</label>
            <input id="admin-retention" type="number" min="1" class="form-control"
              value="${current.photo_retention_days}">
          </div>
          <div class="form-group">
            <label for="admin-session">Trajanje seje (ure)</label>
            <input id="admin-session" type="number" min="1" class="form-control"
              value="${current.session_duration_hours}">
          </div>
          <div class="form-actions">
            <button id="admin-save-btn" class="btn btn-primary">Shrani nastavitve</button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('admin-save-btn').addEventListener('click', async () => {
    const btn = document.getElementById('admin-save-btn');
    const maxPhotos = parseInt(document.getElementById('admin-max-photos').value, 10);
    const retention = parseInt(document.getElementById('admin-retention').value, 10);
    const session  = parseInt(document.getElementById('admin-session').value, 10);

    if ([maxPhotos, retention, session].some(v => isNaN(v) || v < 1)) {
      showToast('Vse vrednosti morajo biti cela števila večja od 0.', 'error');
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Shranjevanje…';

    try {
      await API.admin.updateSettings({
        max_photos_per_entry: maxPhotos,
        photo_retention_days: retention,
        session_duration_hours: session,
      });
      showToast('Nastavitve so bile shranjene.');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Shrani nastavitve';
    }
  });
}
```

- [ ] **Step 4: Add `#admin` routing in `frontend/js/volunteers.js`**

After the `#documents` branch (line 217–218), add:

```js
  } else if (hash === '#admin') {
    renderAdmin();
```

The block around line 215–221 becomes:

```js
  } else if (hash === '#settings') {
    renderSettings();
  } else if (hash === '#documents') {
    renderDocuments();
  } else if (hash === '#admin') {
    renderAdmin();
  } else {
    renderList();
```

- [ ] **Step 5: Rebuild the frontend container and smoke-test in browser**

```
docker compose up -d --build frontend
```

Navigate to `http://localhost:80`, log in, click "Administracija" in the sidebar. Verify:
- Page loads with correct current values (5, 730, 24)
- Change a value, click "Shrani nastavitve" → success toast
- Reload the page → saved value persists

- [ ] **Step 6: Run full test suite**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS

- [ ] **Step 7: Commit**

```bash
git add frontend/js/api.js frontend/index.html frontend/js/admin.js frontend/js/volunteers.js
git commit -m "feat(iss-026): add Administracija page with runtime-tunable settings UI"
```

---

## Post-implementation

After all 5 tasks are done and tests pass:

```bash
docker compose exec api pytest tests/ -v
```

Expected: full suite green. Then run graphify:

```bash
graphify update .
git add graphify-out/
git commit -m "chore: update graphify knowledge graph"
```
