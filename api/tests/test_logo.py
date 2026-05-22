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

    # First save: 1×1
    buf1 = io.BytesIO()
    Image.new("RGB", (1, 1)).save(buf1, format="PNG")
    logo_mod.save_logo(buf1.getvalue())

    # Second save: 2×2 — verifies overwrite actually replaced the file
    buf2 = io.BytesIO()
    Image.new("RGB", (2, 2)).save(buf2, format="PNG")
    logo_mod.save_logo(buf2.getvalue())

    saved = Image.open(logo_mod.LOGO_PATH)
    assert saved.size == (2, 2), "Second save must replace the first"


# ── integration tests: logo endpoints ─────────────────────────────────────────

@pytest.fixture(autouse=False)
def _clean_logo(tmp_path, monkeypatch):
    """Redirect logo storage to a temp dir for isolation.

    Never touches the real logo file on disk.
    """
    from services import logo as logo_mod
    test_dir = tmp_path / "logo"
    test_dir.mkdir()
    monkeypatch.setattr(logo_mod, "LOGO_DIR", test_dir)
    monkeypatch.setattr(logo_mod, "LOGO_PATH", test_dir / "logo.png")
    yield


@pytest.mark.asyncio
async def test_get_logo_returns_404_when_absent(client, _clean_logo):
    res = await client.get("/api/logo")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_upload_logo_and_retrieve(client, auth, _clean_logo):
    files = {"file": ("mylogo.png", _png_1x1(), "image/png")}
    res = await client.post("/api/logo", files=files, headers=auth)
    assert res.status_code == 204

    res = await client.get("/api/logo")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("image/png")


@pytest.mark.asyncio
async def test_upload_logo_requires_auth(client, _clean_logo):
    files = {"file": ("logo.png", _png_1x1(), "image/png")}
    res = await client.post("/api/logo", files=files)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_upload_invalid_logo_returns_422(client, auth, _clean_logo):
    files = {"file": ("logo.png", b"not an image", "image/png")}
    res = await client.post("/api/logo", files=files, headers=auth)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_delete_logo(client, auth, _clean_logo):
    # Upload first
    files = {"file": ("logo.png", _png_1x1(), "image/png")}
    await client.post("/api/logo", files=files, headers=auth)

    res = await client.delete("/api/logo", headers=auth)
    assert res.status_code == 204

    res = await client.get("/api/logo")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_logo_when_absent_returns_404(client, auth, _clean_logo):
    res = await client.delete("/api/logo", headers=auth)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_logo_requires_auth(client, _clean_logo):
    res = await client.delete("/api/logo")
    assert res.status_code == 401
