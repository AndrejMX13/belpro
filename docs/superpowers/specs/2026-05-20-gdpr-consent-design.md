# ISS-015 · GDPR Consent Document — Design Spec

> **For agentic workers:** Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Generate a print-ready GDPR Article 13 consent PDF pre-filled with NGO data, downloadable from a new "Dokumenti" dashboard tab.

**Architecture:** New `documents` router and `consent_pdf` service, following the exact same WeasyPrint pattern as monthly reports. One new DB column on `managers`. One new frontend tab with a single card.

**Tech Stack:** FastAPI, SQLAlchemy, WeasyPrint, vanilla JS

---

## Data Model

One new nullable column on the `managers` table:

```sql
ALTER TABLE managers ADD COLUMN gdpr_additional_clauses TEXT;
```

Added via a new Alembic migration. No other schema changes.

**Note:** `gdpr_additional_clauses` is a pragmatic stopgap. ISS-026 tracks a future `settings` table that may absorb this field.

---

## Settings

One new field in `api/core/settings.py`:

```python
photo_retention_days: int = 730
```

Default 730 days (2 years — covers standard Slovenian NGO record-keeping obligations). This is ISS-007's env var, added here early so the consent PDF can reference it without waiting for ISS-007.

---

## PDF Content

File: `api/services/consent_pdf.py`  
Function: `render_consent_pdf(manager: Manager, photo_retention_days: int) -> bytes`

Reuses `ngo_header_html()` and `BASE_CSS` from `api/services/report_pdf.py`. As part of this task, rename `_ngo_header_html` → `ngo_header_html` and `_BASE_CSS` → `BASE_CSS` in `report_pdf.py` (remove the underscore prefix so they can be imported). Update all internal call sites in `report_pdf.py` accordingly.

Document sections, in order:

1. **NGO header** — logo, name, address, tax number, phone, email (via `_ngo_header_html`)
2. **Title** — "Obvestilo posameznikom po 13. členu Splošne uredbe o varstvu podatkov (GDPR) glede obdelave osebnih podatkov"
3. **Zbirka osebnih podatkov** — "Evidenca prostovoljskega dela"
4. **Upravljavec** — NGO name, address, phone, email (from manager record)
5. **DPO** — "Ni imenovana." (fixed; small NGOs are not required to appoint one)
6. **Namen obdelave** — vodenje evidence prostovoljskega dela v skladu z Zakonom o prostovoljstvu (Ur. l. RS, št. 10/11 in nasl.)
7. **Pravna podlaga**:
   - EMŠO in evidenca ur: člen 6(1)(c) GDPR — zakonska obveznost (Zakon o prostovoljstvu)
   - Fotografije in glasovni posnetki: člen 6(1)(a) GDPR — privolitev posameznika
8. **Uporabniki osebnih podatkov** — Center za socialno delo (CSD), za namen mesečnega poročanja; podatki se ne posredujejo v tretje države
9. **Obdobje hrambe**:
   - Fotografije in glasovni posnetki: `photo_retention_days` dni od nastanka zapisa
   - Evidence ur in aktivnosti: 10 let (standardna arhivska obveznost)
10. **Pravice posameznika** — fixed block covering: dostop, popravek, izbris, omejitev, ugovor, prenosljivost
11. **Preklic privolitve** — fixed: "Privolitev lahko kadar koli prekličete, ne da bi to vplivalo na zakonitost obdelave, ki se je izvajala do preklica."
12. **Pritožba nadzornemu organu** — fixed: Informacijski pooblaščenec, Dunajska 22, 1000 Ljubljana, gp.ip@ip-rs.si, 01 230 97 30, www.ip-rs.si
13. **Avtomatizirano odločanje** — fixed: "Ne izvajamo avtomatiziranega sprejemanja odločitev niti profiliranja."
14. **Dodatne določbe** — rendered only if `manager.gdpr_additional_clauses` is non-empty; displayed as a labelled section with the stored text
15. **Podpis** — blank signature block: date line + volunteer name line + signature line

No external hyperlinks. Laws referenced by name and number only.

---

## API

### New router: `api/routers/documents.py`

Mounted at `/documents`, tag `documents`.

**`GET /documents/consent-pdf`**
- Auth: `require_manager`
- Loads Manager from DB; raises 503 if not configured
- Reads `photo_retention_days` from settings
- Calls `render_consent_pdf(manager, photo_retention_days)`
- Returns `StreamingResponse`, `application/pdf`, `Content-Disposition: attachment; filename="soglasje_gdpr.pdf"`

### Existing: `PATCH /settings`

Extend the settings Pydantic request schema to include:

```python
gdpr_additional_clauses: str | None = None
```

The settings PATCH handler saves it to the Manager row when present.

### Registration

Register the new router in `api/main.py`:

```python
from routers.documents import router as documents_router
app.include_router(documents_router)
```

---

## Frontend

### Navigation

Add "Dokumenti" as a new tab in the dashboard navigation, after the existing tabs.

### Dokumenti tab content

A single card with:

1. **Card header:** "Soglasje za obdelavo osebnih podatkov (GDPR)"
2. **Description:** one sentence — "Prenesite obrazec, ki ga natisnete in izročite prostovoljcu v podpis pred začetkom sodelovanja."
3. **"Dodatne določbe" textarea** — labelled "Dodatne določbe (neobvezno)"; placeholder: "Sem vpišite morebitne dodatne določbe, ki bodo dodane na konec dokumenta. Polje pustite prazno, če dodatnih določb ni."; auto-saved on blur via `PATCH /settings` with `{"gdpr_additional_clauses": value}`; pre-populated from manager settings on page load
4. **"Prenesi PDF" button** — calls `GET /documents/consent-pdf`; triggers browser file download

### JS pattern

Follows existing vanilla JS patterns in `index.html`. No new JS files. The Dokumenti tab section loads manager settings (already fetched on dashboard init) to pre-populate the textarea.

---

## Error Handling

- Manager not configured → 503, same pattern as report endpoints
- DB unavailable → unhandled exception propagates (existing behaviour)
- Empty `gdpr_additional_clauses` → section omitted from PDF, not an error

---

## Out of Scope

- Per-volunteer consent forms (blank template is sufficient)
- Tracking when consent was delivered, signed, or received
- Digital signatures
- Links to external government websites
- Consent withdrawal tracking
