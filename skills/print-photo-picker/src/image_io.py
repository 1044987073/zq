"""Load images: HEIC → RGB, EXIF orientation fix before inference."""

from __future__ import annotations

import io
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pass


def _exif_orientation(img: Image.Image) -> int:
    try:
        exif = img.getexif()
        if exif:
            return int(exif.get(274, 1))  # Orientation
    except Exception:
        pass
    return 1


def _apply_orientation(img: Image.Image, orientation: int) -> Image.Image:
    if orientation == 1:
        return img
    transforms = {
        2: Image.FLIP_LEFT_RIGHT,
        3: Image.ROTATE_180,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.TRANSPOSE,
        6: Image.ROTATE_270,
        7: Image.TRANSVERSE,
        8: Image.ROTATE_90,
    }
    if orientation in transforms:
        return ImageOps.exif_transpose(img)
    return img


def _load_via_sips(path: Path) -> Optional[Image.Image]:
    """macOS fallback for problematic HEIC (HANDOFF §8.1)."""
    if os.uname().sysname != "Darwin":
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
        subprocess.run(
            ["sips", "-s", "format", "jpeg", str(path), "--out", tmp_path],
            check=True,
            capture_output=True,
        )
        img = Image.open(tmp_path).convert("RGB")
        # sips temp is in system temp; use os.remove only on our temp artifact
        os.remove(tmp_path)
        return img
    except Exception as exc:
        logger.warning("sips fallback failed for %s: %s", path, exc)
        return None


def is_likely_placeholder(path: Path) -> bool:
    """Cloud / sync placeholder (HANDOFF §8.5)."""
    try:
        st = path.stat()
        if getattr(st, "st_blocks", 1) == 0:
            return True
        if st.st_size > 0 and st.st_size < 128:
            return True
    except OSError:
        return True
    return False


def load_rgb_array(path: Path) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """
    Returns (H×W×3 uint8 RGB array, error_message).
    Orientation is applied before return.
    """
    path = Path(os.path.realpath(path))
    if is_likely_placeholder(path):
        return None, "placeholder_or_missing"

    img: Optional[Image.Image] = None
    err: Optional[str] = None
    try:
        img = Image.open(path)
        img = _apply_orientation(img, _exif_orientation(img))
        img = img.convert("RGB")
    except Exception as exc:
        err = str(exc)
        img = _load_via_sips(path)

    if img is None:
        return None, err or "open_failed"

    return np.asarray(img), None


def load_rgb_pil(path: Path) -> Tuple[Optional[Image.Image], Optional[str]]:
    arr, err = load_rgb_array(path)
    if arr is None:
        return None, err
    return Image.fromarray(arr), None
