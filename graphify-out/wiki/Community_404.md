# Community 404

> 9 nodes

## Key Concepts

- **cmd_rotate()** (9 connections) — `api/scripts/rotate_emso_key.py`
- **cmd_backup()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **main()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **rotate_emso_key.py** (5 connections) — `api/scripts/rotate_emso_key.py`
- **cmd_restore()** (5 connections) — `api/scripts/rotate_emso_key.py`
- **_db_url()** (4 connections) — `api/scripts/rotate_emso_key.py`
- **Dump volunteers table + old key to out_path as JSON.** (1 connections) — `api/scripts/rotate_emso_key.py`
- **Restore emso + emso_hash for all volunteers from backup_path.** (1 connections) — `api/scripts/rotate_emso_key.py`
- **Re-encrypt all EMŠOs from old_key to new_key. Returns count of rotated records.** (1 connections) — `api/scripts/rotate_emso_key.py`

## Relationships

- [[get_report_history()]] (5 shared connections)
- [[005_report_prefs.py]] (3 shared connections)
- [[Community 363]] (1 shared connections)
- [[BelPro Project Memory Public Index]] (1 shared connections)

## Source Files

- `api/scripts/rotate_emso_key.py`

## Audit Trail

- EXTRACTED: 28 (74%)
- INFERRED: 10 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*