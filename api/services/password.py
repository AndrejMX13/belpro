"""Password hashing and verification using stdlib hashlib.scrypt.

No third-party dependency required.  Parameters follow RFC 7914
interactive-login recommendations (n=16384, r=8, p=1).
"""
from __future__ import annotations

import base64
import hashlib
import os
import secrets

_SALT_LEN = 32
_SCRYPT_N = 16384
_SCRYPT_R = 8
_SCRYPT_P = 1
_DK_LEN = 32


def hash_password(plain: str) -> str:
    """Return a base64-encoded scrypt digest of *plain*.

    Format: base64(salt || dk) where salt is 32 random bytes and dk is 32 bytes.
    """
    salt = os.urandom(_SALT_LEN)
    dk = hashlib.scrypt(
        plain.encode("utf-8"), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, dklen=_DK_LEN
    )
    return base64.b64encode(salt + dk).decode("ascii")


def verify_password(plain: str, stored: str) -> bool:
    """Return True if *plain* matches the stored scrypt digest."""
    raw = base64.b64decode(stored)
    salt, dk = raw[:_SALT_LEN], raw[_SALT_LEN:]
    dk2 = hashlib.scrypt(
        plain.encode("utf-8"), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, dklen=_DK_LEN
    )
    return secrets.compare_digest(dk, dk2)
