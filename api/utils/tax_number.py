"""Slovenian tax number (davčna številka) validation utilities."""

_WEIGHTS = (8, 7, 6, 5, 4, 3, 2)


def tax_number_valid(value: str) -> bool:
    """Return True if value passes the Modulus 11 check digit algorithm.

    Accepts bare 8-digit strings ("12345678") or SI-prefixed strings
    ("SI12345678"). Returns False for any other input.
    """
    digits = value.upper().removeprefix("SI")
    if len(digits) != 8 or not digits.isdigit():
        return False
    total = sum(w * int(d) for w, d in zip(_WEIGHTS, digits))
    remainder = total % 11
    check = 11 - remainder
    if check == 10:
        check = 0
    elif check == 11:
        check = 1
    return int(digits[7]) == check
