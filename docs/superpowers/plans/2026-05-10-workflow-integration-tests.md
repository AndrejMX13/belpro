# Volunteer Entry Workflow Integration Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an integration test suite that drives the `volunteer_entry` n8n workflow end-to-end by posting real WhatsApp payloads to the n8n webhook, then asserting DB state via the FastAPI API.

**Architecture:** Tests live in `tests/workflow/` at the project root — separate from `api/tests/` (which use in-process ASGITransport). Each test creates a real volunteer with a unique phone via the FastAPI API, simulates a full multi-turn conversation by POSTing to the n8n webhook, polls the FastAPI API for state changes, and deletes the volunteer on teardown (cascading to entries). Evolution sends real WhatsApp messages to whatever phone is in the test payload — use a dedicated test phone that you own. The n8n workflow must be **active** (not in test/listen mode) for the production webhook URL to accept calls.

**Tech Stack:** Python 3.14 (host), `httpx`, `pytest`, `pytest-asyncio`, `python-dotenv`. Full Docker stack must be up (`docker compose up -d`).

---

## Key Facts (read before writing any code)

| Detail | Value |
|--------|-------|
| n8n webhook URL | `POST http://localhost:5678/webhook/volunteer-message` |
| FastAPI external URL | `http://localhost:8100` |
| Manager auth | HTTP Basic — user `manager`, password from `.env` `MANAGER_PASSWORD` |
| Phone format in DB | Bare E.164 digits, no `+` — `_normalise_phone` strips it (e.g. `+38641999001` → `38641999001`) |
| Phone in WhatsApp JID | Same bare digits — extracted by `split('@')[0]` from `38641999001@s.whatsapp.net` |
| Volunteer lookup match | `ILIKE '%{search_q}%'` — bare-digit phone in JID finds bare-digit phone in DB ✓ |
| Confirm response | Text message with body `"1"` or `"potrdi"` |
| Edit response | Text message with body `"2"` or `"popravi"` |
| Cancel response | Text message with body `"3"` or text starting with `"prekli"` |
| Good test text | `"Danes sem delal 2 uri razdelitev hrane v Mariboru"` → hours=2.0, date=today, location=Mariboru |
| Entry initial status | `pending_volunteer` (set by POST /api/log-entries in the workflow) |
| Entry after confirm | `pending_manager` |
| Manager phone (seeded) | Read from `GET /api/managers/me` — never use this as a test volunteer phone |

---

## File Map

| File | Action | Purpose |
|------|---------|---------|
| `pyproject.toml` | Create (project root) | pytest asyncio_mode config for workflow tests |
| `tests/__init__.py` | Create | package marker |
| `tests/workflow/__init__.py` | Create | package marker |
| `tests/workflow/conftest.py` | Create | fixtures: HTTP clients, volunteer factory, connectivity check |
| `tests/workflow/helpers.py` | Create | WhatsApp payload builders, polling utilities |
| `tests/workflow/test_volunteer_entry.py` | Create | four integration test scenarios |

---

## Task 1: Host dependencies and directory structure

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/workflow/__init__.py`
- Create: `pyproject.toml` (project root)

- [ ] **Step 1: Install host-side test dependencies**

Run from project root (PowerShell):
```powershell
python -m pip install httpx pytest pytest-asyncio python-dotenv
```

Expected: packages install without error. If already installed, `Requirement already satisfied` is fine.

- [ ] **Step 2: Create `tests/__init__.py` and `tests/workflow/__init__.py`**

Both files are empty. Create them:
```powershell
New-Item -ItemType File -Force tests\__init__.py
New-Item -ItemType Directory -Force tests\workflow
New-Item -ItemType File -Force tests\workflow\__init__.py
```

- [ ] **Step 3: Create `pyproject.toml` at project root**

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

- [ ] **Step 4: Verify pytest finds the new directory**

```powershell
python -m pytest tests/workflow/ --collect-only
```

Expected: `no tests ran` — no errors about collection, just empty results.

- [ ] **Step 5: Commit**

```powershell
git add pyproject.toml tests/
git commit -m "chore: scaffold workflow integration test directory"
```

---

## Task 2: `conftest.py` — fixtures

**Files:**
- Create: `tests/workflow/conftest.py`

- [ ] **Step 1: Write `conftest.py`**

```python
import asyncio
import base64
import itertools
import os
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
import httpx

