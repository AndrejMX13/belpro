# WhatsApp Phone — Single Source of Truth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `ngo_whatsapp_phone` a single authoritative source of truth — seeded from `.env` on first boot, auto-synced from Evolution API when connected, normalized to WhatsApp-native digit format, and kept consistent across DB, `.env`, and the settings UI.

**Architecture:** A new `EvolutionClient` service queries `GET /instance/fetchInstances` on every settings page load; if the instance is `open` with a different phone than DB, it auto-syncs DB and `.env`. The settings UI reflects live connection state (read-only when `open`/`connecting`, editable when `close`/`unreachable`). Number normalization (strip `+`, spaces, dashes → digits only) is applied at every write boundary.

**Tech Stack:** Python 3.11, FastAPI/Pydantic v2, SQLAlchemy async, httpx (new dep), vanilla JS

---

## Context & Key Decisions

- **WhatsApp-native format:** store digits only, no `+` (e.g. `38640123456`). Display adds `+` prefix.
- **Priority hierarchy:** `.env` seeds DB on first boot (null → value). After that, Evolution API is authoritative when `open`; DB is the cached value otherwise.
- **`AUTHENTICATION_API_KEY`** (global Evolution API admin key) is not currently passed to the `api` container — it must be added to `docker-compose.yml`. `EVOLUTION_API_KEY` is the per-instance key used by n8n and is insufficient for `fetchInstances`.
- **`.env` in Docker:** the `api` service uses explicit `environment:` vars (no `env_file:` directive), so `.env` does not exist inside the container. A volume mount `- ./.env:/app/.env:rw` is required for the API to write to it. The file is written for human reference and next-restart pickup — not for live env var updates.
- **`@lid` JIDs:** Android users may cause Evolution API to return `owner: "245616546422929@lid"`. On v2.3.7 this cannot be resolved. Show a message; never crash. Upgrade to v2.4.0+ when available. See `docs/evolution-lid-resolution.md`.
- **`.env` write failure:** non-fatal. Log the warning, return `wa_env_write_ok: false` in the response so the UI can display a warning.
- **Auto-sync is silent:** if phone changes on settings load, update DB + `.env` and show a single toast. No user confirmation needed.

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `api/utils/__init__.py` | Package marker |
| Create | `api/utils/phone.py` | Number normalization |
| Create | `api/utils/env_writer.py` | Safe in-place `.env` key update |
| Create | `api/services/evolution.py` | Evolution API HTTP client |
| Create | `api/tests/test_phone_utils.py` | Unit tests for normalizer |
| Create | `api/tests/test_env_writer.py` | Unit tests for env writer |
| Create | `api/tests/test_evolution_service.py` | Unit tests for Evolution client |
| Modify | `api/core/settings.py` | Add `authentication_api_key`, `ngo_whatsapp_phone` |
| Modify | `api/main.py` | Startup seeding from `.env` → DB |
| Modify | `api/schemas/manager.py` | Add `ConfigInfoResponse`; phone validator on `ManagerUpdate` |
| Modify | `api/routers/managers.py` | Auto-sync in `get_config_info`; normalize in `update_manager` |
| Modify | `api/requirements.txt` | Add `httpx` |
| Modify | `docker-compose.yml` | Add `AUTHENTICATION_API_KEY` + `.env` volume to `api` service |
| Modify | `frontend/js/volunteers.js` | Phone display, connection badges, read-only/editable states |

---

### Task 1: Infrastructure prep

**Files:**
- Modify: `docker-compose.yml` (api service environment + volumes)
- Modify: `api/requirements.txt`
- Modify: `.env.example`

- [ ] **Step 1: Check for `pytest-asyncio` in requirements.txt**

```powershell
docker compose exec api python -c "import pytest_asyncio; print(pytest_asyncio.__version__)"
```

If this fails, add `pytest-asyncio>=0.23` to `api/requirements.txt`.

Also check `asyncio_mode` config — if no `asyncio_mode = "auto"` in `pytest.ini` or `pyproject.toml`, the new async tests in Tasks 4–6 will need `@pytest.mark.asyncio` decorators (they are included in this plan by default).

- [ ] **Step 2: Add `httpx` to `api/requirements.txt`**

Append to `api/requirements.txt`:
```
httpx>=0.27
```

- [ ] **Step 3: Add `AUTHENTICATION_API_KEY`, `NGO_WHATSAPP_PHONE` to the `api` service environment in `docker-compose.yml`**

In the `api` service `environment:` block, after `EVOLUTION_INSTANCE_NAME: ${EVOLUTION_INSTANCE_NAME}`, add:

