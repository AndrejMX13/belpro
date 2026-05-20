# ISS-015 GDPR Consent Document Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a print-ready GDPR Article 13 consent PDF pre-filled with NGO data, downloadable from a new "Dokumenti" dashboard tab, with an optional additional-clauses textarea saved to the manager record.

**Architecture:** New `documents` router and `consent_pdf` service following the WeasyPrint pattern of existing `report_pdf`. One new DB column on `managers`. New `documents.js` frontend tab. Six independent tasks plus one frontend task.

**Tech Stack:** FastAPI, SQLAlchemy 2.x, Alembic, WeasyPrint, vanilla JS

---

## Codebase context (read before any task)

Key files and patterns:

- `api/services/report_pdf.py` — existing WeasyPrint PDF service. Functions `_BASE_CSS`, `_ngo_header_html`, `NGOInfo`, `_esc`, `_generated_line` live here. Task 1 renames two of them to be importable.
- `api/routers/reports.py` — existing router pattern: `APIRouter(prefix=..., tags=[...])`, `StreamingResponse`, `require_manager`, `get_db`.
- `api/routers/managers.py` — `PATCH /managers/me` via `ManagerUpdate` schema, `model_dump(exclude_none=True)` partial-update pattern.
- `api/schemas/manager.py` — `ManagerUpdate` (all optional) and `ManagerResponse` (from_attributes=True).
- `api/models/manager.py` — `Manager` ORM model, single row per deployment.
- `api/main.py` — `app.include_router(...)` with `prefix="/api"`.
- `api/tests/conftest.py` — session-scoped engine runs `alembic upgrade head`; per-test SAVEPOINT isolation; seeds one Manager row. The seeded manager has: first_name="Test", last_name="Manager", phone="+38641000000", email="test@belpro.si", ngo_name="Test NGO d.o.o.", ngo_street="Testna ulica 1", ngo_postal_code="1000", ngo_city="Ljubljana".
- `frontend/js/api.js` — `API` singleton with `downloadRequest()` for PDF downloads.
- `frontend/js/volunteers.js` — contains `route()` function (hash-based router), `renderSettings()`, and global helpers `$()`, `esc()`, `setHtml()`, `toast()`.
- `frontend/index.html` — loads scripts at bottom: api.js, volunteers.js, reports.js, analytics.js.

**Run tests inside the API container:**
```
docker compose exec api pytest tests/ -v
```

**Rebuild API after code changes:**
```
docker compose up -d --build api
```

**Run migrations inside the API container:**
```
docker compose exec api alembic upgrade head
```

---

## File structure

| Action | Path | Responsibility |
|--------|------|----------------|
| Modify | `api/services/report_pdf.py` | Rename `_BASE_CSS`→`BASE_CSS`, `_ngo_header_html`→`ngo_header_html` |
| Modify | `api/tests/test_reports.py` | Update import of renamed symbol |
| Create | `api/db/migrations/versions/011_manager_gdpr_clauses.py` | Add `gdpr_additional_clauses` column |
| Modify | `api/models/manager.py` | Add `gdpr_additional_clauses` field |
| Modify | `api/core/settings.py` | Add `photo_retention_days: int = 730` |
| Modify | `api/schemas/manager.py` | Add `gdpr_additional_clauses` to ManagerUpdate + ManagerResponse |
| Create | `api/services/consent_pdf.py` | `render_consent_pdf(manager, photo_retention_days)` |
| Create | `api/routers/documents.py` | `GET /documents/consent-pdf` |
| Modify | `api/main.py` | Register documents router |
| Create | `api/tests/test_documents.py` | Tests for new endpoint and service |
| Modify | `frontend/index.html` | Add Dokumenti nav item + documents.js script tag |
| Modify | `frontend/js/api.js` | Add `documents.consentPdf()` |
| Modify | `frontend/js/volunteers.js` | Add `#documents` route case |
| Create | `frontend/js/documents.js` | `renderDocuments()` |

---

## Task 1: Rename shared PDF utilities

Make `_BASE_CSS` and `_ngo_header_html` importable by removing their underscore prefix. Update internal call sites in `report_pdf.py` and the import in `test_reports.py`.

**Files:**
- Modify: `api/services/report_pdf.py`
- Modify: `api/tests/test_reports.py`

- [ ] **Step 1: Update the import in test_reports.py first (it will fail until report_pdf.py is changed)**

