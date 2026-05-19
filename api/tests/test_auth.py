"""Tests for auth helpers and endpoints."""
import pytest

from core.auth import _make_session_token, _verify_session_token

_SECRET = "test-secret-key-32-bytes-padding!"


def test_make_and_verify_session_token() -> None:
    token = _make_session_token(_SECRET)
    assert isinstance(token, str)
    assert len(token) > 10
    assert _verify_session_token(token, _SECRET, duration_hours=24) is True


def test_verify_session_token_wrong_secret() -> None:
    token = _make_session_token(_SECRET)
    assert _verify_session_token(token, "wrong-secret", duration_hours=24) is False


def test_verify_session_token_garbage() -> None:
    assert _verify_session_token("notavalidtoken", _SECRET, duration_hours=24) is False


def test_verify_session_token_empty() -> None:
    assert _verify_session_token("", _SECRET, duration_hours=24) is False
