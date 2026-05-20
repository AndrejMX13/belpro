"""Tests for the /documents router and consent_pdf service."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from httpx import AsyncClient


# ── Unit tests for render_consent_pdf ────────────────────────────────────────

def test_render_consent_pdf_returns_bytes():
    """render_consent_pdf returns non-empty bytes for a minimal manager."""
    from services.consent_pdf import render_consent_pdf

    manager = SimpleNamespace(
        ngo_name="Test NGO",
        ngo_street="Testna ulica 1",
        ngo_postal_code="1000",
        ngo_city="Ljubljana",
        phone="+38641000000",
        email="test@belpro.si",
        ngo_davcna=None,
        gdpr_additional_clauses=None,
    )
    pdf = render_consent_pdf(manager, photo_retention_days=730)
    assert isinstance(pdf, bytes)
    assert len(pdf) > 1000


def test_render_consent_pdf_with_additional_clauses():
    """render_consent_pdf produces bytes when additional clauses are set."""
    from services.consent_pdf import render_consent_pdf

    manager = SimpleNamespace(
        ngo_name="Test NGO",
        ngo_street="Testna ulica 1",
        ngo_postal_code="1000",
        ngo_city="Ljubljana",
        phone="+38641000000",
        email="test@belpro.si",
        ngo_davcna="12345670",
        gdpr_additional_clauses="Posebna klavzula za ta primer.",
    )
    pdf = render_consent_pdf(manager, photo_retention_days=365)
    assert isinstance(pdf, bytes)
    assert len(pdf) > 1000


def test_render_consent_pdf_empty_clauses_treated_as_none():
    """render_consent_pdf handles empty string clauses without error."""
    from services.consent_pdf import render_consent_pdf

    manager = SimpleNamespace(
        ngo_name="Test NGO",
        ngo_street="Testna 1",
        ngo_postal_code="1000",
        ngo_city="Ljubljana",
        phone=None,
        email=None,
        ngo_davcna=None,
        gdpr_additional_clauses="",
    )
    pdf = render_consent_pdf(manager, photo_retention_days=730)
    assert isinstance(pdf, bytes)
    assert len(pdf) > 1000


# ── Integration tests for GET /api/documents/consent-pdf ─────────────────────

async def test_consent_pdf_returns_pdf(client: AsyncClient, auth: dict) -> None:
    """Authenticated request returns a PDF response."""
    r = await client.get("/api/documents/consent-pdf", headers=auth)
    assert r.status_code == 200
    assert "application/pdf" in r.headers["content-type"]
    assert "attachment" in r.headers.get("content-disposition", "")
    assert "soglasje_gdpr.pdf" in r.headers.get("content-disposition", "")


async def test_consent_pdf_requires_auth(client: AsyncClient) -> None:
    """Unauthenticated request is rejected."""
    r = await client.get("/api/documents/consent-pdf")
    assert r.status_code == 401


# ── Integration test: PATCH /managers/me saves gdpr_additional_clauses ───────

async def test_patch_manager_saves_gdpr_clauses(client: AsyncClient, auth: dict) -> None:
    """PATCH /managers/me accepts and persists gdpr_additional_clauses."""
    payload = {"gdpr_additional_clauses": "Testna določba."}
    r = await client.patch("/api/managers/me", headers=auth, json=payload)
    assert r.status_code == 200
    assert r.json()["gdpr_additional_clauses"] == "Testna določba."


async def test_patch_manager_clears_gdpr_clauses(client: AsyncClient, auth: dict) -> None:
    """PATCH /managers/me with empty string clears gdpr_additional_clauses.

    Note: sending null is excluded by exclude_none=True and leaves the field unchanged.
    The frontend always sends the string value (even when empty) to allow clearing.
    """
    await client.patch("/api/managers/me", headers=auth,
                       json={"gdpr_additional_clauses": "Testna določba."})
    r = await client.patch("/api/managers/me", headers=auth,
                           json={"gdpr_additional_clauses": ""})
    assert r.status_code == 200
    assert r.json()["gdpr_additional_clauses"] == ""
