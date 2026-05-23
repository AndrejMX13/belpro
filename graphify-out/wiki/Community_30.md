# Community 30

> 21 nodes · cohesion 0.14

## Key Concepts

- **test_encryption.py** (14 connections) — `api/tests/test_encryption.py`
- **encrypt_emso()** (11 connections) — `api/services/encryption.py`
- **hash_emso()** (8 connections) — `api/services/encryption.py`
- **mask_emso()** (8 connections) — `api/services/encryption.py`
- **encryption.py** (5 connections) — `api/services/encryption.py`
- **test_decrypt_with_wrong_key_raises_invalid_tag()** (3 connections) — `api/tests/test_encryption.py`
- **test_hash_differs_from_encryption()** (3 connections) — `api/tests/test_encryption.py`
- **test_different_emso_produces_different_hash()** (2 connections) — `api/tests/test_encryption.py`
- **test_encrypt_produces_different_ciphertext_each_call()** (2 connections) — `api/tests/test_encryption.py`
- **test_hash_is_deterministic()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_exactly_three_chars_returned_unchanged()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_length_preserved()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_replaces_all_but_last_three_chars()** (2 connections) — `api/tests/test_encryption.py`
- **test_mask_short_value_returned_unchanged()** (2 connections) — `api/tests/test_encryption.py`
- **test_roundtrip_restores_plaintext()** (2 connections) — `api/tests/test_encryption.py`
- **AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l** (1 connections) — `api/services/encryption.py`
- **Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag** (1 connections) — `api/services/encryption.py`
- **Decrypt EMŠO ciphertext produced by encrypt_emso.      Returns the plaintext str** (1 connections) — `api/services/encryption.py`
- **Return HMAC-SHA256 hex digest of plaintext EMŠO.      Deterministic (unlike encr** (1 connections) — `api/services/encryption.py`
- **Return EMŠO with all but the last 3 characters replaced by *.      Used in all A** (1 connections) — `api/services/encryption.py`
- **Unit tests for the EMŠO encryption service.  No database needed — pure crypto lo** (1 connections) — `api/tests/test_encryption.py`

## Relationships

- [[Community 40]] (9 shared connections)
- [[Community 33]] (3 shared connections)
- [[Community 7]] (2 shared connections)

## Source Files

- `api/services/encryption.py`
- `api/tests/test_encryption.py`

## Audit Trail

- EXTRACTED: 42 (57%)
- INFERRED: 32 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*