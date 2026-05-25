# volunteer.py

> 13 nodes · cohesion 0.18

## Key Concepts

- **volunteer.py** (13 connections) — `api/schemas/volunteer.py`
- **VolunteerResponse** (6 connections) — `api/schemas/volunteer.py`
- **VolunteerDetailResponse** (5 connections) — `api/schemas/volunteer.py`
- **LogEntryBrief** (4 connections) — `api/schemas/volunteer.py`
- **_normalise_phone()** (3 connections) — `api/schemas/volunteer.py`
- **_validate_emso_checksum()** (2 connections) — `api/schemas/volunteer.py`
- **_normalise_phone_field()** (2 connections) — `api/schemas/volunteer.py`
- **_coerce_empty_email()** (1 connections) — `api/schemas/volunteer.py`
- **Pydantic schemas for the Volunteer entity.** (1 connections) — `api/schemas/volunteer.py`
- **Strip whitespace and leading ``+``, return bare E.164 digits.** (1 connections) — `api/schemas/volunteer.py`
- **Compact log entry view — used inside VolunteerDetailResponse.** (1 connections) — `api/schemas/volunteer.py`
- **Volunteer data returned to the manager dashboard.      emso_masked is computed** (1 connections) — `api/schemas/volunteer.py`
- **Volunteer with full entry history — returned by GET /volunteers/{id}.** (1 connections) — `api/schemas/volunteer.py`

## Relationships

- [[BaseModel]] (9 shared connections)
- [[load_key()]] (3 shared connections)
- [[VolunteerUpdate]] (1 shared connections)

## Source Files

- `api/schemas/volunteer.py`

## Audit Trail

- EXTRACTED: 35 (85%)
- INFERRED: 6 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*