# Encryption & Volunteer CRUD

**Nodes:** 23 | **Cohesion:** 0.162 | **Internal edges:** 41

## Files & Symbols
- `D:\Andrej\vsCode-workspace\BelPro\api\routers\volunteers.py` — 11 symbols (e.g. volunteers.py, _to_response(), ...)
- `api\services\encryption.py` — 12 symbols (e.g. encryption.py, load_key(), ...)

## Bridges To Other Communities
### → API Data Models & Schemas (16 edges)
- volunteers.py --rationale_for--> Volunteers CRUD router. [EXTRACTED]
- _to_response() --rationale_for--> Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object. [EXTRACTED]
- _to_response() --calls--> VolunteerResponse [INFERRED]
- _to_detail_response() --rationale_for--> Same as _to_response but includes sorted log_entries and computed hours for the [EXTRACTED]
- _to_detail_response() --calls--> VolunteerDetailResponse [INFERRED]
  ... and 11 more
### → API Request Handlers (1 edges)
- str --calls--> create_volunteer() [INFERRED]