load_dotenv(Path(__file__).parent.parent.parent / ".env", override=False)

_API_BASE = "http://localhost:8100"
_N8N_BASE = "http://localhost:5678"
_WEBHOOK_PATH = "/webhook/volunteer-message"

_phone_seq = itertools.count(1)


def _manager_password() -> str:
    pw = os.getenv("MANAGER_PASSWORD", "")
    if not pw:
        raise RuntimeError("MANAGER_PASSWORD not set — is .env loaded?")
    return pw


def _auth_header() -> dict[str, str]:
    creds = base64.b64encode(f"manager:{_manager_password()}".encode()).decode()
    return {"Authorization": f"Basic {creds}"}


@pytest_asyncio.fixture(scope="session")
async def api_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable."""
    async with httpx.AsyncClient(
        base_url=_API_BASE, headers=_auth_header(), timeout=30.0
    ) as client:
        try:
            r = await client.get("/api/health")
            r.raise_for_status()
        except Exception as exc:
            pytest.skip(f"FastAPI not reachable at {_API_BASE}: {exc}")
        yield client


@pytest_asyncio.fixture(scope="session")
async def n8n_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Session-scoped AsyncClient against n8n. Skips all tests if unreachable."""
    async with httpx.AsyncClient(base_url=_N8N_BASE, timeout=30.0) as client:
        try:
            r = await client.get("/healthz")
            # n8n /healthz returns 200 when running
            if r.status_code >= 500:
                raise RuntimeError(f"n8n returned {r.status_code}")
        except Exception as exc:
            pytest.skip(f"n8n not reachable at {_N8N_BASE}: {exc}")
        yield client


@pytest_asyncio.fixture
async def test_volunteer(api_client: httpx.AsyncClient) -> AsyncGenerator[dict, None]:
    """
    Creates a volunteer with a unique phone, yields the volunteer dict,
    deletes it (and cascade-deletes entries) on teardown.
    """
    seq = next(_phone_seq)
    # Range 38640900001–38640999999 — unlikely to match the real manager phone.
    phone = f"38640900{seq:03d}"

    payload = {
        "first_name": "Test",
        "last_name": f"Prostovoljec{seq}",
        "street": "Testna ulica 1",
        "postal_code": "1000",
        "city": "Ljubljana",
        "emso": f"{seq:013d}",
        "phone": phone,
        "report_whatsapp": True,
        "report_email": False,
    }
    r = await api_client.post("/api/volunteers", json=payload)
    assert r.status_code == 201, f"Failed to create test volunteer: {r.text}"
    volunteer = r.json()

    yield volunteer

    # Teardown: delete volunteer (cascades to log entries).
    await api_client.delete(f"/api/volunteers/{volunteer['id']}")
```

- [ ] **Step 2: Verify conftest loads without error**

```powershell
python -m pytest tests/workflow/ --collect-only
```

Expected: collection succeeds (0 tests), no import errors.

- [ ] **Step 3: Commit**

```powershell
git add tests/workflow/conftest.py
git commit -m "test(workflow): add conftest with HTTP client fixtures"
```

---

## Task 3: `helpers.py` — payload builders and polling

**Files:**
- Create: `tests/workflow/helpers.py`

- [ ] **Step 1: Write `helpers.py`**

```python
import asyncio
import time
import uuid

import httpx

_WEBHOOK_PATH = "/webhook/volunteer-message"


# ── WhatsApp payload builders ─────────────────────────────────────────────────

def make_text_payload(phone: str, text: str) -> dict:
    """Build a WhatsApp text-message webhook body for the given bare-digit phone."""
    jid = f"{phone}@s.whatsapp.net"
    return {
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": jid,
                "fromMe": False,
                "id": f"test-{uuid.uuid4().hex[:8]}",
            },
            "remoteJidAlt": jid,
            "messageType": "conversation",
            "message": {
                "conversation": text,
            },
        },
    }


