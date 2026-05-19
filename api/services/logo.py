"""NGO logo file management."""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, UnidentifiedImageError

LOGO_DIR = Path("/app/photos/logo")
LOGO_PATH = LOGO_DIR / "logo.png"

_ALLOWED_RASTER_FORMATS = {"JPEG", "PNG", "WEBP", "GIF", "BMP", "TIFF"}


def logo_exists() -> bool:
    """Return True if a logo file is present on disk."""
    return LOGO_PATH.exists()


def delete_logo() -> None:
    """Remove the logo file if it exists. Silent if absent."""
    LOGO_PATH.unlink(missing_ok=True)


def save_logo(data: bytes) -> None:
    """Validate, normalize to PNG, and persist logo bytes.

    Accepts raster formats Pillow can open (JPEG, PNG, WebP, GIF, BMP, TIFF).
    Raises ValueError for unsupported or corrupt input.
    """
    img = _open_image(data)
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    img.save(LOGO_PATH, format="PNG")


def _open_image(data: bytes) -> Image.Image:
    """Open image bytes with Pillow. Raises ValueError for unsupported or corrupt input."""
    try:
        img = Image.open(io.BytesIO(data))
        if img.format is None or img.format.upper() not in _ALLOWED_RASTER_FORMATS:
            raise ValueError(f"Nepodprta oblika datoteke: {img.format}")
        img.load()  # force full read to catch truncated files
        return img
    except UnidentifiedImageError as exc:
        raise ValueError("Nepodprta ali poškodovana datoteka.") from exc
