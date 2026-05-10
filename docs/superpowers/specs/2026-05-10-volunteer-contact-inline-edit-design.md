# Volunteer Contact Info — Inline Edit

**Date:** 2026-05-10
**Status:** Approved

---

## Problem

The volunteer detail page displays contact fields (name, surname, phone, email) as static text. These fields can change in real life (legal name changes, new phone, new email) and currently require a developer to edit the database directly.

## Out of Scope

EMŠO and `registered_at` are immutable through the UI. No edit path exists for them.

---

## Design

### Edit zones

Three independent edit zones on the detail page header area:

| Zone | Fields | Inputs shown on edit |
|------|--------|----------------------|
| Name | `first_name`, `last_name` | Two text inputs side by side |
| Phone | `phone` | One tel input |
| Email | `email` | One text input (not `type="email"` — no browser format enforcement) |

Each zone renders as: current value(s) as plain text + a small pencil button to the right. Clicking the pencil replaces the text with input(s) and reveals Save / Cancel buttons below the input(s). The pencil is hidden while the zone is in edit mode.

Concurrent edits across zones are allowed — each zone manages its own state independently. No coordination logic between zones.

### Interaction flow

1. User clicks pencil → inputs appear pre-filled with current values, Save/Cancel appear, pencil hides.
2. User edits and clicks **Save** → PATCH sent with only that zone's fields. On success: inputs replaced with new text, toast shown, pencil restored. On error: error message shown inline below the input(s), Save re-enabled.
3. User clicks **Cancel** → original values restored, edit mode exits, no network call.

### Error handling

- Phone already taken (DB unique constraint) → backend returns 409 → show "Ta telefonska številka je že registrirana." inline.
- Empty required field → prevent Save client-side, show inline validation message.
- Email: optional field. Submitting an empty email input clears the value (frontend sends `""`, backend converts `""` → `None`). No format validation — an email address is either present or null; correctness is verified when it is actually used.
- Generic network error → show error inline.

---

## Backend changes

**File:** `api/schemas/volunteer.py` — `VolunteerUpdate`

Add four new optional fields:

```python
first_name: str | None = None        # min_length=1 if provided
last_name: str | None = None         # min_length=1 if provided
phone: str | None = None             # min_length=1 if provided
email: str | None = None             # empty string coerced to None; no format validation
```

`first_name`, `last_name`, and `phone` must not be empty strings if provided — use `min_length=1` or a validator.
`email` accepts any non-empty string as-is. An empty string is coerced to `None` before the DB write. No format validation — correctness is verified when the address is actually used.

**File:** `api/routers/volunteers.py` — `update_volunteer`

No logic changes needed. The existing `model_dump(exclude_none=True)` + `setattr` loop already applies any fields present in `VolunteerUpdate`. The DB unique constraint on `phone` will surface as `IntegrityError` → wrap in a try/except that raises HTTP 409, matching the pattern in `create_volunteer`.

---

## Frontend changes

**File:** `frontend/js/volunteers.js` — `renderDetail()`

Three small helper closures (or a reusable `makeInlineEdit` function) wired up after the detail HTML is rendered:

- Each takes: container element, current value(s), field name(s), optional validator.
- Manages its own `editing` boolean flag.
- On save: calls `API.volunteers.update(id, payload)`, updates display text on success.

The name/phone/email display in the `.detail-header` block gains pencil buttons. EMŠO and `registered_at` in `.detail-info-grid` are unchanged.

No full re-render of the detail page on save — only the affected zone's text nodes update.

---

## What does not change

- `VolunteerCreate` schema — registration form is unaffected.
- `_to_response` / `_to_detail_response` helpers — already return all four fields.
- DB schema / Alembic migrations — no column changes.
- EMŠO handling — untouched.
- Report preferences card — untouched.
