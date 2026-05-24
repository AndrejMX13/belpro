---
name: Release versioning strategy
description: BelPro release pipeline from alpha to 1.0.0
type: project
originSessionId: 3426c5bc-2b12-421d-9f19-b68bb96f0d39
---
Release pipeline follows this sequence:

1. **alpha** — active feature development, scope still open (current: v0.9.1-alpha)
2. **beta** — scope frozen, no new features; bug fixes only
3. **1.0.0-RC1** — release candidate, soak testing period
4. **1.0.0** — stable release after RC settles

**How to apply:** Don't suggest or add features once the user moves to beta. RC and 1.0.0 transitions are user-driven after observation periods.
