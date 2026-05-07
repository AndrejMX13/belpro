# API Authentication

**Nodes:** 4 | **Cohesion:** 0.500 | **Internal edges:** 3

## Files & Symbols
- `api\core\auth.py` — 4 symbols (e.g. auth.py, require_manager(), ...)

## Bridges To Other Communities
### → API Data Models & Schemas (4 edges)
- Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw --uses--> Settings [INFERRED]
- Manager authentication — HTTP Basic Auth.  Password priority:   1. manager.passw --uses--> Manager [INFERRED]
- FastAPI dependency — rejects requests without the correct manager password. --uses--> Settings [INFERRED]
- FastAPI dependency — rejects requests without the correct manager password. --uses--> Manager [INFERRED]
