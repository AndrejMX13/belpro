"""AES-256-GCM encryption service for sensitive fields (EMŠO).

Usage
-----
key = load_key(settings.emso_encryption_key)
stored = encrypt_emso(plaintext, key)      # store this in the DB
plain  = decrypt_emso(stored, key)         # retrieve plaintext for masking
masked = mask_emso(plain)                  # safe to return in API responses

Security constraints
--------------------
- Never log plaintext EMŠO at any level.
- load_key() validates key length at startup so misconfiguration fails fast.
- Each call to encrypt_emso() generates a fresh 12-byte random nonce, so
  encrypting the same EMŠO twice produces different ciphertexts.
"""
from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_NONCE_BYTES = 12  # 96-bit nonce, recommended for AES-GCM


def load_key(b64_key: str) -> bytes:
    """Decode and validate a base64-encoded 32-byte AES-256 key.

    Raises ValueError if the decoded key is not exactly 32 bytes.
    Call once at startup so misconfiguration is caught before any request.
    """
    key = base64.b64decode(b64_key)
    if len(key) != 32:
        raise ValueError(
            f"EMSO_ENCRYPTION_KEY must decode to exactly 32 bytes, got {len(key)}"
        )
    return key


def encrypt_emso(plaintext: str, key: bytes) -> str:
    """Encrypt EMŠO with AES-256-GCM.

    Returns base64(nonce + ciphertext + auth_tag) — safe to store in a TEXT column.
    A fresh random nonce is generated for every call.
    """
    nonce = os.urandom(_NONCE_BYTES)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt_emso(ciphertext_b64: str, key: bytes) -> str:
    """Decrypt EMŠO ciphertext produced by encrypt_emso.

    Returns the plaintext string.  Raises cryptography.exceptions.InvalidTag
    if the ciphertext has been tampered with or the key is wrong.
    """
    raw = base64.b64decode(ciphertext_b64)
    nonce, ct = raw[:_NONCE_BYTES], raw[_NONCE_BYTES:]
    return AESGCM(key).decrypt(nonce, ct, None).decode("utf-8")


def mask_emso(plaintext: str) -> str:
    """Return EMŠO with all but the last 3 characters replaced by *.

    Used in all API responses and volunteer-facing PDFs.  The manager
    consolidated report may use the full plaintext if legally required.
    """
    if len(plaintext) <= 3:
        return plaintext
    return "*" * (len(plaintext) - 3) + plaintext[-3:]
