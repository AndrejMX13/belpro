---
name: FastAPI on_event deprecation — pending fix
description: Replace @app.on_event("startup") in api/main.py with lifespan context manager
type: project
originSessionId: 76a454b6-285f-40e8-8f89-c8ccb7ebb548
---
`api/main.py` line 36 uses the deprecated `@app.on_event("startup")` decorator, which produces a deprecation warning in every test run. Replace with the `lifespan` context manager pattern.

**Why:** FastAPI will eventually remove `on_event`. The warning appears consistently in `pytest` output and will clutter CI.

**How to apply:** Replace the startup handler and `FastAPI()` constructor call as follows:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    yield

app = FastAPI(
    title="BelPro API",
    description="Volunteer diary management API for Slovenian NGOs.",
    version="0.9.3",
    lifespan=lifespan,
)
```

Remove the `@app.on_event("startup")` decorator and `verify_db_connection` function entirely.