In `api/tests/test_reports.py`, change line 7:
```python
# Before:
from services.report_pdf import NGOInfo, _ngo_header_html

# After:
from services.report_pdf import NGOInfo, ngo_header_html
```

Update the two test functions that reference `_ngo_header_html` → `ngo_header_html`:

```python
def test_ngo_header_html_without_logo():
    """ngo_header_html must not include an img tag when logo_path is None."""
    ngo = NGOInfo(name="Test NGO", street="Testna 1", postal_code="1000", city="Ljubljana")
    html = ngo_header_html(ngo)
    assert "<img" not in html


def test_ngo_header_html_with_logo():
    """ngo_header_html must include an img tag with data URI src when logo_path is set."""
    ngo = NGOInfo(
        name="Test NGO",
        street="Testna 1",
        postal_code="1000",
        city="Ljubljana",
        logo_path="data:image/png;base64,FAKE",
    )
    html = ngo_header_html(ngo)
    assert "<img" in html
    assert "data:image/png;base64,FAKE" in html
```

- [ ] **Step 2: Run the affected tests to confirm they fail (import error expected)**

```
docker compose exec api pytest tests/test_reports.py::test_ngo_header_html_without_logo tests/test_reports.py::test_ngo_header_html_with_logo -v
```

Expected: FAIL with `ImportError: cannot import name 'ngo_header_html'`

- [ ] **Step 3: Rename `_BASE_CSS` → `BASE_CSS` and `_ngo_header_html` → `ngo_header_html` in report_pdf.py**

In `api/services/report_pdf.py`:

Change the constant definition (line ~16):
```python
# Before:
_BASE_CSS = """

# After:
BASE_CSS = """
```

Change the function definition (line ~61):
```python
# Before:
def _ngo_header_html(ngo: NGOInfo) -> str:

# After:
def ngo_header_html(ngo: NGOInfo) -> str:
```

Update the two internal call sites within `report_pdf.py` that reference these names.

In `render_volunteer_pdf` (around line 107):
```python
# Before:
    header = _ngo_header_html(ngo) if ngo else ""
# After:
    header = ngo_header_html(ngo) if ngo else ""
```

In `render_summary_pdf` (around line 154):
```python
# Before:
    header = _ngo_header_html(ngo) if ngo else ""
# After:
    header = ngo_header_html(ngo) if ngo else ""
```

In the `<head>` style blocks in both render functions, change `{_BASE_CSS}` → `{BASE_CSS}`:

In `render_volunteer_pdf` (the doc string, around line 111):
```python
<head><meta charset="utf-8"><style>{BASE_CSS}</style></head>
```

In `render_summary_pdf` (around line 158):
```python
<head><meta charset="utf-8"><style>{BASE_CSS}</style></head>
```

- [ ] **Step 4: Run the affected tests to confirm they pass**

```
docker compose exec api pytest tests/test_reports.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Run the full test suite to confirm nothing broke**

```
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS

- [ ] **Step 6: Commit**

```
git add api/services/report_pdf.py api/tests/test_reports.py
git commit -m "refactor: make BASE_CSS and ngo_header_html importable from report_pdf"
```

---

## Task 2: DB migration and Manager model field

Add `gdpr_additional_clauses TEXT NULL` to the `managers` table via Alembic, and add the mapped column to the ORM model.

**Files:**
- Create: `api/db/migrations/versions/011_manager_gdpr_clauses.py`
- Modify: `api/models/manager.py`

- [ ] **Step 1: Create the Alembic migration file**

Create `api/db/migrations/versions/011_manager_gdpr_clauses.py`:

```python
"""Add gdpr_additional_clauses to managers.

Revision ID: 011
Revises: 010
Create Date: 2026-05-20
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add gdpr_additional_clauses nullable text column to managers."""
    op.add_column("managers", sa.Column("gdpr_additional_clauses", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove gdpr_additional_clauses column from managers."""
    op.drop_column("managers", "gdpr_additional_clauses")
```

- [ ] **Step 2: Add the mapped column to the Manager ORM model**

In `api/models/manager.py`, add after the `evolution_api_admin_url` field (around line 45):

```python
    gdpr_additional_clauses: Mapped[str | None] = mapped_column(Text(), nullable=True)
```

The full import block already includes `Text` — no import change needed.

