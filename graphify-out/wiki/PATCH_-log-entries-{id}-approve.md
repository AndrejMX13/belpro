# PATCH /log-entries/{id}/approve

> 17 nodes

## Key Concepts

- **Rotacija ključa za šifriranje EMŠO — Navodila za postopek** (11 connections) — `docs/emso_key_rotation_sl.md`
- **Korak 1 — Shranite trenutni ključ** (2 connections) — `docs/emso_key_rotation_sl.md`
- **Korak 2 — Ustvarite nov ključ** (2 connections) — `docs/emso_key_rotation_sl.md`
- **Korak 3 — Zaženite skript za rotacijo** (2 connections) — `docs/emso_key_rotation_sl.md`
- **Korak 4 — Posodobite `.env` in znova zaženite API (med pavzo skripta)** (2 connections) — `docs/emso_key_rotation_sl.md`
- **Če gre kaj narobe** (2 connections) — `docs/emso_key_rotation_sl.md`
- **emso_key_rotation_sl.md** (1 connections) — `docs/emso_key_rotation_sl.md`
- **Kdaj se to opravi** (1 connections) — `docs/emso_key_rotation_sl.md`
- **Predpogoji** (1 connections) — `docs/emso_key_rotation_sl.md`
- **code:bash (grep EMSO_ENCRYPTION_KEY .env)** (1 connections) — `docs/emso_key_rotation_sl.md`
- **code:bash (NEW_KEY=$(python3 -c "import secrets,base64; print(base64.ur)** (1 connections) — `docs/emso_key_rotation_sl.md`
- **code:bash (bash scripts/rotate_emso_key.sh <STAR_KLJUC> "$NEW_KEY")** (1 connections) — `docs/emso_key_rotation_sl.md`
- **code:bash (# Uredite .env — spremenite EMSO_ENCRYPTION_KEY na novo vred)** (1 connections) — `docs/emso_key_rotation_sl.md`
- **Korak 5 — Potrdite čiščenje v prvem terminalu** (1 connections) — `docs/emso_key_rotation_sl.md`
- **Varnostne kopije ustvarjene pred rotacijo** (1 connections) — `docs/emso_key_rotation_sl.md`
- **code:bash (bash scripts/rotate_emso_key.sh --restore)** (1 connections) — `docs/emso_key_rotation_sl.md`
- **Znane težave, odkrite med razvojem** (1 connections) — `docs/emso_key_rotation_sl.md`

## Relationships

- No strong cross-community connections detected

## Source Files

- `docs/emso_key_rotation_sl.md`

## Audit Trail

- EXTRACTED: 32 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*