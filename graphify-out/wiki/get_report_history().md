# get_report_history()

> 27 nodes

## Key Concepts

- **load_key()** (16 connections) — `api/services/encryption.py`
- **test_encryption.py** (14 connections) — `api/tests/test_encryption.py`
- **encrypt_emso()** (8 connections) — `api/services/encryption.py`
- **hash_emso()** (8 connections) — `api/services/encryption.py`
- **mask_emso()** (8 connections) — `api/services/encryption.py`
- **decrypt_emso()** (7 connections) — `api/services/encryption.py`
- **encryption.py** (6 connections) — `api/services/encryption.py`
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
- **test_mask_exactly_three_chars_returned_unchanged()** (2 connections) — `api/tests/test_encryption.py`
- **AES-256-GCM encryption service for sensitive fields (EMŠO).  Usage ----- key = l** (1 connections) — `api/services/encryption.py`
- **Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError** (1 connections) — `api/services/encryption.py`
- **Encrypt EMŠO with AES-256-GCM.      Returns base64(nonce + ciphertext + auth_tag** (1 connections) — `api/services/encryption.py`
- **Decrypt EMŠO ciphertext produced by encrypt_emso.      Returns the plaintext str** (1 connections) — `api/services/encryption.py`
- **Return HMAC-SHA256 hex digest of plaintext EMŠO.      Deterministic (unlike encr** (1 connections) — `api/services/encryption.py`
- *... and 2 more nodes in this community*

## Relationships

- [[errors.py]] (14 shared connections)
- [[Community 404]] (5 shared connections)
- [[path]] (1 shared connections)

## Source Files

- `api/services/encryption.py`
- `api/tests/test_encryption.py`

## Audit Trail

- EXTRACTED: 50 (48%)
- INFERRED: 54 (52%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*