# Auto Monthly Report Delivery — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add automatic monthly report delivery triggered by ops crond, with delivery day and period configurable from Sistemske nastavitve.

**Architecture:** Two new settings (`report_auto_day`, `report_auto_period`) stored in the existing `AppSetting` key-value table and exposed through the existing admin API and UI. When settings change, the API notifies a lightweight `ThreadingHTTPServer` running inside ops. Ops regenerates its crontab and reloads crond. On the configured day, the cron entry calls a new ops script that calls the existing `POST /api/reports/send-monthly` endpoint.

**Tech Stack:** FastAPI + SQLAlchemy (API), Python `http.server.ThreadingHTTPServer` (ops notification server), `httpx` (API→ops notification), `psycopg2` (ops DB read on startup), BusyBox crond on Alpine.

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `api/core/settings.py` | Modify | Add `ops_url` env var |
| `api/services/app_settings.py` | Modify | Add `report_auto_day`, `report_auto_period` properties |
| `api/schemas/admin.py` | Modify | Add new fields to response + update schemas |
| `api/routers/admin.py` | Modify | Return new fields; notify ops after PATCH |
| `api/tests/test_admin.py` | Create | Tests for GET/PATCH admin settings |
| `frontend/js/admin.js` | Modify | Add day input + period select to Sistemske nastavitve |
| `ops/scripts/monthly_report_send.py` | Create | Called by crond; resolves period and calls API |
| `ops/scripts/ops_server.py` | Create | ThreadingHTTPServer; reconfigures crontab on notification |
| `ops/crontab` | Modify | Add default monthly report cron line |
| `ops/entrypoint.sh` | Modify | Start crond in background, ops_server.py in foreground |
| `docker-compose.yml` | Modify | Add `OPS_URL` to api env; add ops healthcheck |

---

### Task 1: AppSettings — new properties and env var

**Files:**
- Modify: `api/core/settings.py`
- Modify: `api/services/app_settings.py`
- Test: `api/tests/test_admin.py` (create)

- [ ] **Step 1: Write the failing tests**

Create `api/tests/test_admin.py`:

```python
from httpx import AsyncClient


async def test_get_settings_returns_report_defaults(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/admin/settings", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["report_auto_day"] == 28
    assert data["report_auto_period"] == "current"
```

- [ ] **Step 2: Run to confirm it fails**

```
docker compose exec api pytest tests/test_admin.py -v
```

Expected: FAIL — `KeyError: 'report_auto_day'` (field not in response yet).

- [ ] **Step 3: Add `ops_url` to `api/core/settings.py`**

In the `# ── Internal service URLs ─────` section, after `authentication_api_key`:

```python
ops_url: str = "http://ops:9000"
```

- [ ] **Step 4: Add two properties to `api/services/app_settings.py`**

After the `session_duration_hours` property:

```python
@property
def report_auto_day(self) -> int:
    """Day of month (1–28) on which monthly reports are auto-sent."""
    return self._int("report_auto_day", 28)

@property
def report_auto_period(self) -> str:
    """Reporting period: 'current' (this month) or 'previous' (last month)."""
    return self._str("report_auto_period", "current") or "current"
```

- [ ] **Step 5: Run tests — they still fail (schema not updated yet)**

```
docker compose exec api pytest tests/test_admin.py -v
```

