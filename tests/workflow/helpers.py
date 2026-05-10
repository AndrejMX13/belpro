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
