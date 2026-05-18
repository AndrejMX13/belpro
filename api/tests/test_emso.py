"""Unit tests for the EMŠO checksum validator utility."""
import pytest
from utils.emso import emso_checksum_valid


@pytest.mark.parametrize("emso", [
    "0101990500003",  # valid: mod=8, check=3
    "1234567890125",  # valid: mod=6, check=5
])
def test_emso_checksum_valid_accepts_valid_numbers(emso: str) -> None:
    assert emso_checksum_valid(emso) is True


@pytest.mark.parametrize("emso", [
    "1234567890123",  # 13 digits but wrong checksum (check should be 5)
    "9876543210987",  # 13 digits but wrong checksum
])
def test_emso_checksum_valid_rejects_bad_checksum(emso: str) -> None:
    assert emso_checksum_valid(emso) is False


@pytest.mark.parametrize("emso", [
    "123",            # too short
    "12345678901234", # too long
    "123456789012a",  # non-digit
    "",
])
def test_emso_checksum_valid_rejects_malformed_input(emso: str) -> None:
    assert emso_checksum_valid(emso) is False
