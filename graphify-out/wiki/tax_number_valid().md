# tax_number_valid()

> 16 nodes · cohesion 0.18

## Key Concepts

- **tax_number_valid()** (11 connections) — `api/utils/tax_number.py`
- **TestTaxNumberValid** (10 connections) — `api/tests/test_tax_number.py`
- **test_tax_number.py** (2 connections) — `api/tests/test_tax_number.py`
- **.test_accepts_valid_bare_digits()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_accepts_si_prefix()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_accepts_lowercase_si_prefix()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_rejects_bad_check_digit()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_rejects_wrong_length()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_rejects_non_digits()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_rejects_empty()** (2 connections) — `api/tests/test_tax_number.py`
- **.test_check_digit_one_case()** (2 connections) — `api/tests/test_tax_number.py`
- **tax_number.py** (2 connections) — `api/utils/tax_number.py`
- **.test_check_digit_zero_case()** (1 connections) — `api/tests/test_tax_number.py`
- **Tests for Slovenian tax number (davčna številka) validation.** (1 connections) — `api/tests/test_tax_number.py`
- **Slovenian tax number (davčna številka) validation utilities.** (1 connections) — `api/utils/tax_number.py`
- **Return True if value passes the Modulus 11 check digit algorithm.      Accepts b** (1 connections) — `api/utils/tax_number.py`

## Relationships

- [[manager.py]] (1 shared connections)

## Source Files

- `api/tests/test_tax_number.py`
- `api/utils/tax_number.py`

## Audit Trail

- EXTRACTED: 28 (62%)
- INFERRED: 17 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*