```yaml
      AUTHENTICATION_API_KEY: ${AUTHENTICATION_API_KEY}
      NGO_WHATSAPP_PHONE: ${NGO_WHATSAPP_PHONE:-}
```

- [ ] **Step 4: Add `.env` volume mount to the `api` service in `docker-compose.yml`**

The current `volumes:` block for the api service is:
```yaml
    volumes:
      - api_photos:/app/photos
      - api_pdfs:/app/pdfs
```

Add the `.env` bind mount:
```yaml
    volumes:
      - api_photos:/app/photos
      - api_pdfs:/app/pdfs
      - ./.env:/app/.env:rw
```

- [ ] **Step 5: Add `NGO_WHATSAPP_PHONE` to `.env.example`**

Append to `.env.example` (in the Evolution API section):
```
NGO_WHATSAPP_PHONE=
```

Also add an empty line to `.env` itself if `NGO_WHATSAPP_PHONE` is not already there:
```powershell
Add-Content "d:\Andrej\vsCode-workspace\BelPro\.env" "`nNGO_WHATSAPP_PHONE="
```

- [ ] **Step 6: Rebuild and verify**

```powershell
docker compose up -d --build api
docker compose logs api --tail=20
```

Expected: `Application startup complete.` — no errors.

- [ ] **Step 7: Commit**

```bash
git add docker-compose.yml api/requirements.txt .env.example
git commit -m "chore: add httpx, expose AUTHENTICATION_API_KEY + NGO_WHATSAPP_PHONE + .env mount to api service"
```

---

### Task 2: Phone normalization utility

**Files:**
- Create: `api/utils/__init__.py`
- Create: `api/utils/phone.py`
- Create: `api/tests/test_phone_utils.py`

- [ ] **Step 1: Write the failing tests**

Create `api/tests/test_phone_utils.py`:

```python
from api.utils.phone import normalize_phone


def test_strips_plus_prefix():
    assert normalize_phone("+38640123456") == "38640123456"


def test_strips_spaces():
    assert normalize_phone("+386 40 123 456") == "38640123456"


def test_strips_dashes():
    assert normalize_phone("+386-40-123-456") == "38640123456"


def test_strips_parentheses():
    assert normalize_phone("+1 (555) 123-4567") == "15551234567"


def test_already_normalized():
    assert normalize_phone("38640123456") == "38640123456"


def test_none_returns_none():
    assert normalize_phone(None) is None


def test_empty_string_returns_none():
    assert normalize_phone("") is None


def test_whitespace_only_returns_none():
    assert normalize_phone("   ") is None


def test_too_short_returns_none():
    # Fewer than 7 digits is not a plausible phone number
    assert normalize_phone("+1234") is None


def test_jid_phone_part():
    # Evolution API owner field arrives as "38640123456@s.whatsapp.net"
    # Callers split on "@" before calling normalize — test the phone part
    assert normalize_phone("38640123456@s.whatsapp.net".split("@")[0]) == "38640123456"
```

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_phone_utils.py -v
```

Expected: `ModuleNotFoundError: No module named 'api.utils'`

- [ ] **Step 3: Create the package and implementation**

Create `api/utils/__init__.py` (empty).

Create `api/utils/phone.py`:

```python
import re


def normalize_phone(raw: str | None) -> str | None:
    """Return digits-only WhatsApp-native phone number, or None for invalid input.

    Strips +, spaces, dashes, parentheses. Returns None if fewer than 7 digits remain.
    Store the result directly as-is — Evolution API and WhatsApp expect no + prefix.
    For display, callers should prepend '+'.
    """
    if not raw:
        return None
    digits = re.sub(r"[^\d]", "", raw)
    if len(digits) < 7:
        return None
    return digits
```

- [ ] **Step 4: Run tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_phone_utils.py -v
```

Expected: 10 passed.

- [ ] **Step 5: Commit**

```bash
git add api/utils/__init__.py api/utils/phone.py api/tests/test_phone_utils.py
git commit -m "feat: add phone normalization utility (WhatsApp-native digit format)"
```

---

### Task 3: .env writer utility

**Files:**
- Create: `api/utils/env_writer.py`
- Create: `api/tests/test_env_writer.py`

- [ ] **Step 1: Write the failing tests**

Create `api/tests/test_env_writer.py`:

```python
from pathlib import Path
from api.utils.env_writer import write_env_key


def test_creates_file_with_new_key(tmp_path):
    env = tmp_path / ".env"
    result = write_env_key("FOO", "bar", env)
    assert result is True
    assert "FOO=bar" in env.read_text()


