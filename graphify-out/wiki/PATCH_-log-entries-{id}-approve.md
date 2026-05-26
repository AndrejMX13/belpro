# PATCH /log-entries/{id}/approve

> 17 nodes

## Key Concepts

- **EMŠO Encryption Key Rotation — Procedure Guide** (11 connections) — `docs/emso_key_rotation.md`
- **Step 1 — Save the current key** (2 connections) — `docs/emso_key_rotation.md`
- **Step 2 — Generate a new key** (2 connections) — `docs/emso_key_rotation.md`
- **Step 3 — Run the rotation script** (2 connections) — `docs/emso_key_rotation.md`
- **Step 4 — Update `.env` and restart the API (while script is paused)** (2 connections) — `docs/emso_key_rotation.md`
- **If something goes wrong** (2 connections) — `docs/emso_key_rotation.md`
- **emso_key_rotation.md** (1 connections) — `docs/emso_key_rotation.md`
- **When to use this** (1 connections) — `docs/emso_key_rotation.md`
- **Prerequisites** (1 connections) — `docs/emso_key_rotation.md`
- **code:bash (grep EMSO_ENCRYPTION_KEY .env)** (1 connections) — `docs/emso_key_rotation.md`
- **code:bash (NEW_KEY=$(python3 -c "import secrets,base64; print(base64.ur)** (1 connections) — `docs/emso_key_rotation.md`
- **code:bash (bash scripts/rotate_emso_key.sh <OLD_KEY> "$NEW_KEY")** (1 connections) — `docs/emso_key_rotation.md`
- **code:bash (# Edit .env — change EMSO_ENCRYPTION_KEY to the new value)** (1 connections) — `docs/emso_key_rotation.md`
- **Step 5 — Confirm cleanup in the first terminal** (1 connections) — `docs/emso_key_rotation.md`
- **Backups taken before this rotation** (1 connections) — `docs/emso_key_rotation.md`
- **code:bash (bash scripts/rotate_emso_key.sh --restore)** (1 connections) — `docs/emso_key_rotation.md`
- **Known issues encountered during development** (1 connections) — `docs/emso_key_rotation.md`

## Relationships

- No strong cross-community connections detected

## Source Files

- `docs/emso_key_rotation.md`

## Audit Trail

- EXTRACTED: 32 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*