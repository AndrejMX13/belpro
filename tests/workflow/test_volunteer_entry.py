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