- [ ] **Step 3: Apply the migration to the development database**

```
docker compose exec api alembic upgrade head
```

Expected output ends with: `Running upgrade 010 -> 011, Add gdpr_additional_clauses to managers.`

- [ ] **Step 4: Run the full test suite (conftest runs migrations automatically)**

```
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS (the new nullable column doesn't break existing tests)

- [ ] **Step 5: Commit**

```
git add api/db/migrations/versions/011_manager_gdpr_clauses.py api/models/manager.py
git commit -m "feat(iss-015): add gdpr_additional_clauses column to managers"
```

---

## Task 3: Settings and schema update

Add `photo_retention_days` to the app settings and `gdpr_additional_clauses` to the manager Pydantic schemas.

**Files:**
- Modify: `api/core/settings.py`
- Modify: `api/schemas/manager.py`

- [ ] **Step 1: Add `photo_retention_days` to Settings**

In `api/core/settings.py`, add after the `max_photos_per_entry` field (around line 44):

```python
    # ── Data retention ────────────────────────────────────────────────────────
    photo_retention_days: int = 730
```

- [ ] **Step 2: Add `gdpr_additional_clauses` to ManagerUpdate**

In `api/schemas/manager.py`, add to the `ManagerUpdate` class after `evolution_api_admin_url` (around line 77):

```python
    gdpr_additional_clauses: str | None = None
```

- [ ] **Step 3: Add `gdpr_additional_clauses` to ManagerResponse**

In `api/schemas/manager.py`, add to the `ManagerResponse` class after `evolution_api_admin_url` (around line 112):

```python
    gdpr_additional_clauses: str | None = None
```

- [ ] **Step 4: Run the full test suite**

```
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS

- [ ] **Step 5: Commit**

```
git add api/core/settings.py api/schemas/manager.py
git commit -m "feat(iss-015): add photo_retention_days setting and gdpr_additional_clauses schema fields"
```

---

## Task 4: Write tests (TDD — write before implementing)

Write all tests for the new consent PDF service and endpoint. They must fail at this point.

**Files:**
- Create: `api/tests/test_documents.py`

- [ ] **Step 1: Create the test file**

Create `api/tests/test_documents.py`:

```python
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
```

- [ ] **Step 2: Run the tests to confirm they fail**

```
docker compose exec api pytest tests/test_documents.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'services.consent_pdf'` and `404` for the endpoint

- [ ] **Step 3: Commit the test file**

```
git add api/tests/test_documents.py
git commit -m "test(iss-015): add failing tests for consent_pdf service and documents endpoint"
```

---

## Task 5: Consent PDF service

Implement `render_consent_pdf()` in a new `api/services/consent_pdf.py`.

**Files:**
- Create: `api/services/consent_pdf.py`

- [ ] **Step 1: Create the service file**

Create `api/services/consent_pdf.py`:

