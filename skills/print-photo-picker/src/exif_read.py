"""EXIF DateTimeOriginal, GPS, Orientation via piexif."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import piexif


@dataclass
class ExifInfo:
    datetime_original: Optional[datetime]
    gps_lat: Optional[float]
    gps_lon: Optional[float]
    orientation: int = 1


def _ratio_to_float(r) -> float:
    try:
        return float(r[0]) / float(r[1])
    except Exception:
        return float(r)


def _gps_to_deg(values, ref: str) -> float:
    d = _ratio_to_float(values[0])
    m = _ratio_to_float(values[1])
    s = _ratio_to_float(values[2])
    deg = d + m / 60.0 + s / 3600.0
    if ref in ("S", "W"):
        deg = -deg
    return deg


def read_exif(path: Path) -> ExifInfo:
    path = Path(os.path.realpath(path))
    orientation = 1
    dt: Optional[datetime] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    try:
        exif_dict = piexif.load(str(path))
    except Exception:
        return ExifInfo(None, None, None, orientation)

    try:
        if piexif.ImageIFD.Orientation in exif_dict.get("0th", {}):
            orientation = int(exif_dict["0th"][piexif.ImageIFD.Orientation])
    except Exception:
        pass

    try:
        exif_ifd = exif_dict.get("Exif", {})
        raw_dt = exif_ifd.get(piexif.ExifIFD.DateTimeOriginal) or exif_ifd.get(piexif.ExifIFD.DateTimeDigitized)
        if raw_dt:
            if isinstance(raw_dt, bytes):
                raw_dt = raw_dt.decode("utf-8", errors="ignore")
            dt = datetime.strptime(raw_dt, "%Y:%m:%d %H:%M:%S")
    except Exception:
        dt = None

    try:
        gps = exif_dict.get("GPS", {})
        if gps:
            lat = _gps_to_deg(gps[piexif.GPSIFD.GPSLatitude], gps[piexif.GPSIFD.GPSLatitudeRef].decode())
            lon = _gps_to_deg(gps[piexif.GPSIFD.GPSLongitude], gps[piexif.GPSIFD.GPSLongitudeRef].decode())
    except Exception:
        lat, lon = None, None

    return ExifInfo(dt, lat, lon, orientation)