def test_appends_key_to_existing_file(tmp_path):
    env = tmp_path / ".env"
    env.write_text("EXISTING=value\n")
    write_env_key("FOO", "bar", env)
    content = env.read_text()
    assert "EXISTING=value" in content
    assert "FOO=bar" in content


def test_updates_existing_key_in_place(tmp_path):
    env = tmp_path / ".env"
    env.write_text("FOO=old\nBAR=keep\n")
    write_env_key("FOO", "new", env)
    content = env.read_text()
    assert "FOO=new" in content
    assert "FOO=old" not in content
    assert "BAR=keep" in content


def test_does_not_duplicate_key(tmp_path):
    env = tmp_path / ".env"
    env.write_text("FOO=old\n")
    write_env_key("FOO", "new", env)
    assert env.read_text().count("FOO=") == 1


def test_preserves_comments(tmp_path):
    env = tmp_path / ".env"
    env.write_text("# comment\nFOO=old\n")
    write_env_key("FOO", "new", env)
    assert "# comment" in env.read_text()


def test_returns_false_on_unwritable_path():
    result = write_env_key("FOO", "bar", Path("/no/such/dir/.env"))
    assert result is False
```

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_env_writer.py -v
```

Expected: `ModuleNotFoundError: No module named 'api.utils.env_writer'`

- [ ] **Step 3: Implement**

Create `api/utils/env_writer.py`:

```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_env_key(key: str, value: str, env_path: Path) -> bool:
    """Update or append KEY=value in a .env file. Returns True on success, False on failure.

    Never raises — failures are logged as warnings. Existing key is replaced in-place;
    new keys are appended. Comments and unrelated lines are preserved.
    """
    try:
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)
            updated = False
            new_lines = []
            for line in lines:
                if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    new_lines.append(line)
            if not updated:
                if new_lines and not new_lines[-1].endswith("\n"):
                    new_lines.append("\n")
                new_lines.append(f"{key}={value}\n")
            env_path.write_text("".join(new_lines), encoding="utf-8")
        else:
            env_path.write_text(f"{key}={value}\n", encoding="utf-8")
        return True
    except Exception as exc:
        logger.warning("Failed to write %s to %s: %s", key, env_path, exc)
        return False
```

- [ ] **Step 4: Run tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_env_writer.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add api/utils/env_writer.py api/tests/test_env_writer.py
git commit -m "feat: add .env key writer utility"
```

---

### Task 4: Evolution API service client

**Files:**
- Create: `api/services/evolution.py`
- Create: `api/tests/test_evolution_service.py`

> **Note:** Before implementing, verify the actual `fetchInstances` response shape by running:
> ```powershell
> docker compose exec api python -c "import httpx,json,os; r=httpx.get('http://evolution-api:8080/instance/fetchInstances',headers={'apikey':os.environ['AUTHENTICATION_API_KEY']}); print(json.dumps(r.json(),indent=2))"
> ```
> The implementation below handles both `instance.status` and `instance.state` fields to cover minor version differences.

- [ ] **Step 1: Write the failing tests**

Create `api/tests/test_evolution_service.py`:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.evolution import EvolutionClient

CLIENT = EvolutionClient(
    base_url="http://localhost:8180",
    api_key="testkey",
    instance_name="belpro",
)

OPEN_RESPONSE = [
    {
        "instance": {
            "instanceName": "belpro",
            "status": "open",
            "owner": "38640123456@s.whatsapp.net",
        }
    }
]
CLOSE_RESPONSE = [
    {"instance": {"instanceName": "belpro", "status": "close"}}
]
LID_RESPONSE = [
    {
        "instance": {
            "instanceName": "belpro",
            "status": "open",
            "owner": "245616546422929@lid",
        }
    }
]
EMPTY_RESPONSE: list = []


def _make_mock_http(json_data: list) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status = MagicMock()
    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=False)
    mock_http.get = AsyncMock(return_value=mock_resp)
    return mock_http


@pytest.mark.asyncio
async def test_connected_returns_normalized_phone_and_open_state():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(OPEN_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone == "38640123456"
    assert state == "open"


@pytest.mark.asyncio
async def test_disconnected_returns_none_and_close_state():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(CLOSE_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "close"


@pytest.mark.asyncio
async def test_network_error_returns_unreachable():
    with patch("httpx.AsyncClient", side_effect=Exception("connection refused")):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "unreachable"


@pytest.mark.asyncio
async def test_lid_jid_returns_lid_unsupported():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(LID_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "lid_unsupported"


@pytest.mark.asyncio
async def test_instance_not_in_response_returns_close():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(EMPTY_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "close"
```

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_evolution_service.py -v
```

Expected: `ModuleNotFoundError: No module named 'api.services.evolution'`

- [ ] **Step 3: Implement**

Create `api/services/evolution.py`:

```python
import logging

