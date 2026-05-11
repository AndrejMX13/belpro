from utils.phone import normalize_phone


def test_strips_plus_prefix():
    assert normalize_phone("+38640123456") == "38640123456"


def test_strips_spaces():
    assert normalize_phone("+386 40 123 456") == "38640123456"


def test_strips_dashes():
    assert normalize_phone("+386-40-123-456") == "38640123456"


def test_strips_parentheses():
    assert normalize_phone("+1 (555) 123-4567") == "15551234567"


def test_already_normalized():
    assert normalize_phone("38640123456") == "38640123456"


def test_none_returns_none():
    assert normalize_phone(None) is None


def test_empty_string_returns_none():
    assert normalize_phone("") is None


def test_whitespace_only_returns_none():
    assert normalize_phone("   ") is None


def test_too_short_returns_none():
    # Fewer than 7 digits is not a plausible phone number
    assert normalize_phone("+1234") is None


def test_jid_phone_part():
    # Evolution API owner field arrives as "38640123456@s.whatsapp.net"
    # Callers split on "@" before calling normalize — test the phone part
    assert normalize_phone("38640123456@s.whatsapp.net".split("@")[0]) == "38640123456"
