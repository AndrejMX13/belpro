---
name: email-validator must be pinned explicitly
description: Packaging gotcha — pydantic[email] extra alone is not enough; email-validator must also be in requirements.txt
type: feedback
originSessionId: b5d90c39-2823-4927-ac2e-1a0be3c0f9b6
---
When using `EmailStr` from Pydantic, `pydantic[email]` in requirements.txt is not sufficient on its own — `email-validator` must also be listed explicitly as a pinned dependency.

**Why:** Discovered when the api container failed to start with `ImportError: email-validator is not installed`. The `pydantic[email]` extra declares it as a dependency but Docker pip install from a flat requirements.txt does not resolve extras transitively in all configurations.

**How to apply:** Any time `EmailStr` is used in a Pydantic model, ensure both `pydantic[email]==<ver>` and `email-validator==<ver>` appear in requirements.txt.

**Same pattern applies to `itsdangerous`** — assumed to be a transitive Starlette dep but is NOT installed in the BelPro Docker image. Must be pinned explicitly in requirements.txt (added as `itsdangerous==2.2.0` during ISS-005).
