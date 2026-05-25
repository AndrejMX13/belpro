# Manager session cookie lifetime in hours.

> 13 nodes

## Key Concepts

- **12. Pripomočki za testiranje** (6 connections) — `SPEC_SL.md`
- **`load_env.ps1` / `load_env.sh`** (3 connections) — `SPEC_SL.md`
- **`switch_manager_phone.ps1` / `switch_manager_phone.sh`** (3 connections) — `SPEC_SL.md`
- **Tipičen potek testiranja** (3 connections) — `SPEC_SL.md`
- **`list_pending_entries.py`** (2 connections) — `SPEC_SL.md`
- **code:block3 (. .\scripts\load_env.ps1)** (1 connections) — `SPEC_SL.md`
- **code:bash (source scripts/load_env.sh)** (1 connections) — `SPEC_SL.md`
- **code:block5 (.\scripts\switch_manager_phone.ps1 volunteer   # nastavi tel)** (1 connections) — `SPEC_SL.md`
- **code:bash (bash scripts/switch_manager_phone.sh volunteer)** (1 connections) — `SPEC_SL.md`
- **code:block7 (python scripts/list_pending_entries.py          # vnosi, ki )** (1 connections) — `SPEC_SL.md`
- **code:block8 (# 0. Nalaganje okoljskih spremenljivk (enkrat na sejo):)** (1 connections) — `SPEC_SL.md`
- **code:bash (# 0. Nalaganje okoljskih spremenljivk (enkrat na sejo):)** (1 connections) — `SPEC_SL.md`
- **Vozlišča ročnega sprožilca v n8n** (1 connections) — `SPEC_SL.md`

## Relationships

- [[PATCH /api/log-entries/{id} (update_log_entry)]] (1 shared connections)

## Source Files

- `SPEC_SL.md`

## Audit Trail

- EXTRACTED: 25 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*