```python
"""GDPR Article 13 consent notice PDF generation."""
from __future__ import annotations

import html as _html
from datetime import datetime

from weasyprint import HTML

from services.logo import logo_src
from services.report_pdf import BASE_CSS, NGOInfo, ngo_header_html

_CONSENT_CSS = """
section { margin-bottom: 1em; }
section h2 { font-size: 10pt; font-weight: bold; margin-bottom: 0.3em; color: #1e3a8a; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.15em; }
section p, section ul { margin: 0.2em 0 0; font-size: 9.5pt; line-height: 1.5; }
section ul { padding-left: 1.5em; }
.signature-block { margin-top: 2em; border-top: 2px solid #1e40af; padding-top: 1em; }
.signature-block h2 { font-size: 10pt; font-weight: bold; color: #1e3a8a; margin-bottom: 0.5em; }
.sig-row { display: flex; justify-content: space-between; margin-top: 2em; font-size: 9.5pt; }
.sig-row span { border-top: 1px solid #1a1a2e; padding-top: 0.25em; min-width: 10em; }
"""


def _esc(s: str | None) -> str:
    return _html.escape(s or "")


def _now_str() -> str:
    n = datetime.now()
    return f"{n.day}. {n.month}. {n.year} {n.strftime('%H:%M')}"


def render_consent_pdf(manager: object, photo_retention_days: int) -> bytes:
    """Render the GDPR Article 13 consent notice PDF and return raw bytes.

    `manager` must expose: ngo_name, ngo_street, ngo_postal_code, ngo_city,
    phone, email, ngo_davcna, gdpr_additional_clauses.
    """
    ngo = NGOInfo(
        name=manager.ngo_name,
        street=manager.ngo_street,
        postal_code=manager.ngo_postal_code,
        city=manager.ngo_city,
        phone=getattr(manager, "phone", None),
        email=getattr(manager, "email", None),
        ngo_davcna=getattr(manager, "ngo_davcna", None),
        logo_path=logo_src(),
    )
    header = ngo_header_html(ngo)

    clauses_html = ""
    raw_clauses = getattr(manager, "gdpr_additional_clauses", None)
    if raw_clauses and raw_clauses.strip():
        clauses_html = f"""
  <section>
    <h2>Dodatne določbe</h2>
    <p>{_esc(raw_clauses.strip())}</p>
  </section>"""

    doc = f"""<!DOCTYPE html>
<html lang="sl">
<head><meta charset="utf-8"><style>{BASE_CSS}{_CONSENT_CSS}</style></head>
<body>
  {header}
  <h1>Obvestilo posameznikom po 13. členu Splošne uredbe o varstvu podatkov (GDPR) glede obdelave osebnih podatkov</h1>
  <p class="meta"><strong>Zbirka:</strong> Evidenca prostovoljskega dela</p>

  <section>
    <h2>Upravljavec zbirke osebnih podatkov</h2>
    <p>{_esc(manager.ngo_name)}<br>
    {_esc(manager.ngo_street)}, {_esc(manager.ngo_postal_code)} {_esc(manager.ngo_city)}<br>
    {f"Davčna št.: {_esc(manager.ngo_davcna)}<br>" if getattr(manager, "ngo_davcna", None) else ""}
    {f"Tel: {_esc(manager.phone)}<br>" if getattr(manager, "phone", None) else ""}
    {f"E-pošta: {_esc(manager.email)}" if getattr(manager, "email", None) else ""}</p>
  </section>

  <section>
    <h2>Pooblaščena oseba za varstvo osebnih podatkov (DPO)</h2>
    <p>Ni imenovana.</p>
  </section>

  <section>
    <h2>Namen obdelave osebnih podatkov</h2>
    <p>Vodenje evidence prostovoljskega dela v skladu z Zakonom o prostovoljstvu (Ur. l. RS, št. 10/11 in nasl.).
    Zbiramo naslednje osebne podatke: EMŠO, telefonska številka, glasovni posnetki, fotografije.</p>
  </section>

  <section>
    <h2>Pravna podlaga za obdelavo osebnih podatkov</h2>
    <ul>
      <li>EMŠO in evidenca ur: člen 6(1)(c) Splošne uredbe — zakonska obveznost (Zakon o prostovoljstvu)</li>
      <li>Fotografije in glasovni posnetki: člen 6(1)(a) Splošne uredbe — privolitev posameznika</li>
    </ul>
  </section>

  <section>
    <h2>Uporabniki osebnih podatkov</h2>
    <p>Center za socialno delo (CSD) za namen mesečnega poročanja o prostovoljskem delu.
    Podatki se ne posredujejo v tretje države ali mednarodne organizacije.</p>
  </section>

  <section>
    <h2>Obdobje hrambe osebnih podatkov</h2>
    <ul>
      <li>Fotografije in glasovni posnetki: {photo_retention_days} dni od nastanka zapisa</li>
      <li>Evidence ur in aktivnosti: 10 let (zakonska arhivska obveznost)</li>
    </ul>
  </section>

  <section>
    <h2>Pravice posameznika</h2>
    <p>Imate pravico zahtevati dostop do vaših osebnih podatkov, njihov popravek ali izbris, omejitev obdelave,
    pravico do ugovora obdelavi ter pravico do prenosljivosti podatkov. Pravice uveljavljate z zahtevo,
    poslano na zgoraj navedene kontakte upravljavca.</p>
  </section>

  <section>
    <h2>Pravica do preklica privolitve</h2>
    <p>Privolitev za obdelavo fotografij in glasovnih posnetkov lahko kadar koli prekličete, ne da bi to vplivalo
    na zakonitost obdelave, ki se je na podlagi privolitve izvajala do njenega preklica.</p>
  </section>

  <section>
    <h2>Pravica do vložitve pritožbe pri nadzornem organu</h2>
    <p>Pritožbo lahko podate Informacijskemu pooblaščencu: Dunajska 22, 1000 Ljubljana,
    gp.ip@ip-rs.si, 01 230 97 30, www.ip-rs.si.</p>
  </section>

  <section>
    <h2>Avtomatizirano odločanje in profiliranje</h2>
    <p>Ne izvajamo avtomatiziranega sprejemanja odločitev niti profiliranja.</p>
  </section>
{clauses_html}
  <div class="signature-block">
    <h2>Izjava in podpis prostovoljca</h2>
    <p>S podpisom potrjujem, da sem bil/-a seznanjen/-a z vsebino tega obvestila in dajem privolitev
    za obdelavo fotografij in glasovnih posnetkov za namen vodenja evidence prostovoljskega dela.</p>
    <div class="sig-row">
      <span>Ime in priimek: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span>Datum: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    </div>
    <div class="sig-row">
      <span>Podpis: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    </div>
  </div>

  <p class="footer">Generirano: {_now_str()}</p>
</body>
</html>"""

    return HTML(string=doc).write_pdf()
```

