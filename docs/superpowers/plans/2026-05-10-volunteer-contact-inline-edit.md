# Volunteer Contact Inline Edit — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make first_name, last_name, phone, and email editable on the volunteer detail page via per-zone inline pencil-edit with Save/Cancel, without a separate modal or form.

**Architecture:** Backend extends `VolunteerUpdate` with the four new fields and wraps the phone uniqueness `IntegrityError` in the update endpoint. Frontend restructures the detail header HTML to embed edit zones and wires them up with a shared `wireInlineEdit` helper after render.

**Tech Stack:** FastAPI, Pydantic v2, SQLAlchemy 2.x (backend); vanilla JS, existing `API.volunteers.update` fetch wrapper (frontend); pytest + pytest-asyncio (schema unit tests).

---

## File Map

| File | Change |
|------|--------|
| `api/schemas/volunteer.py` | Add `first_name`, `last_name`, `email` to `VolunteerUpdate`; add `_coerce_empty_email` validator |
| `api/routers/volunteers.py` | Wrap `db.commit()` in `update_volunteer` with `IntegrityError` → HTTP 409 |
| `api/tests/__init__.py` | Create (empty) |
| `api/tests/test_volunteer_update_schema.py` | Create — unit tests for `VolunteerUpdate` validation |
| `frontend/js/volunteers.js` | Restructure detail header HTML; add `wireInlineEdit` helper; wire 3 edit zones |

---

## Task 1: Create test infrastructure and failing schema tests

**Files:**
- Create: `api/tests/__init__.py`
- Create: `api/tests/test_volunteer_update_schema.py`

- [ ] **Step 1: Create the tests directory and empty `__init__.py`**

```bash
docker compose exec api mkdir -p tests
docker compose exec api touch tests/__init__.py
```

- [ ] **Step 2: Write the failing test file**

Create `api/tests/test_volunteer_update_schema.py`:

```python
"""Unit tests for VolunteerUpdate schema — no DB required."""
import pytest
from pydantic import ValidationError

from schemas.volunteer import VolunteerUpdate


def test_accepts_first_name():
    u = VolunteerUpdate(first_name="Ana")
    assert u.first_name == "Ana"


def test_accepts_last_name():
    u = VolunteerUpdate(last_name="Novak")
    assert u.last_name == "Novak"


def test_rejects_empty_first_name():
    with pytest.raises(ValidationError):
        VolunteerUpdate(first_name="")


def test_rejects_empty_last_name():
    with pytest.raises(ValidationError):
        VolunteerUpdate(last_name="")


def test_accepts_email_string():
    u = VolunteerUpdate(email="test@example.com")
    assert u.email == "test@example.com"


def test_coerces_empty_email_to_none():
    u = VolunteerUpdate(email="")
    assert u.email is None


def test_accepts_none_email():
    u = VolunteerUpdate(email=None)
    assert u.email is None


def test_normalises_phone():
    u = VolunteerUpdate(phone="+386 41 123 456")
    assert u.phone == "38641123456"


def test_all_none_produces_empty_dump():
    u = VolunteerUpdate()
    assert u.model_dump(exclude_none=True) == {}


def test_first_name_included_in_dump():
    u = VolunteerUpdate(first_name="Maja")
    assert u.model_dump(exclude_none=True) == {"first_name": "Maja"}
```

- [ ] **Step 3: Run tests — verify they fail**

```bash
docker compose exec api pytest tests/test_volunteer_update_schema.py -v
```

Expected: most tests FAIL with `ValidationError` or assertion errors because `first_name`, `last_name`, `email` are not yet in `VolunteerUpdate`.

---

## Task 2: Extend VolunteerUpdate schema

**Files:**
- Modify: `api/schemas/volunteer.py`

- [ ] **Step 1: Replace the `VolunteerUpdate` class**

In `api/schemas/volunteer.py`, replace the existing `VolunteerUpdate` class (lines 109–121) with:

```python
class VolunteerUpdate(BaseModel):
    """Fields that can be updated on an existing volunteer."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    phone: Annotated[str, Field(min_length=1, max_length=30)] | None = None
    email: str | None = None
    report_whatsapp: bool | None = None
    report_email: bool | None = None

    @field_validator("phone", mode="after")
    @classmethod
    def _normalise_phone_field(cls, v: str | None) -> str | None:
        """Normalise phone to bare E.164 digits, pass through None."""
        if v is None:
            return None
        return _normalise_phone(v)

    @field_validator("email", mode="before")
    @classmethod
    def _coerce_empty_email(cls, v: object) -> object:
        """Treat empty string as absent — store None rather than ''."""
        if v == "":
            return None
        return v
```

Note: `EmailStr` is intentionally not used here. An email address is either present or null; format correctness is verified when the address is actually used.

- [ ] **Step 2: Run the schema tests — verify they pass**

```bash
docker compose exec api pytest tests/test_volunteer_update_schema.py -v
```

Expected: all 10 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add api/schemas/volunteer.py api/tests/__init__.py api/tests/test_volunteer_update_schema.py
git commit -m "feat: extend VolunteerUpdate with first_name, last_name, email fields"
```

---

## Task 3: Handle phone IntegrityError in update_volunteer

**Files:**
- Modify: `api/routers/volunteers.py`

The existing `update_volunteer` endpoint does not catch `IntegrityError`, so a duplicate phone number causes a 500. The fix mirrors the pattern already used in `create_volunteer`.

- [ ] **Step 1: Add IntegrityError import (already present — verify)**

Check line 12 of `api/routers/volunteers.py`:

```python
from sqlalchemy.exc import IntegrityError
```

It is already imported. No change needed.

- [ ] **Step 2: Wrap the commit in update_volunteer**

In `api/routers/volunteers.py`, replace the body of `update_volunteer` after the `setattr` loop:

Find this block (currently around line 354–361):

```python
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(volunteer, field, value)

    await db.commit()
    await db.refresh(volunteer)

    key = load_key(settings.emso_encryption_key)
    return _to_response(volunteer, key)
```

Replace with:

```python
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(volunteer, field, value)

    try:
        await db.commit()
        await db.refresh(volunteer)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ta telefonska številka je že registrirana.",
        )

    key = load_key(settings.emso_encryption_key)
    return _to_response(volunteer, key)
```

- [ ] **Step 3: Rebuild the API container and verify startup**

```bash
docker compose up -d --build api
docker compose logs api --tail=20
```

Expected: container starts, no import errors.

- [ ] **Step 4: Smoke-test the endpoint via FastAPI docs**

Open `http://localhost:8100/docs`, find `PATCH /volunteers/{volunteer_id}`, and confirm the request body now shows `first_name`, `last_name`, `email` as optional fields alongside the existing ones.

- [ ] **Step 5: Commit**

```bash
git add api/routers/volunteers.py
git commit -m "fix: handle duplicate phone IntegrityError in update_volunteer (409)"
```

---

## Task 4: Frontend — inline edit zones on the detail page

**Files:**
- Modify: `frontend/js/volunteers.js`

Two changes inside `renderDetail()`:
1. Restructure the detail header HTML to embed edit zones with stable IDs.
2. Add a `wireInlineEdit` helper and call it for each of the 3 zones after the HTML is set.

- [ ] **Step 1: Replace the detail-header and detail-meta HTML block**

In `renderDetail()`, find the existing header block (lines 708–718):

```javascript
      <div class="detail-header">
        <div class="detail-avatar">${initials}</div>
        <div>
          <div class="detail-name">${esc(v.first_name + ' ' + v.last_name)}</div>
          <div class="detail-meta">${esc(v.phone)}${v.email ? ' · ' + esc(v.email) : ''}</div>
          <div style="margin-top:0.4rem">
            ${v.active
              ? '<span class="badge badge-active">Aktiven</span>'
              : '<span class="badge badge-inactive">Neaktiven</span>'}
          </div>
        </div>
      </div>
```