import httpx

from api.utils.phone import normalize_phone

logger = logging.getLogger(__name__)


class EvolutionClient:
    """Async HTTP client for the Evolution API WhatsApp gateway."""

    def __init__(self, base_url: str, api_key: str, instance_name: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._instance_name = instance_name

    async def get_connected_phone(self) -> tuple[str | None, str]:
        """Return (normalized_phone, state) for the configured instance.

        States: "open" | "connecting" | "close" | "unreachable" | "lid_unsupported"
        phone is non-None only when state is "open" and owner is a resolvable E.164 JID.

        v2.3.7 note: Android users may appear as @lid JIDs which cannot be resolved.
        Upgrade to v2.4.0+ if @lid owners are seen. See docs/evolution-lid-resolution.md.
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"{self._base_url}/instance/fetchInstances",
                    headers={"apikey": self._api_key},
                )
                resp.raise_for_status()
                instances: list = resp.json()
        except Exception as exc:
            logger.warning("Evolution API unreachable at %s: %s", self._base_url, exc)
            return None, "unreachable"

        for item in instances:
            inst = item.get("instance", {})
            if inst.get("instanceName") != self._instance_name:
                continue

            # "status" is standard in v2.3.x; "state" appears in some versions
            state: str = inst.get("status") or inst.get("state") or "close"
            owner: str | None = inst.get("owner")

            if not owner:
                return None, state

            if owner.endswith("@lid"):
                logger.warning(
                    "Evolution API returned @lid JID for instance '%s' — "
                    "upgrade to v2.4.0+ to resolve. See docs/evolution-lid-resolution.md.",
                    self._instance_name,
                )
                return None, "lid_unsupported"

            phone = normalize_phone(owner.split("@")[0])
            return phone, state

        return None, "close"
```

- [ ] **Step 4: Run tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_evolution_service.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add api/services/evolution.py api/tests/test_evolution_service.py
git commit -m "feat: add EvolutionClient with connected phone resolution"
```

---

### Task 5: Settings update + startup seeding

**Files:**
- Modify: `api/core/settings.py`
- Modify: `api/main.py`
- Modify: `api/tests/test_managers.py`

The seeding logic is extracted into a standalone async function `seed_whatsapp_phone_from_env` so it can be tested directly without spinning up the full ASGI lifespan.

- [ ] **Step 1: Write the failing test**

Add to `api/tests/test_managers.py` (at the top with other imports, add `from sqlalchemy import select` and `from api.models.manager import Manager` if not already present):

```python
@pytest.mark.asyncio
async def test_seed_whatsapp_phone_populates_null_db_field(db_session):
    """seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null."""
    from api.main import seed_whatsapp_phone_from_env
    from api.core.settings import Settings

    # Ensure DB has null phone
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = None
    await db_session.commit()

    fake_settings = Settings.model_construct(ngo_whatsapp_phone="+386 40 999 888")
    await seed_whatsapp_phone_from_env(db_session, fake_settings)

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640999888"


@pytest.mark.asyncio
async def test_seed_whatsapp_phone_does_not_overwrite_existing_value(db_session):
    """seed_whatsapp_phone_from_env leaves existing DB value untouched."""
    from api.main import seed_whatsapp_phone_from_env
    from api.core.settings import Settings

    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640111222"
    await db_session.commit()

    fake_settings = Settings.model_construct(ngo_whatsapp_phone="38640999888")
    await seed_whatsapp_phone_from_env(db_session, fake_settings)

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640111222"
```

> `Settings.model_construct(...)` creates a Settings instance without validation, bypassing required fields — suitable for unit tests that only need specific fields.

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_managers.py::test_seed_whatsapp_phone_populates_null_db_field tests/test_managers.py::test_seed_whatsapp_phone_does_not_overwrite_existing_value -v
```

Expected: `ImportError: cannot import name 'seed_whatsapp_phone_from_env' from 'api.main'`

- [ ] **Step 3: Add fields to `api/core/settings.py`**

After `evolution_instance_name`, add:

```python
    authentication_api_key: str = ""
    ngo_whatsapp_phone: str = ""
```

- [ ] **Step 4: Add seeding function and update lifespan in `api/main.py`**

Add to the imports block at the top of `api/main.py`:

```python
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.settings import Settings, get_settings
from api.models.manager import Manager
from api.utils.phone import normalize_phone
```

(Remove any duplicate existing imports of `text` or `select` if already present.)

Add this function **before** the `lifespan` definition:

```python
async def seed_whatsapp_phone_from_env(session: AsyncSession, settings: Settings) -> None:
    """Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null."""
    if not settings.ngo_whatsapp_phone:
        return
    normalized = normalize_phone(settings.ngo_whatsapp_phone)
    if not normalized:
        return
    manager = (await session.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager and not manager.ngo_whatsapp_phone:
        manager.ngo_whatsapp_phone = normalized
        await session.commit()
```

Update the `lifespan` function:

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null."""
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))

    settings = get_settings()
    async with AsyncSessionLocal() as session:
        await seed_whatsapp_phone_from_env(session, settings)

    yield
