"""Tests for NGO logo service and endpoints."""
from __future__ import annotations

import io

import pytest
from PIL import Image


# ── helpers ───────────────────────────────────────────────────────────────────

def _png_1x1() -> bytes:
    """Minimal valid 1×1 PNG."""
    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color=(255, 0, 0)).save(buf, format="PNG")
    return buf.getvalue()


def _ico_16x16() -> bytes:
    """Minimal valid 16×16 ICO — openable by Pillow but not in allowed list."""
    buf = io.BytesIO()
    Image.new("RGB", (16, 16)).save(buf, format="ICO")
    return buf.getvalue()


# ── unit tests: logo service ──────────────────────────────────────────────────

def test_logo_not_exists_initially(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")
    assert not logo_mod.logo_exists()


def test_save_creates_png_on_disk(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")

    logo_mod.save_logo(_png_1x1())

    assert logo_mod.logo_exists()
    # Verify the saved file is a valid PNG regardless of input format
    saved = Image.open(logo_mod.LOGO_PATH)
    assert saved.format == "PNG"


def test_delete_removes_file(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")

    logo_mod.save_logo(_png_1x1())
    assert logo_mod.logo_exists()
    logo_mod.delete_logo()
    assert not logo_mod.logo_exists()


def test_delete_when_no_logo_is_silent(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")
    # Must not raise
    logo_mod.delete_logo()


def test_open_image_rejects_corrupt_bytes(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")

    with pytest.raises(ValueError, match="Nepodprta"):
        logo_mod.save_logo(b"this is not an image and not SVG either")


def test_open_image_rejects_disallowed_format(tmp_path, monkeypatch):
    """ICO is openable by Pillow but excluded from the allowed set."""
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")

    with pytest.raises(ValueError):
        logo_mod.save_logo(_ico_16x16())


def test_save_overwrites_existing_logo(tmp_path, monkeypatch):
    import services.logo as logo_mod
    monkeypatch.setattr(logo_mod, "LOGO_DIR", tmp_path / "logo")
    monkeypatch.setattr(logo_mod, "LOGO_PATH", tmp_path / "logo" / "logo.png")

    logo_mod.save_logo(_png_1x1())

    logo_mod.save_logo(_png_1x1())

    # Both saves must produce a valid PNG
    assert logo_mod.LOGO_PATH.exists()
    Image.open(logo_mod.LOGO_PATH).verify()