def make_response_payload(phone: str, response_type: str) -> dict:
    """
    Build a volunteer response payload. response_type must be one of:
    'confirm' (sends text "1"), 'edit' (sends "2"), 'cancel' (sends "3").
    """
    text_map = {"confirm": "1", "edit": "2", "cancel": "3"}
    if response_type not in text_map:
        raise ValueError(f"response_type must be confirm/edit/cancel, got {response_type!r}")
    return make_text_payload(phone, text_map[response_type])


# ── Webhook sender ────────────────────────────────────────────────────────────

async def post_to_webhook(n8n_client: httpx.AsyncClient, payload: dict) -> None:
    """POST a WhatsApp event to the n8n webhook. Asserts 200."""
    r = await n8n_client.post(_WEBHOOK_PATH, json=payload)
    assert r.status_code == 200, f"Webhook rejected payload: {r.status_code} {r.text}"


# ── Polling utilities ─────────────────────────────────────────────────────────

async def poll_for_entry(
    api_client: httpx.AsyncClient,
    volunteer_id: str,
    *,
    timeout: float = 20.0,
    interval: float = 0.5,
) -> dict:
    """
    Poll GET /api/log-entries until at least one entry for volunteer_id appears.
    Returns the first matching entry dict.
    Raises TimeoutError if nothing appears within timeout seconds.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        r = await api_client.get("/api/log-entries", params={"limit": 50})
        r.raise_for_status()
        items = r.json().get("items", [])
        matches = [e for e in items if e["volunteer_id"] == volunteer_id]
        if matches:
            return matches[0]
        await asyncio.sleep(interval)
    raise TimeoutError(
        f"No log entry appeared for volunteer {volunteer_id} within {timeout}s"
    )


async def poll_for_entry_status(
    api_client: httpx.AsyncClient,
    entry_id: str,
    expected_status: str,
    *,
    timeout: float = 20.0,
    interval: float = 0.5,
) -> dict:
    """
    Poll GET /api/log-entries/{entry_id} until its status matches expected_status.
    Returns the entry dict. Raises TimeoutError if status never changes.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        r = await api_client.get(f"/api/log-entries/{entry_id}")
        if r.status_code == 200:
            entry = r.json()
            if entry["status"] == expected_status:
                return entry
        await asyncio.sleep(interval)
    raise TimeoutError(
        f"Entry {entry_id} never reached status {expected_status!r} within {timeout}s"
    )


async def poll_for_entry_gone(
    api_client: httpx.AsyncClient,
    entry_id: str,
    *,
    timeout: float = 20.0,
    interval: float = 0.5,
) -> None:
    """
    Poll until GET /api/log-entries/{entry_id} returns 404.
    Raises TimeoutError if entry persists beyond timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        r = await api_client.get(f"/api/log-entries/{entry_id}")
        if r.status_code == 404:
            return
        await asyncio.sleep(interval)
    raise TimeoutError(f"Entry {entry_id} still exists after {timeout}s")
```

- [ ] **Step 2: Verify helpers import cleanly**

```powershell
python -m pytest tests/workflow/ --collect-only
```

Expected: 0 tests collected, no import errors.

- [ ] **Step 3: Commit**

```powershell
git add tests/workflow/helpers.py
git commit -m "test(workflow): add WhatsApp payload builders and polling helpers"
```

---

## Task 4: Happy path — text entry then confirm

**Files:**
- Create: `tests/workflow/test_volunteer_entry.py` (initial version with one test)

- [ ] **Step 1: Write the first test**

```python
"""
Workflow integration tests for volunteer_entry n8n workflow.

Prerequisites:
  - docker compose up -d  (full stack running)
  - n8n volunteer_entry workflow is ACTIVE (not in test/listen mode)
  - MANAGER_PASSWORD is set in .env
  - A real WhatsApp number is reachable via the Evolution instance for
    the phone numbers used in test payloads (or accept that messages go
    to a test device).

