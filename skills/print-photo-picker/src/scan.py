"""Recursive scan, integrity probe, MD5 exact dedup (HANDOFF §7 Step 1)."""

from __future__ import annotations

import hashlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Set

from PIL import Image

from .constants import EXCLUDE_DIR_NAMES, EXCLUDE_FILE_NAMES, EXCLUDE_SUFFIXES, IMAGE_EXTENSIONS
from .image_io import is_likely_placeholder

logger = logging.getLogger(__name__)


@dataclass
class ScannedFile:
    path: Path
    md5: str
    size: int
    mtime: float
    corrupt: bool = False
    skip_reason: Optional[str] = None


def _should_skip_dir(name: str) -> bool:
    low = name.lower()
    if low.startswith("."):
        return True
    return low in EXCLUDE_DIR_NAMES


def _should_skip_file(path: Path) -> bool:
    low_name = path.name.lower()
    if low_name in EXCLUDE_FILE_NAMES:
        return True
    if any(low_name.endswith(s) for s in EXCLUDE_SUFFIXES):
        return True
    return path.suffix.lower() not in IMAGE_EXTENSIONS


def iter_image_paths(
    source_dir: Path,
    output_dir: Optional[Path] = None,
    include_raw: bool = False,
) -> Iterable[Path]:
    source_dir = Path(os.path.realpath(source_dir))
    output_real = Path(os.path.realpath(output_dir)) if output_dir else None
    raw_ext = {".cr2", ".nef", ".arw", ".dng"}

    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not _should_skip_dir(d)]
        root_path = Path(root)
        if output_real:
            try:
                if Path(os.path.realpath(root_path)).is_relative_to(output_real):
                    continue
            except (ValueError, AttributeError):
                if str(root_path).startswith(str(output_real)):
                    continue

        for name in files:
            p = root_path / name
            if _should_skip_file(p):
                if include_raw and p.suffix.lower() in raw_ext:
                    yield p
                continue
            yield p


def md5_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def probe_integrity(path: Path) -> bool:
    if is_likely_placeholder(path):
        return False
    try:
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


def scan_directory(
    source_dir: Path,
    output_dir: Optional[Path] = None,
    include_raw: bool = False,
) -> List[ScannedFile]:
    seen_md5: Set[str] = set()
    results: List[ScannedFile] = []

    for path in iter_image_paths(source_dir, output_dir, include_raw=include_raw):
        path = Path(os.path.realpath(path))
        try:
            st = path.stat()
        except OSError as exc:
            logger.warning("stat failed %s: %s", path, exc)
            continue

        corrupt = not probe_integrity(path)
        skip_reason = None
        file_md5 = ""
        if not corrupt:
            try:
                file_md5 = md5_file(path)
            except OSError as exc:
                corrupt = True
                skip_reason = str(exc)

        if corrupt:
            results.append(
                ScannedFile(path=path, md5="", size=st.st_size, mtime=st.st_mtime, corrupt=True, skip_reason=skip_reason)
            )
            continue

        if file_md5 in seen_md5:
            results.append(
                ScannedFile(
                    path=path,
                    md5=file_md5,
                    size=st.st_size,
                    mtime=st.st_mtime,
                    corrupt=False,
                    skip_reason="md5_duplicate",
                )
            )
            continue

        seen_md5.add(file_md5)
        results.append(
            ScannedFile(path=path, md5=file_md5, size=st.st_size, mtime=st.st_mtime, corrupt=False)
        )

    return results
