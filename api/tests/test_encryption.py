"""Unit tests for the EMŠO encryption service.

No database needed — pure crypto logic.
"""
import base64
import os

import pytest
from cryptography.exceptions import InvalidTag

from services.encryption import decrypt_emso, encrypt_emso, hash_emso, load_key, mask_emso

_EMSO = "1234567890123"

# A valid 32-byte key encoded as base64.
_KEY_B64 = base64.b64encode(os.urandom(32)).decode()
_KEY = load_key(_KEY_B64)


# ── load_key ──────────────────────────────────────────────────────────────────

def test_load_key_accepts_valid_32_byte_key() -> None:
    key = load_key(_KEY_B64)
    assert len(key) == 32


def test_load_key_rejects_short_key() -> None:
    bad = base64.b64encode(b"tooshort").decode()
    with pytest.raises(ValueError, match="32 bytes"):
        load_key(bad)


def test_load_key_accepts_key_without_padding() -> None:
    # Some base64 encoders strip trailing '=' padding.
    stripped = _KEY_B64.rstrip("=")
    key = load_key(stripped)
    assert len(key) == 32


# ── encrypt / decrypt roundtrip ───────────────────────────────────────────────

def test_roundtrip_restores_plaintext() -> None:
    assert decrypt_emso(encrypt_emso(_EMSO, _KEY), _KEY) == _EMSO


def test_encrypt_produces_different_ciphertext_each_call() -> None:
    # Fresh random nonce means two encryptions of the same value must differ.
    assert encrypt_emso(_EMSO, _KEY) != encrypt_emso(_EMSO, _KEY)


def test_decrypt_with_wrong_key_raises_invalid_tag() -> None:
    ciphertext = encrypt_emso(_EMSO, _KEY)
    wrong_key = load_key(base64.b64encode(os.urandom(32)).decode())
    with pytest.raises(InvalidTag):
        decrypt_emso(ciphertext, wrong_key)


# ── hash_emso ─────────────────────────────────────────────────────────────────

def test_hash_is_deterministic() -> None:
    assert hash_emso(_EMSO, _KEY) == hash_emso(_EMSO, _KEY)


def test_different_emso_produces_different_hash() -> None:
    assert hash_emso(_EMSO, _KEY) != hash_emso("9999999999999", _KEY)


def test_hash_differs_from_encryption() -> None:
    # Sanity: hash and ciphertext are different representations.
    assert hash_emso(_EMSO, _KEY) != encrypt_emso(_EMSO, _KEY)


# ── mask_emso ─────────────────────────────────────────────────────────────────

def test_mask_replaces_all_but_last_three_chars() -> None:
    assert mask_emso(_EMSO) == "**********123"


def test_mask_length_preserved() -> None:
    assert len(mask_emso(_EMSO)) == len(_EMSO)


def test_mask_short_value_returned_unchanged() -> None:
    assert mask_emso("ab") == "ab"


def test_mask_exactly_three_chars_returned_unchanged() -> None:
    assert mask_emso("123") == "123"