Replace with:

```javascript
      <div class="detail-header">
        <div class="detail-avatar" id="vol-avatar">${initials}</div>
        <div>
          <div class="detail-name" style="display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap">
            <span id="vol-name-text">${esc(v.first_name + ' ' + v.last_name)}</span>
            <button class="btn btn-ghost btn-sm" id="vol-name-pencil" title="Uredi ime" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-name-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-fname" value="${esc(v.first_name)}" maxlength="100" style="width:7rem">
              <input type="text" id="vol-lname" value="${esc(v.last_name)}" maxlength="100" style="width:9rem">
              <button class="btn btn-primary btn-sm" id="vol-name-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-name-cancel">Prekliči</button>
              <span id="vol-name-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
          </div>
          <div class="detail-meta" style="display:flex;align-items:center;gap:0.3rem;flex-wrap:wrap;margin-top:0.2rem">
            <span id="vol-phone-text">${esc(v.phone)}</span>
            <button class="btn btn-ghost btn-sm" id="vol-phone-pencil" title="Uredi telefon" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-phone-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-phone-inp" value="${esc(v.phone)}" maxlength="30" style="width:12rem">
              <button class="btn btn-primary btn-sm" id="vol-phone-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-phone-cancel">Prekliči</button>
              <span id="vol-phone-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
            <span id="vol-email-sep">${v.email ? ' · ' : ''}</span>
            <span id="vol-email-text">${v.email ? esc(v.email) : ''}</span>
            <button class="btn btn-ghost btn-sm" id="vol-email-pencil" title="Uredi e-pošto" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-email-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-email-inp" value="${v.email ? esc(v.email) : ''}" maxlength="255" style="width:14rem" placeholder="E-poštni naslov (neobvezno)">
              <button class="btn btn-primary btn-sm" id="vol-email-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-email-cancel">Prekliči</button>
              <span id="vol-email-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
          </div>
          <div style="margin-top:0.4rem">
            ${v.active
              ? '<span class="badge badge-active">Aktiven</span>'
              : '<span class="badge badge-inactive">Neaktiven</span>'}
          </div>
        </div>
      </div>
```

Note: input spans use `style="display:none"` — **not** the `hidden` attribute — because the `hidden` attribute is overridden by any inline `display:` style. The JS toggles `inputsEl.style.display` between `'flex'` and `'none'`.

- [ ] **Step 2: Add the wireInlineEdit helper and zone wiring**

After the existing `$('back-btn').addEventListener(...)` block (around line 810), add:

```javascript
    function wireInlineEdit({ pencilId, inputsId, textId, saveId, cancelId, errId, validate, getPayload, onSuccess }) {
      const pencilEl = $(pencilId);
      const inputsEl = $(inputsId);
      const textEl   = $(textId);
      const saveEl   = $(saveId);
      const cancelEl = $(cancelId);
      const errEl    = $(errId);

      const inputs = Array.from(inputsEl.querySelectorAll('input'));
      let savedValues = [];

      function enterEdit() {
        savedValues            = inputs.map(inp => inp.value);
        textEl.hidden          = true;
        pencilEl.hidden        = true;
        inputsEl.style.display = 'flex';
        errEl.textContent      = '';
        inputs[0].focus();
      }

      function exitEdit() {
        inputsEl.style.display = 'none';
        textEl.hidden          = false;
        pencilEl.hidden        = false;
        errEl.textContent      = '';
      }

      pencilEl.addEventListener('click', enterEdit);

      // Restore values typed but not saved so the zone reopens clean.
      cancelEl.addEventListener('click', () => {
        inputs.forEach((inp, i) => { inp.value = savedValues[i]; });
        exitEdit();
      });
      saveEl.addEventListener('click', async () => {
        const validationErr = validate ? validate() : null;
        if (validationErr) { errEl.textContent = validationErr; return; }
        saveEl.disabled    = true;
        saveEl.textContent = 'Shranjevanje…';
        try {
          await API.volunteers.update(id, getPayload());
          onSuccess();
          exitEdit();
          toast('Podatki so bili shranjeni.');
        } catch (e) {
          errEl.textContent = e.message;
        } finally {
          saveEl.disabled    = false;
          saveEl.textContent = 'Shrani';
        }
      });
    }

    // Name zone
    wireInlineEdit({
      pencilId: 'vol-name-pencil', inputsId: 'vol-name-inputs',
      textId:   'vol-name-text',   saveId:   'vol-name-save',
      cancelId: 'vol-name-cancel', errId:    'vol-name-err',
      validate: () => {
        if (!$('vol-fname').value.trim()) return 'Ime ne sme biti prazno.';
        if (!$('vol-lname').value.trim()) return 'Priimek ne sme biti prazen.';
        return null;
      },
      getPayload: () => ({
        first_name: $('vol-fname').value.trim(),
        last_name:  $('vol-lname').value.trim(),
      }),
      onSuccess: () => {
        const fn = $('vol-fname').value.trim();
        const ln = $('vol-lname').value.trim();
        $('vol-name-text').textContent = fn + ' ' + ln;
        $('vol-avatar').textContent    = (fn[0] + ln[0]).toUpperCase();
      },
    });

    // Phone zone
    wireInlineEdit({
      pencilId: 'vol-phone-pencil', inputsId: 'vol-phone-inputs',
      textId:   'vol-phone-text',   saveId:   'vol-phone-save',
      cancelId: 'vol-phone-cancel', errId:    'vol-phone-err',
      validate: () => {
        if (!$('vol-phone-inp').value.trim()) return 'Telefonska številka ne sme biti prazna.';
        return null;
      },
      getPayload: () => ({ phone: $('vol-phone-inp').value.trim() }),
      onSuccess: () => {
        $('vol-phone-text').textContent = $('vol-phone-inp').value.trim();
      },
    });

    // Email zone
    wireInlineEdit({
      pencilId: 'vol-email-pencil', inputsId: 'vol-email-inputs',
      textId:   'vol-email-text',   saveId:   'vol-email-save',
      cancelId: 'vol-email-cancel', errId:    'vol-email-err',
      validate: null,
      getPayload: () => ({ email: $('vol-email-inp').value.trim() }),
      onSuccess: () => {
        const val = $('vol-email-inp').value.trim();
        $('vol-email-text').textContent = val;
        $('vol-email-sep').textContent  = val ? ' · ' : '';
      },
    });
```

- [ ] **Step 3: Verify the page loads without JS errors**

Open `http://localhost:80`, navigate to any volunteer detail page. Open browser DevTools console — there should be no errors. The detail header should show pencil buttons next to name, phone, and email.

- [ ] **Step 4: Test the name zone**

Click the ✏ next to the volunteer's name. Two inputs should appear pre-filled with first and last name, plus Save/Cancel. Edit the last name, click Save. The display should update in place (both name text and the avatar initials), and a toast should appear.

- [ ] **Step 5: Test the phone zone**

Click ✏ next to phone. Edit to a new number, Save. Display updates. Then try saving an already-registered phone number — the inline error "Ta telefonska številka je že registrirana." should appear below the input.

- [ ] **Step 6: Test the email zone**

Click ✏ next to email. If the volunteer has no email, the input is empty — type an address and Save. The separator " · " and email should appear. Then edit again and clear the field, Save — both separator and email text should disappear.

- [ ] **Step 7: Test Cancel**

Open any edit zone, change a value, click Prekliči. The original value should be restored and inputs should hide without a network call.

- [ ] **Step 8: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: inline editing of name, phone, email on volunteer detail page"
```
