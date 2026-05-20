# Settings Table (ISS-026) Design

## Goal

Introduce a `settings` DB table as the runtime-tunable configuration layer, and a single `AppSettings` dependency that is the central authority for all configuration — both env-based and DB-overridable — so every caller gets consistent answers from one place.

## Architecture

Three configuration sources currently exist:

- **Env vars / `Settings` class** (`api/core/settings.py`) — secrets, infra URLs, and fallback defaults. Never queried from the DB.
- **`Manager` model** — NGO identity, contact details, SMTP config, WhatsApp phone. Entity data describing this NGO.
- **`settings` table** (new) — runtime-tunable, non-secret, non-infra values. Can be changed from the dashboard without restarting containers.

**`gdpr_additional_clauses` stays in the `Manager` model.** It is NGO-specific text tied to that entity, already has a working UI in Dokumenti, and migrating it adds churn without practical gain.

The new `AppSettings` class wraps the env `Settings` and the DB row dict. It exposes the three DB-tunable values as typed properties (DB-first, env fallback), and forwards all other attribute access to the underlying `Settings` via `__getattr__`. All routes replace `Depends(get_settings)` with `Depends(get_app_settings)`.

## Tech Stack

Python / FastAPI / SQLAlchemy 2.x async / Alembic / Pydantic / Vanilla JS

---

## Data Layer

### `settings` table

```sql
CREATE TABLE settings (
    id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name  TEXT NOT NULL UNIQUE,
    type  TEXT NOT NULL,   -- 'int' | 'bool' | 'text' | 'json'
    value TEXT
);
```

### Seed rows (inserted in the Alembic migration)

| name | type | value |
|---|---|---|
| `max_photos_per_entry` | int | 5 |
| `photo_retention_days` | int | 730 |
| `session_duration_hours` | int | 24 |

Seeds use `INSERT ... ON CONFLICT DO NOTHING` so re-running the migration on an existing install does not overwrite customised values.

### ORM model

New file `api/models/app_setting.py`:

```python
class AppSetting(Base):
    __tablename__ = "settings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, ...)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
```

---

## API Layer

### Central authority: `AppSettings`

New file `api/services/app_settings.py`:

```python
class AppSettings:
    """Central authority for all configuration.

    DB-tunable values are resolved from the settings table with env fallback.
    All other settings delegate transparently to the underlying env Settings.
    """

    def __init__(self, env: Settings, db_overrides: dict[str, str]):
        self._env = env
        self._db = db_overrides

    # Typed helpers — all values are stored as TEXT in the DB; each helper
    # converts to the appropriate Python type, with env fallback when missing.

    def _int(self, name: str, default: int) -> int:
        raw = self._db.get(name)
        return int(raw) if raw is not None else default

    def _bool(self, name: str, default: bool) -> bool:
        raw = self._db.get(name)
        return raw.lower() in ("true", "1", "yes") if raw is not None else default

    def _str(self, name: str, default: str | None) -> str | None:
        raw = self._db.get(name)
        return raw if raw is not None else default

    # New DB-tunable settings always get a typed property using the appropriate
    # helper above. The type column in the DB is a hint for the admin UI
    # (what control to render); the Python layer derives the type from the
    # property definition, not from the DB column.

    @property
    def max_photos_per_entry(self) -> int:
        return self._int("max_photos_per_entry", self._env.max_photos_per_entry)

    @property
    def photo_retention_days(self) -> int:
        return self._int("photo_retention_days", self._env.photo_retention_days)

    @property
    def session_duration_hours(self) -> int:
        return self._int("session_duration_hours", self._env.session_duration_hours)

    def __getattr__(self, name: str):
        return getattr(self._env, name)


async def get_app_settings(
    db: AsyncSession = Depends(get_db),
    env: Settings = Depends(get_settings),
) -> AppSettings:
    rows = (await db.execute(select(AppSetting))).scalars().all()
    return AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
```

