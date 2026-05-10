"""Unit tests for VolunteerUpdate schema — no DB required."""
import pytest
from pydantic import ValidationError

from schemas.volunteer import VolunteerUpdate


def test_accepts_first_name():
    u = VolunteerUpdate(first_name="Ana")
    assert u.first_name == "Ana"


def test_accepts_last_name():
    u = VolunteerUpdate(last_name="Novak")
    assert u.last_name == "Novak"


def test_rejects_empty_first_name():
    with pytest.raises(ValidationError):
        VolunteerUpdate(first_name="")


def test_rejects_empty_last_name():
    with pytest.raises(ValidationError):
        VolunteerUpdate(last_name="")


def test_accepts_email_string():
    u = VolunteerUpdate(email="test@example.com")
    assert u.email == "test@example.com"


def test_coerces_empty_email_to_none():
    u = VolunteerUpdate(email="")
    assert u.email is None


def test_accepts_none_email():
    u = VolunteerUpdate(email=None)
    assert u.email is None


def test_normalises_phone():
    u = VolunteerUpdate(phone="+386 41 123 456")
    assert u.phone == "38641123456"


def test_all_none_produces_empty_dump():
    u = VolunteerUpdate()
    assert u.model_dump(exclude_none=True) == {}


def test_first_name_included_in_dump():
    u = VolunteerUpdate(first_name="Maja")
    assert u.model_dump(exclude_none=True) == {"first_name": "Maja"}
