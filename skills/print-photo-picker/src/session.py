"""Session clustering + Top-1 scoring (HANDOFF §4)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import imagehash

from .constants import (
    DEFAULT_NEAR_TOP_SCORE_DELTA,
    DEFAULT_PHASH_HAMMING_MAX,
    DEFAULT_SESSION_RADIUS_M,
    DEFAULT_SESSION_WINDOW_MINUTES,
    SCORE_WEIGHTS,
)
from .face_metrics import (
    haversine_m,
    norm_blur,
    norm_exposure,
    norm_eye,
    norm_face_area,
)


@dataclass
class ImageDecision:
    abs_path: str
    quality_label: str
    session_id: Optional[str] = None
    session_score: float = 0.0
    disposition: str = "pending"  # qualified | duplicate | cleanup | stay
    cleanup_subdir: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    record: Dict = field(default_factory=dict)
    subject_sim: float = 0.0
    ambiguous_match: bool = False


def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def phash_distance(a: str, b: str) -> int:
    try:
        return imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b)
    except Exception:
        return 999


def compute_session_score(record: dict, subject_face: dict) -> float:
    lap = subject_face.get("laplacian_face", 0.0)
    ear = subject_face.get("ear", 0.0)
    mean = record.get("gray_mean", 128.0)
    area = subject_face.get("face_area_ratio", 0.0)
    s = (
        SCORE_WEIGHTS["blur"] * norm_blur(lap)
        + SCORE_WEIGHTS["exposure"] * norm_exposure(mean)
        + SCORE_WEIGHTS["eye_open"] * norm_eye(ear)
        + SCORE_WEIGHTS["face_area"] * norm_face_area(area)
    )
    return float(s)


def _can_merge(
    a: ImageDecision,
    b: ImageDecision,
    window_min: int,
    radius_m: float,
    phash_max: int,
) -> bool:
    ra, rb = a.record, b.record
    dt_a = _parse_dt(ra.get("exif_datetime")) or datetime.fromtimestamp(
        Path(a.abs_path).stat().st_mtime
    )
    dt_b = _parse_dt(rb.get("exif_datetime")) or datetime.fromtimestamp(
        Path(b.abs_path).stat().st_mtime
    )
    if abs((dt_a - dt_b).total_seconds()) > window_min * 60:
        return False

    lat_a, lon_a = ra.get("exif_gps_lat"), ra.get("exif_gps_lon")
    lat_b, lon_b = rb.get("exif_gps_lat"), rb.get("exif_gps_lon")

    if lat_a is not None and lon_a is not None and lat_b is not None and lon_b is not None:
        return haversine_m(lat_a, lon_a, lat_b, lon_b) <= radius_m

    if ra.get("exif_datetime") and rb.get("exif_datetime"):
        dir_a = str(Path(a.abs_path).parent)
        dir_b = str(Path(b.abs_path).parent)
        if dir_a != dir_b:
            return False
        pa, pb = ra.get("phash"), rb.get("phash")
        if not pa or not pb:
            return False
        return phash_distance(pa, pb) <= phash_max

    # Tier 3: no EXIF datetime in record — mtime + phash + same dir
    dir_a = str(Path(a.abs_path).parent)
    dir_b = str(Path(b.abs_path).parent)
    if dir_a != dir_b:
        return False
    try:
        mt_a = Path(a.abs_path).stat().st_mtime
        mt_b = Path(b.abs_path).stat().st_mtime
    except OSError:
        return False
    if abs(mt_a - mt_b) > window_min * 60:
        return False
    pa, pb = ra.get("phash"), rb.get("phash")
    if not pa or not pb:
        return False
    return phash_distance(pa, pb) <= phash_max


def cluster_sessions(
    pass_items: List[ImageDecision],
    window_min: int = DEFAULT_SESSION_WINDOW_MINUTES,
    radius_m: float = DEFAULT_SESSION_RADIUS_M,
    phash_max: int = DEFAULT_PHASH_HAMMING_MAX,
    near_delta: float = DEFAULT_NEAR_TOP_SCORE_DELTA,
) -> List[ImageDecision]:
    if not pass_items:
        return pass_items

    for item in pass_items:
        sf = item.record.get("subject_face") or {}
        item.session_score = compute_session_score(item.record, sf)

    # Union-find style greedy clustering
    n = len(pass_items)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            if _can_merge(pass_items[i], pass_items[j], window_min, radius_m, phash_max):
                union(i, j)

    groups: Dict[int, List[int]] = {}
    for i in range(n):
        r = find(i)
        groups.setdefault(r, []).append(i)

    sid = 0
    for _, idxs in groups.items():
        sid += 1
        session_id = f"session_{sid:04d}"
        members = [pass_items[i] for i in idxs]
        members.sort(key=lambda m: m.session_score, reverse=True)
        top1 = members[0]
        top1.session_id = session_id
        top1.disposition = "qualified"
        top1.tags = []
        if top1.ambiguous_match:
            top1.tags.append("匹配歧义·复核")

        for rank, m in enumerate(members[1:], start=2):
            m.session_id = session_id
            delta = top1.session_score - m.session_score
            if delta < near_delta:
                m.disposition = "qualified"
                m.tags.append("次优·可复核")
            else:
                m.disposition = "duplicate"
                m.cleanup_subdir = "重复"

        if len(members) == 1 and members[0].ambiguous_match:
            members[0].tags.append("单张session·匹配歧义")

    return pass_items
