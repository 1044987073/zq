#!/usr/bin/env python3
"""Synthetic mixed test set for pipeline smoke / scale (≥500 files)."""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def make_image(path: Path, kind: str, seed: int) -> None:
    rng = random.Random(seed)
    w, h = 640, 480
    if kind == "dark":
        arr = np.full((h, w, 3), 20, dtype=np.uint8)
    elif kind == "bright":
        arr = np.full((h, w, 3), 245, dtype=np.uint8)
    elif kind == "blur":
        arr = np.random.default_rng(seed).integers(80, 181, (h, w, 3), dtype=np.uint8)
    else:
        arr = np.random.default_rng(seed).integers(40, 201, (h, w, 3), dtype=np.uint8)

    img = Image.fromarray(arr)
    if kind == "blur":
        img = img.filter(ImageFilter.GaussianBlur(radius=6))
    draw = ImageDraw.Draw(img)
    # simple oval "face" region — not a real face; for scan/index stress only
    cx, cy = w // 2 + rng.randint(-40, 40), h // 2 + rng.randint(-30, 30)
    draw.ellipse((cx - 60, cy - 80, cx + 60, cy + 80), fill=(220, 180, 160))
    img.save(path, quality=85)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--count", type=int, default=520)
    args = ap.parse_args()
    root = args.out
    root.mkdir(parents=True, exist_ok=True)
    kinds = ["normal", "dark", "bright", "blur", "burst"] * 20
    base_t = datetime(2024, 8, 15, 10, 0, 0)
    for i in range(args.count):
        k = kinds[i % len(kinds)]
        sub = root / ("burst" if k == "burst" else k)
        sub.mkdir(exist_ok=True)
        ext = ".jpg" if i % 17 else ".png"
        if i % 53 == 0:
            ext = ".webp"
        path = sub / f"img_{i:04d}{ext}"
        make_image(path, "blur" if k == "blur" else ("dark" if k == "dark" else "bright" if k == "bright" else "normal"), i)
        if k == "burst":
            # same mtime window for burst folder
            ts = (base_t + timedelta(seconds=i % 120)).timestamp()
            path.touch()
            import os

            os.utime(path, (ts, ts))
    print(f"Wrote {args.count} images under {root}")


if __name__ == "__main__":
    main()