```

- [ ] **Step 5: Run new tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_managers.py::test_seed_whatsapp_phone_populates_null_db_field tests/test_managers.py::test_seed_whatsapp_phone_does_not_overwrite_existing_value -v
```

Expected: 2 passed.

- [ ] **Step 6: Run full test suite — no regressions**

```powershell
docker compose exec api pytest tests/ -v
```

Expected: all green.

- [ ] **Step 7: Commit**

```bash
git add api/core/settings.py api/main.py api/tests/test_managers.py
git commit -m "feat: add authentication_api_key + ngo_whatsapp_phone to Settings; seed DB from .env on startup"
```

---

### Task 6: ConfigInfoResponse schema + enhanced get_config_info

**Files:**
- Modify: `api/schemas/manager.py`
- Modify: `api/routers/managers.py`
- Modify: `api/tests/test_managers.py`

- [ ] **Step 1: Write failing tests**

Add to `api/tests/test_managers.py`:

```python
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_config_info_includes_wa_fields(client, auth_headers):
    with patch(
        "api.routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=(None, "unreachable")),
    ):
        resp = await client.get("/managers/me/config-info", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "wa_phone" in data
    assert "wa_state" in data
    assert "wa_synced" in data
    assert "wa_env_write_ok" in data
    assert data["wa_state"] == "unreachable"
    assert data["wa_synced"] is False


@pytest.mark.asyncio
async def test_config_info_auto_syncs_when_evolution_reports_new_phone(
    client, auth_headers, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = None
    await db_session.commit()

    with patch(
        "api.routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=("38640111222", "open")),
    ):
        resp = await client.get("/managers/me/config-info", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["wa_phone"] == "38640111222"
    assert data["wa_state"] == "open"
    assert data["wa_synced"] is True

    await db_session.refresh(manager)
    assert manager.ngo_whatsapp_phone == "38640111222"


@pytest.mark.asyncio
async def test_config_info_no_sync_when_phone_already_matches(
    client, auth_headers, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640111222"
    await db_session.commit()

    with patch(
        "api.routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=("38640111222", "open")),
    ):
        resp = await client.get("/managers/me/config-info", headers=auth_headers)

    assert resp.json()["wa_synced"] is False


@pytest.mark.asyncio
async def test_config_info_shows_db_phone_when_disconnected(
    client, auth_headers, db_session
):
    manager = (await db_session.execute(select(Manager).limit(1))).scalar_one()
    manager.ngo_whatsapp_phone = "38640999888"
    await db_session.commit()

    with patch(
        "api.routers.managers.EvolutionClient.get_connected_phone",
        new=AsyncMock(return_value=(None, "close")),
    ):
        resp = await client.get("/managers/me/config-info", headers=auth_headers)

    data = resp.json()
    assert data["wa_phone"] == "38640999888"
    assert data["wa_state"] == "close"
```

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_managers.py::test_config_info_includes_wa_fields tests/test_managers.py::test_config_info_auto_syncs_when_evolution_reports_new_phone tests/test_managers.py::test_config_info_no_sync_when_phone_already_matches tests/test_managers.py::test_config_info_shows_db_phone_when_disconnected -v
```

Expected: failures due to missing `wa_state` / wrong response shape.

- [ ] **Step 3: Add `ConfigInfoResponse` to `api/schemas/manager.py`**

Append after the last class in the file:

```python
class ConfigInfoResponse(BaseModel):
    """Response schema for GET /managers/me/config-info."""

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_from_name: str
    smtp_configured: bool
    evolution_api_admin_url: str
    wa_phone: str | None
    wa_state: str  # "open" | "connecting" | "close" | "unreachable" | "lid_unsupported"
    wa_synced: bool
    wa_env_write_ok: bool
