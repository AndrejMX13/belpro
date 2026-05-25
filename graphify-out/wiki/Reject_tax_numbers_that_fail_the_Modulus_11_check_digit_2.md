# Reject tax numbers that fail the Modulus 11 check digit.

> 14 nodes

## Key Concepts

- **normalize_phone()** (16 connections) — `api/utils/phone.py`
- **test_phone_utils.py** (10 connections) — `api/tests/test_phone_utils.py`
- **test_strips_plus_prefix()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_spaces()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_dashes()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_parentheses()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_already_normalized()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_none_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_empty_string_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_whitespace_only_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_too_short_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_jid_phone_part()** (2 connections) — `api/tests/test_phone_utils.py`
- **phone.py** (1 connections) — `api/utils/phone.py`
- **Return digits-only WhatsApp-native phone number, or None for invalid input.** (1 connections) — `api/utils/phone.py`

## Relationships

- [[merge_semantic.py]] (2 shared connections)
- [[GET /api/log-entries (list_log_entries)]] (1 shared connections)
- [[n8n Set Node Pattern]] (1 shared connections)

## Source Files

- `api/tests/test_phone_utils.py`
- `api/utils/phone.py`

## Audit Trail

- EXTRACTED: 24 (50%)
- INFERRED: 24 (50%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*