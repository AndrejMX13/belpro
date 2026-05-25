# EvolutionClient

> 12 nodes · cohesion 0.17

## Key Concepts

- **EvolutionClient** (7 connections) — `api/services/evolution.py`
- **get_config_info()** (4 connections) — `api/routers/managers.py`
- **ConfigInfoResponse** (4 connections) — `api/schemas/manager.py`
- **.send_document()** (4 connections) — `api/services/evolution.py`
- **.get_connected_phone()** (3 connections) — `api/services/evolution.py`
- **evolution.py** (2 connections) — `api/services/evolution.py`
- **Return config status for the settings UI; auto-syncs WhatsApp phone if connected** (1 connections) — `api/routers/managers.py`
- **Response schema for GET /managers/me/config-info.** (1 connections) — `api/schemas/manager.py`
- **.__init__()** (1 connections) — `api/services/evolution.py`
- **Async HTTP client for the Evolution API WhatsApp gateway.** (1 connections) — `api/services/evolution.py`
- **Return (normalized_phone, state) for the configured instance.          States: "** (1 connections) — `api/services/evolution.py`
- **Send a PDF document to a WhatsApp number via Evolution API sendMedia.** (1 connections) — `api/services/evolution.py`

## Relationships

- [[send_monthly_reports()]] (3 shared connections)
- [[managers.py]] (1 shared connections)
- [[BaseModel]] (1 shared connections)
- [[manager.py]] (1 shared connections)
- [[normalize_phone()]] (1 shared connections)
- [[n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)]] (1 shared connections)

## Source Files

- `api/routers/managers.py`
- `api/schemas/manager.py`
- `api/services/evolution.py`

## Audit Trail

- EXTRACTED: 23 (77%)
- INFERRED: 7 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*