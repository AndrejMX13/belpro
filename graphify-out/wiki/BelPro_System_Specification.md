# BelPro System Specification

> 36 nodes

## Key Concepts

- **load_key()** (16 connections) — `api/services/encryption.py`
- **test_encryption.py** (14 connections) — `api/tests/test_encryption.py`
- **cmd_rotate()** (9 connections) — `api/scripts/rotate_emso_key.py`
- **encrypt_emso()** (8 connections) — `api/services/encryption.py`
- **hash_emso()** (8 connections) — `api/services/encryption.py`
- **mask_emso()** (8 connections) — `api/services/encryption.py`
- **decrypt_emso()** (7 connections) — `api/services/encryption.py`
- **cmd_backup()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **main()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **encryption.py** (6 connections) — `api/services/encryption.py`
- **rotate_emso_key.py** (5 connections) — `api/scripts/rotate_emso_key.py`
- **cmd_restore()** (5 connections) — `api/scripts/rotate_emso_key.py`
- **_db_url()** (4 connections) — `api/scripts/rotate_emso_key.py`
- **test_decrypt_with_wrong_key_raises_invalid_tag()** (4 connections) — `api/tests/test_encryption.py`
- **test_roundtrip_restores_plaintext()** (3 connections) — `api/tests/test_encryption.py`
- **test_hash_differs_from_encryption()** (3 connections) — `api/tests/test_encryption.py`
- **test_load_key_accepts_valid_32_byte_key()** (2 connections) — `api/tests/test_encryption.py`
- **test_load_key_rejects_short_key()** (2 connections) — `api/tests/test_encryption.py`
- **test_load_key_accepts_key_without_padding()** (2 connections) — `api/tests/test_encryption.py`
- **test_encrypt_produces_different_ciphertext_each_call()** (2 connections) — `api/tests/test_encryption.py`
- **test_hash_is_deterministic()** (2 connections) — `api/tests/test_encryption.py`
- **test_different_emso_produces_different_hash()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_replaces_all_but_last_three_chars()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_length_preserved()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_short_value_returned_unchanged()** (2 connections) — `api/tests/test_encryption.py`
- *... and 11 more nodes in this community*

## Relationships

- [[log_entries.py]] (14 shared connections)
- [[load_key()]] (4 shared connections)
- [[Community 348]] (1 shared connections)
- [[ops_server.py]] (1 shared connections)

## Source Files

- `api/scripts/rotate_emso_key.py`
- `api/services/encryption.py`
- `api/tests/test_encryption.py`

## Audit Trail

- EXTRACTED: 78 (55%)
- INFERRED: 64 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*