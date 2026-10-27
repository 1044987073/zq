"""Face geometry metrics: EAR, blur on crop, normalization helpers."""

from __future__ import annotations

import math
from typing import Iterable, List, Sequence

import cv2
import numpy as np


# WFLW 106-point eye regions (InsightFace buffalo_l landmark_2d_106)
LEFT_EYE_IDX = (60, 61, 62, 63, 64, 65, 66, 67)
RIGHT_EYE_IDX = (68, 69, 70, 71, 72, 73, 74, 75)


def _dist(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def eye_aspect_ratio_106(landmarks: np.ndarray) -> float:
    """Average EAR of both eyes from 106 landmarks."""
    def ear(indices: Sequence[int]) -> float:
        pts = [landmarks[i] for i in indices]
        # vertical pairs + horizontal
        v1 = _dist(pts[1], pts[5])
        v2 = _dist(pts[2], pts[4])
        h = _dist(pts[0], pts[3])
        if h <= 1e-6:
            return 0.0
        return (v1 + v2) / (2.0 * h)

    left = ear(LEFT_EYE_IDX[:6]) if len(LEFT_EYE_IDX) >= 6 else ear(LEFT_EYE_IDX)
    right = ear(RIGHT_EYE_IDX[:6]) if len(RIGHT_EYE_IDX) >= 6 else ear(RIGHT_EYE_IDX)
    return (left + right) / 2.0


def laplacian_variance_bgr(img_bgr: np.ndarray) -> float:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def laplacian_variance_crop(img_bgr: np.ndarray, bbox: np.ndarray) -> float:
    x1, y1, x2, y2 = [int(v) for v in bbox[:4]]
    h, w = img_bgr.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return 0.0
    crop = img_bgr[y1:y2, x1:x2]
    return laplacian_variance_bgr(crop)


def exposure_stats_rgb(img_rgb: np.ndarray) -> tuple[float, float, float]:
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    mean = float(np.mean(gray))
    total = gray.size
    highlight = float(np.sum(gray > 250)) / total
    shadow = float(np.sum(gray < 15)) / total
    return mean, highlight, shadow


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na < 1e-9 or nb < 1e-9:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def normalize_embedding(emb: np.ndarray) -> np.ndarray:
    emb = emb.astype(np.float64)
    n = np.linalg.norm(emb)
    if n < 1e-9:
        return emb
    return emb / n


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def norm_blur(laplacian_face: float, lap_min: float = 60.0, lap_max: float = 300.0) -> float:
    return clamp01((laplacian_face - lap_min) / max(lap_max - lap_min, 1e-6))


def norm_exposure(mean: float, low: float = 50.0, high: float = 220.0) -> float:
    mid = (low + high) / 2.0
    half = (high - low) / 2.0
    return clamp01(1.0 - abs(mean - mid) / half)


def norm_eye(ear: float, ear_min: float = 0.21, ear_max: float = 0.35) -> float:
    return clamp01((ear - ear_min) / max(ear_max - ear_min, 1e-6))


def norm_face_area(ratio: float, cap: float = 0.25) -> float:
    return clamp01(ratio / cap)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