```

- [ ] **Step 4: Replace `get_config_info` in `api/routers/managers.py`**

Add these imports at the top of `api/routers/managers.py` (alongside existing imports):

```python
import logging
from pathlib import Path

from api.services.evolution import EvolutionClient
from api.schemas.manager import ConfigInfoResponse
from api.utils.env_writer import write_env_key
```

Add the logger after the imports:

```python
logger = logging.getLogger(__name__)
```

Replace the entire `get_config_info` function body (keep the decorator):

```python
@router.get("/me/config-info", dependencies=[Depends(require_manager)])
async def get_config_info(
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ConfigInfoResponse:
    """Return config status for the settings UI; auto-syncs WhatsApp phone if connected."""
    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not configured.")

    client = EvolutionClient(
        base_url=settings.evolution_api_url,
        api_key=settings.authentication_api_key,
        instance_name=settings.evolution_instance_name,
    )
    live_phone, wa_state = await client.get_connected_phone()

    wa_synced = False
    wa_env_write_ok = True

    if wa_state == "open" and live_phone and live_phone != manager.ngo_whatsapp_phone:
        logger.info(
            "WhatsApp phone auto-sync: DB=%s → Evolution API=%s",
            manager.ngo_whatsapp_phone,
            live_phone,
        )
        manager.ngo_whatsapp_phone = live_phone
        await db.commit()
        wa_synced = True
        wa_env_write_ok = write_env_key("NGO_WHATSAPP_PHONE", live_phone, Path(".env"))
        if not wa_env_write_ok:
            logger.warning("Failed to write NGO_WHATSAPP_PHONE to .env after auto-sync")

    wa_phone = live_phone if wa_state == "open" else manager.ngo_whatsapp_phone
    smtp_configured = bool(manager.smtp_host and manager.smtp_user and settings.smtp_password)

    return ConfigInfoResponse(
        smtp_host=manager.smtp_host or "",
        smtp_port=manager.smtp_port or 587,
        smtp_user=manager.smtp_user or "",
        smtp_from_name=manager.smtp_from_name or "",
        smtp_configured=smtp_configured,
        evolution_api_admin_url=manager.evolution_api_admin_url or "http://localhost:8180/manager/login",
        wa_phone=wa_phone,
        wa_state=wa_state,
        wa_synced=wa_synced,
        wa_env_write_ok=wa_env_write_ok,
    )
```

- [ ] **Step 5: Run new tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_managers.py::test_config_info_includes_wa_fields tests/test_managers.py::test_config_info_auto_syncs_when_evolution_reports_new_phone tests/test_managers.py::test_config_info_no_sync_when_phone_already_matches tests/test_managers.py::test_config_info_shows_db_phone_when_disconnected -v
```

Expected: 4 passed.

- [ ] **Step 6: Run full test suite — no regressions**

```powershell
docker compose exec api pytest tests/ -v
```

Expected: all green.

- [ ] **Step 7: Commit**

```bash
git add api/schemas/manager.py api/routers/managers.py api/tests/test_managers.py
git commit -m "feat: ConfigInfoResponse with wa_phone/wa_state; auto-sync phone from Evolution API on settings load"
```

---

### Task 7: Normalize phone in update_manager + write .env on manual save

**Files:**
- Modify: `api/schemas/manager.py` (`ManagerUpdate`)
- Modify: `api/routers/managers.py` (`update_manager`)
- Modify: `api/tests/test_managers.py`

- [ ] **Step 1: Write failing tests**

Add to `api/tests/test_managers.py`:

```python
@pytest.mark.asyncio
async def test_update_manager_normalizes_whatsapp_phone(client, auth_headers):
    resp = await client.patch(
        "/managers/me",
        json={"ngo_whatsapp_phone": "+386 40 123 456"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["ngo_whatsapp_phone"] == "38640123456"


@pytest.mark.asyncio
async def test_update_manager_rejects_too_short_phone(client, auth_headers):
    resp = await client.patch(
        "/managers/me",
        json={"ngo_whatsapp_phone": "+123"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_update_manager_empty_phone_is_not_stored_as_empty_string(
    client, auth_headers
):
    # Empty string normalizes to None, which is excluded from the PATCH (no 422)
    resp = await client.patch(
        "/managers/me",
        json={"ngo_whatsapp_phone": ""},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    # DB must not contain an empty string
    assert resp.json()["ngo_whatsapp_phone"] != ""
```

- [ ] **Step 2: Run tests — verify they fail**

```powershell
docker compose exec api pytest tests/test_managers.py::test_update_manager_normalizes_whatsapp_phone tests/test_managers.py::test_update_manager_rejects_too_short_phone tests/test_managers.py::test_update_manager_empty_phone_is_not_stored_as_empty_string -v
```

Expected: first test fails (no normalization), second may pass or fail, third passes (200 already).

- [ ] **Step 3: Add phone validator to `ManagerUpdate` in `api/schemas/manager.py`**

Add `field_validator` to the imports at the top of the file:

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
```

Add this validator **inside** the `ManagerUpdate` class:

```python
    @field_validator("ngo_whatsapp_phone", mode="before")
    @classmethod
    def normalize_wa_phone(cls, v: str | None) -> str | None:
        """Normalize to WhatsApp-native digits-only format; reject unparseable values."""
        from api.utils.phone import normalize_phone

        if v is None:
            return None
        normalized = normalize_phone(v)
        if v and not normalized:
            raise ValueError("Telefonska številka je prekratka ali neveljavna.")
        return normalized
```

- [ ] **Step 4: Add `.env` write to `update_manager` in `api/routers/managers.py`**

In `update_manager`, after `await db.commit()` and before `await db.refresh(manager)`, add:

```python
    if "ngo_whatsapp_phone" in payload.model_fields_set and manager.ngo_whatsapp_phone:
        write_env_key("NGO_WHATSAPP_PHONE", manager.ngo_whatsapp_phone, Path(".env"))
```

- [ ] **Step 5: Run new tests — verify they pass**

```powershell
docker compose exec api pytest tests/test_managers.py::test_update_manager_normalizes_whatsapp_phone tests/test_managers.py::test_update_manager_rejects_too_short_phone tests/test_managers.py::test_update_manager_empty_phone_is_not_stored_as_empty_string -v
```

Expected: 3 passed.

- [ ] **Step 6: Run full test suite — no regressions**

```powershell
docker compose exec api pytest tests/ -v
```

Expected: all green.

- [ ] **Step 7: Commit**

```bash
git add api/schemas/manager.py api/routers/managers.py api/tests/test_managers.py
git commit -m "feat: normalize ngo_whatsapp_phone on PATCH; write .env on manual save"
```

---

### Task 8: Settings UI — display, badges, read-only states

**Files:**
- Modify: `frontend/js/volunteers.js`

No automated tests — verify manually in the browser after changes.

- [ ] **Step 1: Add `_waBadge` helper before `renderSettings`**

In `volunteers.js`, find the line `async function renderSettings()` and insert this function immediately **before** it:

```js
function _waBadge(state) {
  const map = {
    open:            '<span style="color:var(--success,#16a34a);font-size:0.85rem">✓ Povezano</span>',
    connecting:      '<span style="color:#d97706;font-size:0.85rem">⟳ Vzpostavljanje...</span>',
    close:           '<span style="color:var(--text-muted,#6b7280);font-size:0.85rem">Ni povezano</span>',
    unreachable:     '<span style="color:#dc2626;font-size:0.85rem">⚠ Evolution API nedosegljiv</span>',
    lid_unsupported: '<span style="color:#d97706;font-size:0.85rem">⚠ @lid JID — nadgradite Evolution API</span>',
  };
  return map[state] || '';
}
```

- [ ] **Step 2: Add auto-sync toast**

In `renderSettings`, right after the `[manager, configInfo] = await Promise.all(...)` destructuring, add:

```js
  if (configInfo.wa_synced) {
    toast('Številka WhatsApp bota je bila samodejno posodobljena.');
  }
```

- [ ] **Step 3: Replace the phone field HTML in `renderSettings`**

Find this block (approximate lines 1237–1263):
```js
      <div class="field" style="margin-top:0.75rem">
        <label>Mobilna številka za BelPro</label>
        <input id="s-ngo-wa-phone" type="tel" value="${esc(manager.ngo_whatsapp_phone || '')}" maxlength="30" placeholder="+38640...">
        <div class="form-hint">Telefonska številka, ki je povezana z WhatsApp botom (Evolution API).</div>
      </div>
      <div style="margin-top:0.5rem">
        <a id="s-evo-api-link" href="${esc(configInfo.evolution_api_admin_url)}" target="_blank" rel="noopener noreferrer"
           class="btn btn-secondary btn-sm">Odpri nastavitve povezave telefonske številke ↗</a>
      </div>
```

Replace with:

```js
      <div class="field" style="margin-top:0.75rem">
        <label>Mobilna številka za BelPro</label>
        <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
          <input id="s-ngo-wa-phone" type="tel"
            value="${esc(configInfo.wa_phone ? '+' + configInfo.wa_phone : (manager.ngo_whatsapp_phone ? '+' + manager.ngo_whatsapp_phone : ''))}"
            maxlength="30" placeholder="+38640..."
            ${(configInfo.wa_state === 'open' || configInfo.wa_state === 'connecting') ? 'readonly' : ''}>
          ${_waBadge(configInfo.wa_state)}
        </div>
        ${(configInfo.wa_state === 'open' || configInfo.wa_state === 'connecting')
          ? '<div class="form-hint">Številko upravljate prek Evolution API — spremenite jo tam in nato osvežite to stran.</div>'
          : '<div class="form-hint">Telefonska številka, ki je povezana z WhatsApp botom (Evolution API).</div>'}
        ${!configInfo.wa_env_write_ok
          ? '<div class="form-error" style="margin-top:0.25rem">Opozorilo: posodobitve datoteke .env ni bilo mogoče zapisati — preverite dovoljenja datoteke.</div>'
          : ''}
      </div>
      <div style="margin-top:0.5rem">
        <a id="s-evo-api-link" href="${esc(configInfo.evolution_api_admin_url)}" target="_blank" rel="noopener noreferrer"
           class="btn btn-secondary btn-sm">Odpri nastavitve Evolution API ↗</a>
      </div>
```

- [ ] **Step 4: Verify the `s-ngo-save` handler payload line**

Find the `ngo_whatsapp_phone` line in the `s-ngo-save` click handler. It should read:

```js
      ngo_whatsapp_phone: $('s-ngo-wa-phone').value.trim() || null,
```

No change needed — the backend normalizes whatever value arrives.

- [ ] **Step 5: Manual verification checklist**

Open the dashboard at `http://localhost:80`, go to Settings, and verify:

- [ ] **Connected state** (`wa_state: "open"`): phone field shows `+38640...` and is read-only (cursor shows not-allowed or text cursor without edit); green "✓ Povezano" badge visible; hint says to use Evolution API to change; Evolution API link button present
- [ ] **Disconnected state** (`wa_state: "close"`): phone field is editable; grey "Ni povezano" badge; hint is generic
- [ ] **Unreachable state** (`wa_state: "unreachable"`): red badge; field is editable
- [ ] **Auto-sync toast**: if `wa_synced` was true on load, toast "Številka WhatsApp bota je bila samodejno posodobljena." appears
- [ ] **Manual save with formatting**: type `+386 40 999 888` in editable state, save → reload → field shows `+38640999888` (normalized, with display prefix)
- [ ] **Evolution API link**: clicking "Odpri nastavitve Evolution API ↗" opens the Evolution API admin panel in a new tab

- [ ] **Step 6: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: settings UI — WhatsApp phone display, connection badges, read-only when connected, auto-sync toast"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|------------|------|
| Single source of truth hierarchy (.env → DB → Evolution API) | Tasks 5, 6 |
| Evolution API authoritative when `open` (auto-sync) | Task 6 |
| DB seeded from `.env` on first boot (null guard) | Task 5 |
| Number normalization — WhatsApp-native digits, no `+` in DB | Tasks 2, 3, 7 |
| `.env` updated on auto-sync | Task 6 |
| `.env` updated on manual save | Task 7 |
| `.env` write failure: UI warning + server log | Tasks 3, 6, 8 |
| UI: read-only field when `open` or `connecting` | Task 8 |
| UI: badge per connection state (5 states) | Task 8 |
| UI: toast on auto-sync | Task 8 |
| `@lid` JID: log warning, return `lid_unsupported` state, show message | Tasks 4, 8 |
| httpx dependency added | Task 1 |
| `AUTHENTICATION_API_KEY` exposed to `api` container | Task 1 |
| `.env` file mounted into container for writing | Task 1 |

### Pre-flight checks before Task 6

1. **Fixture names** — Tests reference `client`, `auth_headers`, `db_session`. Verify these match exactly in `api/tests/conftest.py` before running Task 6 tests. Rename references if needed.
2. **`pytest-asyncio` mode** — If `asyncio_mode = "auto"` is not set in pytest config, all `@pytest.mark.asyncio` decorators in this plan are required (they are included). If it IS set to `auto`, the decorators are harmless extras.
3. **`fetchInstances` response shape** — Run the verification command in Task 4 to confirm the actual JSON structure matches the implementation. If `status` vs `state` or the `instance` nesting differs, adjust `EvolutionClient.get_connected_phone` accordingly.
4. **`NGO_WHATSAPP_PHONE` in `.env`** — Task 1 adds it. If `.env` is not writable from inside the container after the volume mount, `write_env_key` returns `False` and logs a warning — the rest of the feature still works correctly.