Run: python -m pytest tests/workflow/ -v
"""

import pytest
import httpx

from tests.workflow.helpers import (
    make_text_payload,
    make_response_payload,
    post_to_webhook,
    poll_for_entry,
    poll_for_entry_status,
    poll_for_entry_gone,
)

# A text message the Text Extract node can parse.
# Yields: hours=2.0, date=today, location="Mariboru", activity contains "razdelitev hrane"
_ENTRY_TEXT = "Danes sem delal 2 uri razdelitev hrane v Mariboru"


@pytest.mark.asyncio
async def test_happy_path_text_confirm(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """Volunteer sends a text entry and confirms it. Entry must reach pending_manager."""
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    # Turn 1: volunteer sends a work-diary text message.
    await post_to_webhook(n8n_client, make_text_payload(phone, _ENTRY_TEXT))

    # Workflow creates the entry and sends a confirmation request via WA.
    entry = await poll_for_entry(api_client, volunteer_id)
    assert entry["status"] == "pending_volunteer"
    assert entry["hours"] == 2.0
    assert "razdelitev hrane" in entry["activity_description"]
    entry_id = entry["id"]

    # Turn 2: volunteer replies "1" (Potrdi).
    await post_to_webhook(n8n_client, make_response_payload(phone, "confirm"))

    # Workflow confirms the entry and notifies the manager.
    confirmed = await poll_for_entry_status(api_client, entry_id, "pending_manager")
    assert confirmed["id"] == entry_id
```

- [ ] **Step 2: Run the test (stack must be up and workflow active)**

```powershell
python -m pytest tests/workflow/test_volunteer_entry.py::test_happy_path_text_confirm -v
```

Expected: PASSED. If FAILED with TimeoutError, check n8n execution logs at `http://localhost:5678` to see where the workflow stalled.

- [ ] **Step 3: Commit**

```powershell
git add tests/workflow/test_volunteer_entry.py
git commit -m "test(workflow): add happy-path text-confirm integration test"
```

---

## Task 5: Edit path — text, edit, new text, confirm

**Files:**
- Modify: `tests/workflow/test_volunteer_entry.py`

- [ ] **Step 1: Add the edit-path test**

Append to `test_volunteer_entry.py`:

```python
@pytest.mark.asyncio
async def test_edit_path(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """
    Volunteer sends entry, chooses edit, sends corrected entry, then confirms.
    Original entry is deleted; corrected entry reaches pending_manager.
    """
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    # Turn 1: send initial entry.
    await post_to_webhook(n8n_client, make_text_payload(phone, _ENTRY_TEXT))
    original = await poll_for_entry(api_client, volunteer_id)
    assert original["status"] == "pending_volunteer"
    original_id = original["id"]

    # Turn 2: volunteer replies "2" (Popravi / edit).
    await post_to_webhook(n8n_client, make_response_payload(phone, "edit"))

    # Turn 3: volunteer sends the corrected entry (different hours).
    corrected_text = "Danes sem delal 3 uri razdelitev hrane v Mariboru"
    await post_to_webhook(n8n_client, make_text_payload(phone, corrected_text))

    # Workflow deletes the original entry and creates a new one.
    await poll_for_entry_gone(api_client, original_id)
    corrected = await poll_for_entry(api_client, volunteer_id)
    assert corrected["status"] == "pending_volunteer"
    assert corrected["hours"] == 3.0
    corrected_id = corrected["id"]

    # Turn 4: volunteer confirms the corrected entry.
    await post_to_webhook(n8n_client, make_response_payload(phone, "confirm"))
    confirmed = await poll_for_entry_status(api_client, corrected_id, "pending_manager")
    assert confirmed["id"] == corrected_id
```

- [ ] **Step 2: Run the edit-path test**

```powershell
python -m pytest tests/workflow/test_volunteer_entry.py::test_edit_path -v
```

Expected: PASSED.

- [ ] **Step 3: Commit**

```powershell
git add tests/workflow/test_volunteer_entry.py
git commit -m "test(workflow): add edit-path integration test"
```

---

## Task 6: Cancel path — text then cancel

**Files:**
- Modify: `tests/workflow/test_volunteer_entry.py`

- [ ] **Step 1: Add the cancel-path test**

Append to `test_volunteer_entry.py`:

```python
@pytest.mark.asyncio
async def test_cancel_path(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """
    Volunteer sends entry and cancels it. Entry must be deleted from the DB.
    """
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    # Turn 1: send entry.
    await post_to_webhook(n8n_client, make_text_payload(phone, _ENTRY_TEXT))
    entry = await poll_for_entry(api_client, volunteer_id)
    assert entry["status"] == "pending_volunteer"
    entry_id = entry["id"]

    # Turn 2: volunteer replies "3" (Prekliči / cancel).
    await post_to_webhook(n8n_client, make_response_payload(phone, "cancel"))

    # Workflow deletes the entry.
    await poll_for_entry_gone(api_client, entry_id)
```

- [ ] **Step 2: Run the cancel-path test**

```powershell
python -m pytest tests/workflow/test_volunteer_entry.py::test_cancel_path -v
```

Expected: PASSED.

- [ ] **Step 3: Commit**

```powershell
git add tests/workflow/test_volunteer_entry.py
git commit -m "test(workflow): add cancel-path integration test"
```

---

## Task 7: Unknown volunteer test

**Files:**
- Modify: `tests/workflow/test_volunteer_entry.py`

- [ ] **Step 1: Add the unknown-volunteer test**

Append to `test_volunteer_entry.py`:

```python
@pytest.mark.asyncio
async def test_unknown_volunteer_creates_no_entry(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
):
    """
    A message from an unregistered phone must not create any log entry.
    The workflow sends a 'not registered' WA message (untestable here without
    mocking Evolution) but the DB effect is fully assertable.
    """
    # A phone that is guaranteed not to exist as a volunteer.
    unknown_phone = "38640000000"

    r = await api_client.get("/api/log-entries", params={"limit": 1})
    r.raise_for_status()
    count_before = r.json()["total"]

    await post_to_webhook(n8n_client, make_text_payload(unknown_phone, _ENTRY_TEXT))

    # Give the workflow time to finish — it has no DB side-effect to poll for,
    # so we wait a fixed interval then assert the count is unchanged.
    import asyncio
    await asyncio.sleep(8)

    r = await api_client.get("/api/log-entries", params={"limit": 1})
    r.raise_for_status()
    count_after = r.json()["total"]

    assert count_after == count_before, (
        f"Expected no new entries, but count went from {count_before} to {count_after}"
    )
```

- [ ] **Step 2: Run the unknown-volunteer test**

```powershell
python -m pytest tests/workflow/test_volunteer_entry.py::test_unknown_volunteer_creates_no_entry -v
```

Expected: PASSED.

- [ ] **Step 3: Run the full suite**

```powershell
python -m pytest tests/workflow/ -v
```

Expected: 4 tests, all PASSED.

- [ ] **Step 4: Commit**

```powershell
git add tests/workflow/test_volunteer_entry.py
git commit -m "test(workflow): add unknown-volunteer no-entry-created test"
```

---

## Self-Review

**Spec coverage:**
- ✅ Happy path (text + confirm) — Task 4
- ✅ Edit path (text + edit + corrected text + confirm) — Task 5
- ✅ Cancel path (text + cancel) — Task 6
- ✅ Unknown volunteer — Task 7
- ⚠️ Audio message path (Whisper transcription) — explicitly out of scope; requires a real audio file and adds Whisper latency. Test separately when working on transcription.
- ⚠️ Manager notification side-effect — workflow sends WA to manager after confirm; this is an Evolution-side effect, not assertable without real Evolution verification. Accepted gap.

**Placeholder scan:** None found.

**Type consistency:** All helpers use `str` for IDs and phone numbers throughout. `entry["hours"]` is compared with `float` literals (`2.0`, `3.0`) — verify the API returns hours as a number not a string; adjust to `Decimal` or `str` comparison if needed at test-run time.

**Known assumptions to verify at run time:**
1. `GET /api/log-entries` supports `?limit=N` and returns `{"total": int, "items": [...]}` — confirm from existing test_log_entries.py.
2. `GET /api/log-entries/{id}` returns 404 when not found — confirm from existing tests.
3. Volunteer DELETE cascades to log entries — confirm from model or test observation.
4. n8n health endpoint is `/healthz` — if 404, try `/` or adjust the conftest connectivity check.
