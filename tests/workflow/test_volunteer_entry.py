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

import asyncio

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
    assert float(entry["hours"]) == 2.0
    assert "razdelitev hrane" in entry["activity_description"]
    entry_id = entry["id"]

    # Brief pause: the n8n workflow saves phone→entry_id state to static data
    # *after* the DB entry is created. poll_for_entry returns as soon as the DB
    # row appears, which can be before the state write completes. Without this
    # sleep, Turn 2 may arrive while the state is not yet persisted and the
    # confirm branch would find no pending entry for this phone.
    await asyncio.sleep(2)

    # Turn 2: volunteer replies "1" (Potrdi).
    await post_to_webhook(n8n_client, make_response_payload(phone, "confirm"))

    # Workflow confirms the entry and notifies the manager.
    confirmed = await poll_for_entry_status(api_client, entry_id, "pending_manager")
    assert confirmed["id"] == entry_id


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

    # Wait for n8n to persist static state before sending next turn.
    await asyncio.sleep(2)

    # Turn 2: volunteer replies "2" (Popravi / edit).
    await post_to_webhook(n8n_client, make_response_payload(phone, "edit"))

    # Wait for n8n to update mode="editing" in static state.
    await asyncio.sleep(2)

    # Turn 3: volunteer sends the corrected entry (different hours).
    corrected_text = "Danes sem delal 3 uri razdelitev hrane v Mariboru"
    await post_to_webhook(n8n_client, make_text_payload(phone, corrected_text))

    # Workflow deletes the original entry and creates a new one.
    await poll_for_entry_gone(api_client, original_id)
    corrected = await poll_for_entry(api_client, volunteer_id)
    assert corrected["status"] == "pending_volunteer"
    assert float(corrected["hours"]) == 3.0
    corrected_id = corrected["id"]

    # Wait for n8n to persist state for the corrected entry.
    await asyncio.sleep(2)

    # Turn 4: volunteer confirms the corrected entry.
    await post_to_webhook(n8n_client, make_response_payload(phone, "confirm"))
    confirmed = await poll_for_entry_status(api_client, corrected_id, "pending_manager")
    assert confirmed["id"] == corrected_id


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

    # Wait for n8n to persist static state before sending next turn.
    await asyncio.sleep(2)

    # Turn 2: volunteer replies "3" (Prekliči / cancel).
    await post_to_webhook(n8n_client, make_response_payload(phone, "cancel"))

    # Workflow deletes the entry.
    await poll_for_entry_gone(api_client, entry_id)


@pytest.mark.asyncio
async def test_unknown_volunteer_creates_no_entry(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
):
    """
    A message from an unregistered phone must not create any log entry.
    The workflow sends a 'not registered' WA message (untestable without
    Evolution mocking) but the DB effect is fully assertable.
    """
    # A phone guaranteed not to exist as a volunteer.
    unknown_phone = "38640000000"

    r = await api_client.get("/api/log-entries", params={"limit": 1})
    r.raise_for_status()
    count_before = r.json()["total"]

    await post_to_webhook(n8n_client, make_text_payload(unknown_phone, _ENTRY_TEXT))

    # Fixed wait: the workflow has no DB side-effect to poll for,
    # so we wait long enough for the workflow to complete then assert count unchanged.
    await asyncio.sleep(8)

    r = await api_client.get("/api/log-entries", params={"limit": 1})
    r.raise_for_status()
    count_after = r.json()["total"]

    assert count_after == count_before, (
        f"Expected no new entries, but count went from {count_before} to {count_after}"
    )
