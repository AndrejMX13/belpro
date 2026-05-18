"""EMŠO (Enotna matična številka občana) validation utilities."""

_WEIGHTS = (7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2)


def emso_checksum_valid(emso: str) -> bool:
    """Return True if emso passes the mod-11 checksum.

    Assumes the caller already verified length (13) and all-digits — but also
    checks those here so the function is safe to call standalone.
    A mod-11 remainder of 1 means no valid check digit exists — treated as invalid.
    """
    if len(emso) != 13 or not emso.isdigit():
        return False
    total = sum(w * int(d) for w, d in zip(_WEIGHTS, emso))
    mod = total % 11
    if mod == 1:
        return False
    expected = 0 if mod == 0 else 11 - mod
    return int(emso[12]) == expected
