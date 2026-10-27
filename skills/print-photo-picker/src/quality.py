"""Quality gate — HANDOFF §3 five rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .constants import (
    DEFAULT_BLUR_LAPLACIAN_MIN,
    DEFAULT_BLUR_SCORE_MIN,
    DEFAULT_EAR_MIN,
    DEFAULT_EXPOSURE_MEAN_MAX,
    DEFAULT_EXPOSURE_MEAN_MIN,
    DEFAULT_HIGHLIGHT_RATIO_MAX,
    DEFAULT_PITCH_MAX,
    DEFAULT_SHADOW_RATIO_MAX,
    DEFAULT_YAW_MAX,
)


@dataclass
class QualityResult:
    label: str  # pass | blur | eyes_closed | pose_bad | exposure_bad | no_match
    reasons: List[str]
    subject_face: Optional[dict]


def evaluate_quality(
    faces: List[dict],
    subject_idx: Optional[int],
    gray_mean: float,
    highlight_ratio: float,
    shadow_ratio: float,
    face_threshold: float,
    subject_sim: float,
    blur_laplacian_min: float = DEFAULT_BLUR_LAPLACIAN_MIN,
    blur_score_min: float = DEFAULT_BLUR_SCORE_MIN,
    ear_min: float = DEFAULT_EAR_MIN,
    yaw_max: float = DEFAULT_YAW_MAX,
    pitch_max: float = DEFAULT_PITCH_MAX,
    exposure_mean_min: float = DEFAULT_EXPOSURE_MEAN_MIN,
    exposure_mean_max: float = DEFAULT_EXPOSURE_MEAN_MAX,
    highlight_max: float = DEFAULT_HIGHLIGHT_RATIO_MAX,
    shadow_max: float = DEFAULT_SHADOW_RATIO_MAX,
) -> QualityResult:
    if subject_idx is None or subject_sim < face_threshold:
        return QualityResult(label="no_match", reasons=["face_sim_below_threshold"], subject_face=None)

    face = faces[subject_idx]
    reasons: List[str] = []

    bs = face.get("blur_score")
    lap = face.get("laplacian_face", 0.0)
    blur_fail = lap < blur_laplacian_min
    if bs is not None:
        blur_fail = blur_fail or bs < blur_score_min
    if blur_fail:
        reasons.append("blur")

    if face.get("ear", 0.0) < ear_min:
        reasons.append("eyes_closed")

    if abs(face.get("yaw", 0.0)) > yaw_max or abs(face.get("pitch", 0.0)) > pitch_max:
        reasons.append("pose_bad")

    exp_bad = (
        gray_mean < exposure_mean_min
        or gray_mean > exposure_mean_max
        or highlight_ratio > highlight_max
        or shadow_ratio > shadow_max
    )
    if exp_bad:
        reasons.append("exposure_bad")

    if not reasons:
        return QualityResult(label="pass", reasons=[], subject_face=face)

    # Primary label for folder routing (first failing category priority)
    priority = ["blur", "eyes_closed", "pose_bad", "exposure_bad"]
    for p in priority:
        if p in reasons:
            return QualityResult(label=p, reasons=reasons, subject_face=face)

    return QualityResult(label="no_match", reasons=reasons, subject_face=face)