- [ ] **Step 2: Run the unit tests**

```
docker compose exec api pytest tests/test_documents.py::test_render_consent_pdf_returns_bytes tests/test_documents.py::test_render_consent_pdf_with_additional_clauses tests/test_documents.py::test_render_consent_pdf_empty_clauses_treated_as_none -v
```

Expected: All 3 PASS

- [ ] **Step 3: Commit**

```
git add api/services/consent_pdf.py
git commit -m "feat(iss-015): add consent_pdf service with render_consent_pdf"
```

---

## Task 6: Documents router and main.py registration

Create `api/routers/documents.py` with the `GET /documents/consent-pdf` endpoint, then register it in `main.py`.

**Files:**
- Create: `api/routers/documents.py`
- Modify: `api/main.py`

- [ ] **Step 1: Create the router**

Create `api/routers/documents.py`:

```python
"""Documents router — downloadable compliance documents."""
from __future__ import annotations

import io
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.manager import Manager
from services.consent_pdf import render_consent_pdf

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/consent-pdf", response_model=None, dependencies=[Depends(require_manager)])
async def download_consent_pdf(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StreamingResponse:
    """Generate and stream the GDPR Article 13 consent notice PDF."""
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
```

- [ ] **Step 2: Register the router in main.py**

In `api/main.py`, add the import after the other router imports (around line 22):

```python
from routers.documents import router as documents_router
```

Add the include_router call after the existing ones (around line 67):

```python
app.include_router(documents_router, prefix="/api")
```

- [ ] **Step 3: Rebuild and run all tests**

```
docker compose up -d --build api
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS including all tests in test_documents.py

- [ ] **Step 4: Commit**

```
git add api/routers/documents.py api/main.py
git commit -m "feat(iss-015): add documents router with GET /documents/consent-pdf"
```

---

## Task 7: Frontend — Dokumenti tab

Add the "Dokumenti" navigation tab, create `documents.js`, wire up routing and the API client.

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/js/api.js`
- Modify: `frontend/js/volunteers.js`
- Create: `frontend/js/documents.js`

- [ ] **Step 1: Add the Dokumenti nav item to index.html**

In `frontend/index.html`, add the new nav item after the Nastavitve item (after line 59). Insert:

```html
      <a href="#documents" class="nav-item" data-page="documents">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10,9 9,9 8,9"/></svg>
        Dokumenti
      </a>
```

- [ ] **Step 2: Add the documents.js script tag to index.html**

In `frontend/index.html`, add after the analytics.js script tag (line 92):

```html
<script src="/js/documents.js"></script>
```

- [ ] **Step 3: Add the documents API method to api.js**

In `frontend/js/api.js`, add a `documents` section after the `logo` section (before the closing `};` of the return object, around line 204):

```js
    documents: {
      consentPdf: () => downloadRequest('/documents/consent-pdf'),
    },
```

- [ ] **Step 4: Add the `#documents` route case to volunteers.js**

In `frontend/js/volunteers.js`, in the `route()` function, add the `#documents` case. Find the block ending with `} else { renderList(); }` (around line 217) and insert before it:

```js
  } else if (hash === '#documents') {
    renderDocuments();
```

So the block reads:
```js
  } else if (hash === '#documents') {
    renderDocuments();
  } else {
    renderList();
  }
```