Expected: FAIL — `KeyError: 'report_auto_day'` (property exists but schema doesn't expose it).

- [ ] **Step 6: Commit**

```bash
git add api/core/settings.py api/services/app_settings.py api/tests/test_admin.py
git commit -m "feat: add report_auto_day and report_auto_period AppSettings properties"
```

---

### Task 2: Admin schemas — new fields

**Files:**
- Modify: `api/schemas/admin.py`

- [ ] **Step 1: Replace the full content of `api/schemas/admin.py`**

```python
"""Pydantic schemas for the admin settings endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AdminSettingsResponse(BaseModel):
    """Current values of all runtime-tunable settings."""

    max_photos_per_entry: int
    photo_retention_days: int
    session_duration_hours: int
    report_auto_day: int
    report_auto_period: str


class AdminSettingsUpdate(BaseModel):
    """Partial update for runtime-tunable settings. Only provided fields are written."""

    max_photos_per_entry: int | None = Field(None, ge=1)
    photo_retention_days: int | None = Field(None, ge=1)
    session_duration_hours: int | None = Field(None, ge=1)
    report_auto_day: int | None = Field(None, ge=1, le=28)
    report_auto_period: str | None = Field(None, pattern="^(current|previous)$")
```

- [ ] **Step 2: Commit**

```bash
git add api/schemas/admin.py
git commit -m "feat: add report_auto_day and report_auto_period to admin schemas"
```

---

### Task 3: Admin router — return new fields, save them, notify ops

**Files:**
- Modify: `api/routers/admin.py`
- Test: `api/tests/test_admin.py`

- [ ] **Step 1: Add tests for PATCH saving new fields and ops notification**

Append to `api/tests/test_admin.py`:

```python
from unittest.mock import AsyncMock, MagicMock, patch


async def test_patch_settings_saves_report_fields(client: AsyncClient, auth: dict) -> None:
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=AsyncMock(
            post=AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))
        ))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 5, "report_auto_period": "previous"},
            headers=auth,
        )

    assert r.status_code == 200
    data = r.json()
    assert data["report_auto_day"] == 5
    assert data["report_auto_period"] == "previous"


async def test_patch_settings_notifies_ops(client: AsyncClient, auth: dict) -> None:
    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=MagicMock(raise_for_status=MagicMock()))

    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_http)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 1},
            headers=auth,
        )

    assert r.status_code == 200
    mock_http.post.assert_called_once()
    call_args = mock_http.post.call_args
    assert "/reconfigure" in call_args[0][0]
    assert call_args[1]["json"]["report_auto_day"] == 1


async def test_patch_settings_ops_failure_does_not_break_save(
    client: AsyncClient, auth: dict
) -> None:
    with patch("routers.admin.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(side_effect=Exception("ops unreachable"))
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        r = await client.patch(
            "/api/admin/settings",
            json={"report_auto_day": 10},
            headers=auth,
        )

    assert r.status_code == 200
    assert r.json()["report_auto_day"] == 10
```

- [ ] **Step 2: Run to confirm they fail**

```
docker compose exec api pytest tests/test_admin.py -v
```

Expected: all three new tests FAIL.

- [ ] **Step 3: Replace `api/routers/admin.py` with the updated version**

```python
"""Admin router — runtime-tunable settings management."""
from __future__ import annotations

import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import Settings, get_settings
from db.session import get_db
from models.app_setting import AppSetting
from models.error_log import ErrorLog
from schemas.admin import AdminSettingsResponse, AdminSettingsUpdate
from services.app_settings import AppSettings

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


async def _notify_ops(db: AsyncSession, env: Settings, s: AppSettings) -> None:
    """POST /reconfigure to ops. Logs and persists error on failure; never raises."""
    payload = {
        "report_auto_day": s.report_auto_day,
        "report_auto_period": s.report_auto_period,
    }
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(
                f"{env.ops_url}/reconfigure",
                json=payload,
                headers={"X-Internal-Key": env.api_secret_key},
            )
            r.raise_for_status()
    except Exception as exc:
        logger.warning("ops notification failed: %s", exc)
        db.add(ErrorLog(
            service="api",
            operation="notify_ops_reconfigure",
            message="Ops service notification failed",
            detail=str(exc),
        ))
        await db.commit()


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
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
    )


@router.patch(
    "/settings",
    response_model=AdminSettingsResponse,
    dependencies=[Depends(require_manager)],
)
async def update_admin_settings(
    body: AdminSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    env: Annotated[Settings, Depends(get_settings)],
) -> AdminSettingsResponse:
    """Update one or more runtime-tunable settings. Returns updated state."""
    raw_updates = body.model_dump(exclude_none=True)
    # Infer value_type from Python type so string settings are stored correctly.
    updates = {
        k: (str(v), "str" if isinstance(v, str) else "int")
        for k, v in raw_updates.items()
    }

    for name, (value, vtype) in updates.items():
        row = (
            await db.execute(select(AppSetting).where(AppSetting.name == name))
        ).scalar_one_or_none()
        if row is None:
            db.add(AppSetting(name=name, value_type=vtype, value=value))
        else:
            row.value = value

    if updates:
        await db.commit()

    rows = (await db.execute(select(AppSetting))).scalars().all()
    s = AppSettings(env, {r.name: r.value for r in rows if r.value is not None})

    if updates:
        await _notify_ops(db, env, s)

    return AdminSettingsResponse(
        max_photos_per_entry=s.max_photos_per_entry,
        photo_retention_days=s.photo_retention_days,
        session_duration_hours=s.session_duration_hours,
        report_auto_day=s.report_auto_day,
        report_auto_period=s.report_auto_period,
    )
```

- [ ] **Step 4: Run all tests**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS (210+ tests).

- [ ] **Step 5: Commit**

```bash
git add api/routers/admin.py api/tests/test_admin.py
git commit -m "feat: admin settings — report_auto_day/period fields + ops notification"
```

---

### Task 4: Frontend — Sistemske nastavitve UI

**Files:**
- Modify: `frontend/js/admin.js`

Context: `admin.js` renders a settings card with three number inputs. Settings are loaded via `API.admin.getSettings()` and saved via `API.admin.updateSettings(patch)`. Only changed fields are included in the patch. No build step — changes are picked up on hard refresh (Ctrl+Shift+R).

- [ ] **Step 1: Add the two new form fields to the HTML template in `renderAdmin()`**

In `admin.js`, after the `a-session-duration` field block and before the `admin-settings-error` div:

```javascript
        <div class="field">
          <label for="a-report-day">Dan samodejnega pošiljanja poročil (1–28)</label>
          <input id="a-report-day" type="number" min="1" max="28" style="width:100%;max-width:12rem" step="1" />
        </div>
        <div class="field">
          <label for="a-report-period">Obdobje poročila</label>
          <select id="a-report-period" style="width:100%;max-width:16rem">
            <option value="current">Tekoči mesec</option>
            <option value="previous">Prejšnji mesec</option>
          </select>
        </div>
```

- [ ] **Step 2: Load the new fields after fetching settings**

After `$('a-session-duration').value = data.session_duration_hours;`:

```javascript
    $('a-report-day').value    = data.report_auto_day;
    $('a-report-period').value = data.report_auto_period;
```

- [ ] **Step 3: Include the new fields in the `current` snapshot for the save handler**

Replace the `current` object inside the save handler click listener:

```javascript
    const current = {
      max_photos_per_entry:   parseInt($('a-max-photos').value, 10),
      photo_retention_days:   parseInt($('a-photo-retention').value, 10),
      session_duration_hours: parseInt($('a-session-duration').value, 10),
      report_auto_day:        parseInt($('a-report-day').value, 10),
      report_auto_period:     $('a-report-period').value,
    };
```

- [ ] **Step 4: Update the validation loop to skip `report_auto_period` (it's a string, not an int)**

Replace the validation block:

```javascript
    for (const [key, val] of Object.entries(current)) {
      if (key === 'report_auto_period') continue;
      if (!Number.isInteger(val) || val < 1) {
        errEl.textContent = 'Vse vrednosti morajo biti cela števila, večja ali enaka 1.';
        errEl.style.display = 'block';
        return;
      }
    }
```

- [ ] **Step 5: Verify manually**

Hard-refresh the dashboard (Ctrl+Shift+R). Open Administracija. Confirm the two new fields appear with values 28 and "Tekoči mesec". Change day to 5, save — confirm toast "Nastavitve so bile shranjene." Reload — confirm day shows 5.

- [ ] **Step 6: Commit**

```bash
git add frontend/js/admin.js
git commit -m "feat: add report_auto_day and report_auto_period to Sistemske nastavitve UI"
```

---

### Task 5: monthly_report_send.py

**Files:**
- Create: `ops/scripts/monthly_report_send.py`

Context: This script is called by crond. It receives `--period current` or `--period previous`, resolves the target year/month from `datetime.now(timezone.utc)`, and calls `POST /api/reports/send-monthly`. The API already does all the delivery logic. Errors are reported via `POST /api/errors` (the established ops error pattern from `photo_cleanup.py`).

- [ ] **Step 1: Create `ops/scripts/monthly_report_send.py`**

```python
#!/usr/bin/env python3
"""Auto monthly report sender — called by crond on the configured day.

Usage: monthly_report_send.py --period {current,previous}
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={
                "service": "ops",
                "operation": "monthly_report_send",
                "message": message,
                "detail": detail,
            },
            timeout=10,
        )
    except Exception:
        pass


def resolve_period(period: str) -> tuple[int, int]:
    """Return (year, month) for the given period label.

    'current'  → today's year and month.
    'previous' → the previous calendar month (handles Jan → Dec year rollover).
    """
    today = datetime.now(timezone.utc)
    if period == "previous":
        ref = today.replace(day=1) - timedelta(days=1)
        return ref.year, ref.month
    return today.year, today.month


def main() -> None:
    """Resolve target month and call the send-monthly API endpoint."""
    parser = argparse.ArgumentParser(description="Send monthly reports via BelPro API.")
    parser.add_argument("--period", choices=["current", "previous"], required=True)
    args = parser.parse_args()

    year, month = resolve_period(args.period)
    print(
        f"[monthly_report_send] Sending reports for {year}-{month:02d}"
        f" (period={args.period})"
    )

    try:
        r = requests.post(
            f"{API_URL}/api/reports/send-monthly",
            params={"year": year, "month": month},
            headers={"X-Internal-Key": API_SECRET_KEY},
            timeout=300,
        )
        r.raise_for_status()
        data = r.json()
        sent_email = len(data.get("sent_via_email", []))
        sent_wa = len(data.get("sent_via_whatsapp", []))
        errors = data.get("errors", [])
        print(
            f"[monthly_report_send] Done: {sent_email} email, {sent_wa} WhatsApp"
            f", {len(errors)} errors"
        )
        if errors:
            for e in errors:
                print(f"[monthly_report_send] ERROR: {e}")
    except Exception as exc:
        report_error("Monthly report send failed", str(exc))
        print(f"[monthly_report_send] FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the period resolution logic manually**

```bash
# In Git Bash, from the project root:
python -c "
from datetime import datetime, timedelta, timezone
# Simulate January (year boundary)
today = datetime(2026, 1, 15, tzinfo=timezone.utc)
ref = today.replace(day=1) - timedelta(days=1)
print('previous from Jan:', ref.year, ref.month)  # expect 2025 12
# Simulate normal month
today2 = datetime(2026, 5, 28, tzinfo=timezone.utc)
ref2 = today2.replace(day=1) - timedelta(days=1)
print('previous from May:', ref2.year, ref2.month)  # expect 2026 4
"
```

Expected output:
```
previous from Jan: 2025 12
previous from May: 2026 4
```

- [ ] **Step 3: Commit**

```bash
git add ops/scripts/monthly_report_send.py
git commit -m "feat: add monthly_report_send.py ops script"
```

---

### Task 6: ops_server.py

**Files:**
- Create: `ops/scripts/ops_server.py`

Context: `ThreadingHTTPServer` gives each incoming HTTP request its own thread automatically — the main loop keeps accepting while request threads do their work. The server uses `psycopg2` (already in `ops/requirements.txt`) to read settings from the DB on startup, so it can sync the crontab before accepting requests. `requests` (also in `ops/requirements.txt`) is used for error reporting. No new dependencies.

- [ ] **Step 1: Create `ops/scripts/ops_server.py`**

```python
#!/usr/bin/env python3
"""Ops HTTP notification server.

Listens on port 9000 for reconfiguration notifications from the API.
ThreadingHTTPServer handles each request in its own thread; the main
loop never blocks.

Endpoints:
    GET  /health      — Docker healthcheck
    POST /reconfigure — Regenerate crontab and reload crond
"""
from __future__ import annotations

import json
import logging
import os
import signal
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg2
import requests

API_URL = os.environ.get("API_URL", "http://api:8000")
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
PORT = int(os.environ.get("OPS_SERVER_PORT", "9000"))
CRONTAB_PATH = Path("/etc/crontabs/ops")

logging.basicConfig(
    level=logging.INFO,
    format="[ops_server] %(levelname)s %(message)s",
    stream=__import__("sys").stdout,
)
logger = logging.getLogger(__name__)

# Static crontab lines + one dynamic monthly-report line.
CRONTAB_TEMPLATE = (
    "# m h dom mon dow command\n"
    "0 2 * * * /app/scripts/backup.sh >> /proc/1/fd/1 2>&1\n"
    "0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1\n"
    "0 7 {day} * * /app/scripts/monthly_report_send.py --period {period}"
    " >> /proc/1/fd/1 2>&1\n"
)


def _dsn(url: str) -> str:
    """Convert asyncpg DATABASE_URL to a psycopg2-compatible DSN."""
    return url.replace("postgresql+asyncpg://", "postgresql://")


def report_error(message: str, detail: str = "") -> None:
    """POST failure to the API error log. Best-effort — never raises."""
    try:
        requests.post(
            f"{API_URL}/api/errors",
            headers={"X-Internal-Key": API_SECRET_KEY, "Content-Type": "application/json"},
            json={
                "service": "ops",
                "operation": "ops_server",
                "message": message,
                "detail": detail,
            },
            timeout=10,
        )
    except Exception:
        pass


def reload_crond() -> None:
    """Send SIGHUP to crond so it reloads the crontab file."""
    result = subprocess.run(["pidof", "crond"], capture_output=True, text=True)
    pid_str = result.stdout.strip()
    if not pid_str:
        raise RuntimeError("crond process not found via pidof")
    os.kill(int(pid_str), signal.SIGHUP)


def write_crontab(day: int, period: str) -> None:
    """Write a new crontab to CRONTAB_PATH and reload crond."""
    content = CRONTAB_TEMPLATE.format(day=day, period=period)
    CRONTAB_PATH.write_text(content)
    reload_crond()
    logger.info("Crontab updated: day=%d period=%s", day, period)


def fetch_settings_from_db() -> dict[str, str]:
    """Read report_auto_day and report_auto_period from the settings table.

    Returns an empty dict on any failure (caller falls back to defaults).
    Retries 3 times with 2-second gaps to handle slow DB startup.
    """
    for attempt in range(3):
        try:
            conn = psycopg2.connect(_dsn(DATABASE_URL))
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT name, value FROM settings"
                    " WHERE name IN ('report_auto_day', 'report_auto_period')"
                )
                rows = {name: value for name, value in cur.fetchall()}
            conn.close()
            return rows
        except Exception as exc:
            logger.warning("Settings fetch attempt %d/3 failed: %s", attempt + 1, exc)
            if attempt < 2:
                time.sleep(2)
    return {}


class _Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the ops notification server."""

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        logger.info(fmt, *args)

    def _send(self, status: int, body: bytes = b"", content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, b'{"status":"ok"}')
        else:
            self._send(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/reconfigure":
            self._send(404)
            return

        if self.headers.get("X-Internal-Key", "") != API_SECRET_KEY:
            self._send(403)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")

        # Respond immediately — this thread continues working after the response.
        self._send(202)

        day = int(payload.get("report_auto_day", 28))
        period = str(payload.get("report_auto_period", "current"))
        try:
            write_crontab(day, period)
        except Exception as exc:
            logger.error("Crontab update failed: %s", exc)
            report_error("Crontab update failed", str(exc))


def main() -> None:
    """Sync crontab with DB settings, then start the notification server."""
    logger.info("Fetching settings from DB for startup crontab sync...")
    rows = fetch_settings_from_db()
    if rows:
        day = int(rows.get("report_auto_day", 28))
        period = rows.get("report_auto_period", "current") or "current"
        try:
            write_crontab(day, period)
            logger.info("Startup crontab sync complete (day=%d, period=%s).", day, period)
        except Exception as exc:
            logger.warning("Startup crontab sync failed; baked-in default remains: %s", exc)
    else:
        logger.warning("No settings in DB; baked-in default crontab remains.")

    server = ThreadingHTTPServer(("0.0.0.0", PORT), _Handler)
    logger.info("Ops server listening on port %d.", PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add ops/scripts/ops_server.py
git commit -m "feat: add ops_server.py notification server"
```

---

### Task 7: ops crontab and entrypoint

**Files:**
- Modify: `ops/crontab`
- Modify: `ops/entrypoint.sh`

- [ ] **Step 1: Add the monthly report line to `ops/crontab`**

Replace the full content of `ops/crontab`:

```
# m h dom mon dow command
0 2 * * * /app/scripts/backup.sh >> /proc/1/fd/1 2>&1
0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1
0 7 28 * * /app/scripts/monthly_report_send.py --period current >> /proc/1/fd/1 2>&1
```

This baked-in file reflects the defaults (day=28, period=current). `ops_server.py` overwrites it at startup if the DB has different values.

- [ ] **Step 2: Update `ops/entrypoint.sh`**

Replace the full content:

```bash
#!/bin/bash
# Start crond in the background (daemonises itself).
crond -l 2
# Start the ops notification server in the foreground (becomes the main process).
exec python3 /app/scripts/ops_server.py
```

- [ ] **Step 3: Commit**

```bash
git add ops/crontab ops/entrypoint.sh
git commit -m "feat: add monthly report cron entry and update ops entrypoint"
```

---

### Task 8: docker-compose and integration test

**Files:**
- Modify: `docker-compose.yml`

- [ ] **Step 1: Add `OPS_URL` to the api service environment**

In `docker-compose.yml`, under the `api:` service `environment:` block, after `NGO_WHATSAPP_PHONE`:

```yaml
      OPS_URL: http://ops:9000
```

- [ ] **Step 2: Add a healthcheck to the ops service**

In the `ops:` service block, add after the `volumes:` section:

```yaml
    healthcheck:
      test: ["CMD-SHELL", "wget -qO /dev/null http://localhost:9000/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
```

- [ ] **Step 3: Rebuild and restart both services**

```
docker compose up -d --build api ops
```

- [ ] **Step 4: Verify ops server started correctly**

```
docker compose logs ops --tail=20
```

Expected output includes:
```
[ops_server] INFO Fetching settings from DB for startup crontab sync...
[ops_server] INFO Startup crontab sync complete (day=28, period=current).
[ops_server] INFO Ops server listening on port 9000.
```

- [ ] **Step 5: Verify the health endpoint**

```
docker compose exec api curl -s http://ops:9000/health
```

Expected: `{"status":"ok"}`

- [ ] **Step 6: Verify the reconfigure endpoint is called when settings change**

Open the dashboard → Administracija → change "Dan samodejnega pošiljanja" to 5 → Shrani.

Then check ops logs:
```
docker compose logs ops --tail=10
```

Expected: `[ops_server] INFO Crontab updated: day=5 period=current`

Verify the crontab inside the container:
```
docker compose exec ops cat /etc/crontabs/ops
```

Expected:
```
# m h dom mon dow command
0 2 * * * /app/scripts/backup.sh >> /proc/1/fd/1 2>&1
0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1
0 7 5 * * /app/scripts/monthly_report_send.py --period current >> /proc/1/fd/1 2>&1
```

- [ ] **Step 7: Run the full API test suite to confirm no regressions**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 8: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: wire OPS_URL and ops healthcheck in docker-compose"
```
