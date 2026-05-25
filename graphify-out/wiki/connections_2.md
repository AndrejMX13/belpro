# connections

> 38 nodes

## Key Concepts

- **Volunteer (ORM)** (25 connections) — `api/models/volunteer.py`
- **_to_response()** (12 connections) — `api/routers/volunteers.py`
- **create_volunteer()** (12 connections) — `api/routers/volunteers.py`
- **volunteers.py** (11 connections) — `api/routers/volunteers.py`
- **list_volunteers()** (10 connections) — `api/routers/volunteers.py`
- **_to_detail_response()** (9 connections) — `api/routers/volunteers.py`
- **VolunteerResponse (Schema)** (9 connections) — `api/schemas/volunteer.py`
- **check_emso()** (8 connections) — `api/routers/volunteers.py`
- **update_volunteer()** (8 connections) — `api/routers/volunteers.py`
- **get_volunteer()** (7 connections) — `api/routers/volunteers.py`
- **activate_volunteer()** (6 connections) — `api/routers/volunteers.py`
- **deactivate_volunteer()** (6 connections) — `api/routers/volunteers.py`
- **AnalyticsSummary (Schema)** (5 connections) — `api/schemas/analytics.py`
- **VolunteerCreate (Schema)** (5 connections) — `api/schemas/volunteer.py`
- **VolunteerDetailResponse (Schema)** (4 connections) — `api/schemas/volunteer.py`
- **delete_volunteer()** (3 connections) — `api/routers/volunteers.py`
- **HoursPerVolunteer (Schema)** (2 connections) — `api/schemas/analytics.py`
- **VolunteerListResponse (Schema)** (2 connections) — `api/schemas/volunteer.py`
- **VolunteerUpdate (Schema)** (2 connections) — `api/schemas/volunteer.py`
- **EmsoCheckRequest (Schema)** (2 connections) — `api/schemas/volunteer.py`
- **encrypt_emso (Service)** (2 connections) — `api/services/encryption.py`
- **hash_emso (Service)** (2 connections) — `api/services/encryption.py`
- **Volunteers CRUD router.** (1 connections) — `api/routers/volunteers.py`
- **Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object.** (1 connections) — `api/routers/volunteers.py`
- **Same as _to_response but includes sorted log_entries and computed hours for the** (1 connections) — `api/routers/volunteers.py`
- *... and 13 more nodes in this community*

## Relationships

- [[app_settings.py]] (14 shared connections)
- [[connections]] (8 shared connections)
- [[scripts/setup.sh]] (6 shared connections)
- [[renderDetail() — volunteer detail page]] (4 shared connections)
- [[Code Reviewer Skill]] (2 shared connections)
- [[load_key()]] (1 shared connections)
- [[BelPro System Specification]] (1 shared connections)

## Source Files

- `api/models/volunteer.py`
- `api/routers/volunteers.py`
- `api/schemas/analytics.py`
- `api/schemas/volunteer.py`
- `api/services/encryption.py`

## Audit Trail

- EXTRACTED: 124 (74%)
- INFERRED: 44 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*