- [ ] **Step 5: Create documents.js**

Create `frontend/js/documents.js`:

```js
'use strict';

async function renderDocuments() {
  $('topbar-title').textContent = 'Dokumenti';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="documents"]')?.classList.add('active');

  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  let manager;
  try {
    manager = await API.managers.me();
  } catch (err) {
    setHtml($('main-content'), `<p class="form-error" style="margin:2rem">Napaka: ${esc(err.message)}</p>`);
    return;
  }

  const card = 'background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-bottom:1.5rem';
  const h2   = 'font-size:1rem;font-weight:600;margin:0 0 1.25rem';

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Dokumenti</h1>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Soglasje za obdelavo osebnih podatkov (GDPR)</h2>
      <p style="margin-bottom:1.25rem;color:var(--text-secondary,#6b7280);font-size:0.9rem">
        Prenesite obrazec, ki ga natisnete in izročite prostovoljcu v podpis pred začetkom sodelovanja.
        Obrazec je predizpolnjen s podatki vaše organizacije.
      </p>
      <div class="field">
        <label for="gdpr-clauses">Dodatne določbe <span style="font-weight:400;color:var(--text-secondary,#6b7280)">(neobvezno)</span></label>
        <textarea id="gdpr-clauses" rows="5" style="width:100%;box-sizing:border-box"
          placeholder="Sem vpišite morebitne dodatne določbe, ki bodo dodane na konec dokumenta. Polje pustite prazno, če dodatnih določb ni.">${esc(manager.gdpr_additional_clauses || '')}</textarea>
        <div class="form-hint">Besedilo bo dodano na konec dokumenta pod naslovom &ldquo;Dodatne določbe&rdquo;.</div>
      </div>
      <div id="gdpr-status" style="min-height:1.2rem;font-size:0.85rem;margin-bottom:0.5rem"></div>
      <div class="form-actions">
        <button class="btn btn-primary btn-sm" id="gdpr-download-btn">Prenesi PDF</button>
      </div>
    </div>
  `);

  const clausesEl = document.getElementById('gdpr-clauses');
  const statusEl  = document.getElementById('gdpr-status');
  const downloadBtn = document.getElementById('gdpr-download-btn');

  clausesEl.addEventListener('blur', async () => {
    statusEl.style.color = '';
    statusEl.textContent = 'Shranjevanje…';
    try {
      await API.managers.update({ gdpr_additional_clauses: clausesEl.value.trim() });
      statusEl.style.color = 'var(--success,#16a34a)';
      statusEl.textContent = 'Shranjeno.';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
    } catch (err) {
      statusEl.style.color = 'var(--danger,#dc2626)';
      statusEl.textContent = 'Napaka pri shranjevanju: ' + esc(err.message);
    }
  });

  downloadBtn.addEventListener('click', async () => {
    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Priprava…';
    try {
      const { blob, filename } = await API.documents.consentPdf();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      toast('Napaka pri generiranju PDF: ' + esc(err.message));
    } finally {
      downloadBtn.disabled = false;
      downloadBtn.textContent = 'Prenesi PDF';
    }
  });
}
```

- [ ] **Step 6: Rebuild API and verify the API tests still pass**

```
docker compose up -d --build api
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS

- [ ] **Step 7: Manually verify the UI**

Open the dashboard in a browser. Confirm:
1. "Dokumenti" tab appears in the sidebar nav
2. Clicking it loads the card with the textarea and download button
3. Typing in the textarea and clicking away saves without error ("Shranjeno." appears briefly)
4. Clicking "Prenesi PDF" downloads `soglasje_gdpr.pdf`
5. Opening the PDF shows the NGO header (with logo if uploaded), all required sections, and the signature block
6. If additional clauses were saved, they appear in the PDF under "Dodatne določbe"
7. Refreshing the Dokumenti page re-loads the saved textarea content

- [ ] **Step 8: Commit**

```
git add frontend/index.html frontend/js/api.js frontend/js/volunteers.js frontend/js/documents.js
git commit -m "feat(iss-015): add Dokumenti tab with GDPR consent PDF download"
```

---

## Final check

- [ ] Run the full test suite one last time:

```
docker compose exec api pytest tests/ -v
```

Expected: All tests PASS with no failures or warnings.

- [ ] Push to remote:

```
git push central main
```
