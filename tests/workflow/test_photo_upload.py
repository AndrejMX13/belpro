"""
Direct API tests for POST /api/log-entries/{entry_id}/photos/base64.

These tests bypass n8n and call the FastAPI endpoint directly.
They verify extension validation, base64 decoding, photo_count response,
and 404 behaviour — without needing a real WhatsApp image or Evolution API.

Prerequisites: same as test_volunteer_entry.py (full stack running).
"""

import asyncio
import base64
import uuid

import httpx
import pytest

from tests.workflow.helpers import make_text_payload, post_to_webhook, poll_for_entry

# Any bytes with a valid image extension — EXIF extraction fails gracefully (try/except).
_FAKE_JPEG_B64 = base64.b64encode(b"fake-jpeg-content-for-testing").decode()


@pytest.mark.asyncio
async def test_upload_photo_happy_path(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """Upload a photo directly to the API. Response must be 201 with photo_count=1."""
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    # Create an entry via the n8n webhook so we have a real entry_id.
    entry_text = "Danes sem delal 1 uro razdelitev hrane v Ljubljani"
    await post_to_webhook(n8n_client, make_text_payload(phone, entry_text))
    entry = await poll_for_entry(api_client, volunteer_id)
    entry_id = entry["id"]

    r = await api_client.post(
        f"/api/log-entries/{entry_id}/photos/base64",
        json={"image_base64": _FAKE_JPEG_B64, "filename": "test_photo.jpg"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["log_entry_id"] == entry_id
    assert body["photo_count"] == 1
    assert body["photo_path"].endswith(".jpg")
    assert body["photo_exif_timestamp"] is None  # fake bytes have no EXIF


@pytest.mark.asyncio
async def test_upload_second_photo_increments_count(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """Uploading two photos must yield photo_count=2 on the second response."""
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    entry_text = "Danes sem delal 2 uri razdelitev hrane v Mariboru"
    await post_to_webhook(n8n_client, make_text_payload(phone, entry_text))
    entry = await poll_for_entry(api_client, volunteer_id)
    entry_id = entry["id"]

    payload = {"image_base64": _FAKE_JPEG_B64, "filename": "photo.jpg"}
    r1 = await api_client.post(f"/api/log-entries/{entry_id}/photos/base64", json=payload)
    assert r1.status_code == 201
    assert r1.json()["photo_count"] == 1

    r2 = await api_client.post(f"/api/log-entries/{entry_id}/photos/base64", json=payload)
    assert r2.status_code == 201
    assert r2.json()["photo_count"] == 2


@pytest.mark.asyncio
async def test_upload_photo_bad_extension(
    api_client: httpx.AsyncClient,
    n8n_client: httpx.AsyncClient,
    test_volunteer: dict,
):
    """A filename with a disallowed extension must return 422."""
    phone = test_volunteer["phone"]
    volunteer_id = test_volunteer["id"]

    entry_text = "Danes sem delal 1 uro razdelitev hrane v Celju"
    await post_to_webhook(n8n_client, make_text_payload(phone, entry_text))
    entry = await poll_for_entry(api_client, volunteer_id)
    entry_id = entry["id"]

    r = await api_client.post(
        f"/api/log-entries/{entry_id}/photos/base64",
        json={"image_base64": _FAKE_JPEG_B64, "filename": "document.pdf"},
    )
    assert r.status_code == 422, r.text


@pytest.mark.asyncio
async def test_upload_photo_unknown_entry(
    api_client: httpx.AsyncClient,
):
    """Uploading to a non-existent entry_id must return 404."""
    unknown_id = str(uuid.uuid4())
    r = await api_client.post(
        f"/api/log-entries/{unknown_id}/photos/base64",
        json={"image_base64": _FAKE_JPEG_B64, "filename": "photo.jpg"},
    )
    assert r.status_code == 404, r.text