### Caller migration

All routes currently using `Depends(get_settings)` for the three tunable values switch to `Depends(get_app_settings)`. The existing `get_settings()` stays in `core/settings.py` as the env-only fallback used internally by `AppSettings`; no route calls it directly anymore.

Affected call sites:
- Photo upload route — `max_photos_per_entry`
- Auth / login route — `session_duration_hours`
- Consent PDF route — `photo_retention_days`

### Admin router

New file `api/routers/admin.py`, prefix `/api/admin`, protected by `require_manager`.

```
GET  /api/admin/settings  → AdminSettingsResponse
PATCH /api/admin/settings  → AdminSettingsResponse
```

```python
class AdminSettingsResponse(BaseModel):
    max_photos_per_entry: int
    photo_retention_days: int
    session_duration_hours: int

class AdminSettingsUpdate(BaseModel):
    max_photos_per_entry: int | None = None
    photo_retention_days: int | None = None
    session_duration_hours: int | None = None
```

`PATCH` upserts each non-None field into the `settings` table. Returns the full current state after update.

Router registered in `api/main.py`:

```python
from routers.admin import router as admin_router
app.include_router(admin_router, prefix="/api")
```

### Env vars

The three env var fields remain in `Settings` as fallback defaults. In `.env.example` they get a comment noting the DB value takes precedence at runtime. No existing `.env` file breaks.

---

## Frontend

### Navigation

New nav item added to `frontend/index.html` sidebar after "Dokumenti":

```html
<a href="#admin" class="nav-item" data-page="admin">
  <svg>...</svg>
  Administracija
</a>
```

New script tag: `<script src="/js/admin.js"></script>`

### Admin page (`frontend/js/admin.js`)

Renders on `#admin` hash. Calls `GET /api/admin/settings` on load. Displays one card — "Sistemske nastavitve" — with three numeric inputs and an explicit "Shrani nastavitve" button.

**No auto-save.** These are system-level values; accidental saves have real consequences. Explicit save only.

On save: `PATCH /api/admin/settings` with the three field values. Success and error feedback via existing `showToast()`.

`API.admin` namespace added to `frontend/js/api.js`:

```js
admin: {
  getSettings: () => request('/admin/settings'),
  updateSettings: (data) => request('/admin/settings', { method: 'PATCH', body: JSON.stringify(data) }),
}
```

### Page scaffold

The admin page is intentionally minimal for now — one card with three fields. It is the scaffolding for health status (ISS-012), backup controls, and error log (ISS-014) which will be added in subsequent issues.

---

## Testing

### Unit tests (`api/tests/test_app_settings.py`)

- `AppSettings` resolves DB value when present
- `AppSettings` falls back to env value when DB row missing
- `AppSettings` passthrough delegates to env for non-tunable fields (e.g. `emso_encryption_key`)

### Integration tests (`api/tests/test_admin.py`)

- `GET /api/admin/settings` returns seeded defaults (200)
- `GET /api/admin/settings` requires auth (401)
- `PATCH /api/admin/settings` updates a value and GET reflects the change (200)
- `PATCH /api/admin/settings` with partial payload only updates provided fields (200)
- `PATCH /api/admin/settings` rejects non-integer values (422)

---

## Migration

Single Alembic migration (`012_settings_table`):

1. `CREATE TABLE settings ...`
2. `INSERT INTO settings (name, type, value) VALUES ... ON CONFLICT DO NOTHING` for all three rows

No data from existing tables is moved. No existing routes break before the caller-migration step.

---

## Out of scope

- `gdpr_additional_clauses` — stays in Manager model; will be evaluated separately if needed
- SMTP fields, WhatsApp phone, Evolution API URL — entity data in Manager; no change
- Caching the settings query — single-tenant app, low-frequency read paths; a DB query per relevant request is sufficient
- `bool` and `json` type support in the admin UI — table schema supports them for future use; UI only handles `int` values in this pass
