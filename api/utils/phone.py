import re


def normalize_phone(raw: str | None) -> str | None:
    """Return digits-only WhatsApp-native phone number, or None for invalid input.

    Strips +, spaces, dashes, parentheses. Returns None if fewer than 7 digits remain.
    Store the result directly — Evolution API and WhatsApp expect no + prefix.
    For display, callers prepend '+'.
    """
    if not raw:
        return None
    digits = re.sub(r"[^\d]", "", raw)
    if len(digits) < 7:
        return None
    return digits
