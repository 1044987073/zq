#!/usr/bin/env python3
"""Build a mixed demo album from InsightFace samples + augmentations (unique MD5)."""

from __future__ import annotations

import argparse
import io
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import piexif
from PIL import Image, ImageEnhance, ImageFilter


def _jpeg_bytes(img: Image.Image, q: int) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=q)
    return buf.getvalue()


def _write_with_exif(path: Path, img: Image.Image, dt: datetime, quality: int) -> None:
    exif_dict = {
        "0th": {},
        "Exif": {piexif.ExifIFD.DateTimeOriginal: dt.strftime("%Y:%m:%d %H:%M:%S").encode()},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="JPEG", quality=quality, exif=exif_bytes)


def augment(img: Image.Image, seed: int, kind: str) -> Image.Image:
    rng = random.Random(seed)
    out = img.copy()
    if kind == "blur":
        out = out.filter(ImageFilter.GaussianBlur(radius=rng.uniform(2, 5)))
    elif kind == "dark":
        out = ImageEnhance.Brightness(out).enhance(rng.uniform(0.15, 0.35))
    elif kind == "bright":
        out = ImageEnhance.Brightness(out).enhance(rng.uniform(1.6, 2.0))
    elif kind == "burst":
        out = ImageEnhance.Brightness(out).enhance(rng.uniform(0.9, 1.1))
        out = out.rotate(rng.uniform(-3, 3), fillcolor=(128, 128, 128))
    else:
        out = ImageEnhance.Contrast(out).enhance(rng.uniform(0.85, 1.15))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--count", type=int, default=520)
    ap.add_argument("--samples-dir", type=Path, required=True)
    args = ap.parse_args()

    samples = [p for p in args.samples_dir.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    if not samples:
        raise SystemExit("no sample images")
    subject = next((p for p in samples if p.name == "t1.jpg"), samples[0])
    other = next((p for p in samples if "Tom" in p.name or "tom" in p.name.lower()), samples[-1])

    base_t = datetime(2024, 8, 15, 14, 30, 0)
    kinds = ["normal", "burst", "blur", "dark", "bright", "other_face"]
    out = args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    i = 0
    while i < args.count:
        kind = kinds[i % len(kinds)]
        src = other if kind == "other_face" else subject
        img = Image.open(src).convert("RGB")
        aug = augment(img, i, kind)
        sub = out / ("session_a" if i < args.count // 2 else "session_b")
        dt = base_t + timedelta(seconds=(i % 120) if kind == "burst" else i * 37)
        q = 70 + (i % 25)
        path = sub / f"photo_{i:04d}_{kind}.jpg"
        _write_with_exif(path, aug, dt, q)
        i += 1

    print(f"Built {args.count} unique JPEGs under {out}")


if __name__ == "__main__":
    main()
