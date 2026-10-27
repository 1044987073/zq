"""Reference face embedding + subject match (HANDOFF §7 Step 3)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

import numpy as np

from .constants import DEFAULT_BLUR_LAPLACIAN_MIN, DEFAULT_BLUR_SCORE_MIN, DEFAULT_EAR_MIN
from .face_metrics import cosine_similarity, normalize_embedding
from .index_worker import index_single_image


@dataclass
class RefFaceResult:
    embedding: np.ndarray
    warnings: List[str]


@dataclass
class MatchResult:
    abs_path: str
    subject_sim: float
    subject_face_index: Optional[int]
    ambiguous: bool = False


def build_reference_embedding(
    ref_paths: Sequence[Path],
    face_threshold: float,
    blur_laplacian_min: float = DEFAULT_BLUR_LAPLACIAN_MIN,
    blur_score_min: float = DEFAULT_BLUR_SCORE_MIN,
    ear_min: float = DEFAULT_EAR_MIN,
) -> RefFaceResult:
    warnings: List[str] = []
    embs: List[np.ndarray] = []

    for p in ref_paths:
        payload = index_single_image(str(p))
        if payload.get("error"):
            raise ValueError(f"参考图无法读取: {p} ({payload['error']})")
        faces = payload.get("faces") or []
        if not faces:
            raise ValueError(f"参考图未检测到人脸: {p}")

        best = max(faces, key=lambda f: f.get("det_score", 0))
        if best.get("laplacian_face", 0) < blur_laplacian_min:
            raise ValueError(f"参考图主体过糊，请换更清晰的照片: {p}")
        bs = best.get("blur_score")
        if bs is not None and bs < blur_score_min:
            raise ValueError(f"参考图 blur_score 过低: {p}")
        if best.get("ear", 0) < ear_min:
            warnings.append(f"参考图可能闭眼/半闭眼: {p}")

        emb = best.get("embedding")
        if emb is None:
            raise ValueError(f"参考图 embedding 失败: {p}")
        embs.append(normalize_embedding(np.array(emb, dtype=np.float64)))

    mean_emb = normalize_embedding(np.mean(np.stack(embs, axis=0), axis=0))
    return RefFaceResult(embedding=mean_emb, warnings=warnings)


def match_subject(
    faces: List[dict],
    ref_emb: np.ndarray,
    face_threshold: float,
    twin_gap: float = 0.03,
) -> MatchResult:
    if not faces:
        return MatchResult(abs_path="", subject_sim=0.0, subject_face_index=None)

    sims = []
    for i, f in enumerate(faces):
        emb = f.get("embedding")
        if emb is None:
            sims.append((i, 0.0))
            continue
        sims.append((i, cosine_similarity(np.array(emb), ref_emb)))

    sims.sort(key=lambda x: x[1], reverse=True)
    best_i, best_sim = sims[0]
    ambiguous = False
    if len(sims) > 1 and best_sim >= face_threshold:
        second_sim = sims[1][1]
        if second_sim >= face_threshold and (best_sim - second_sim) < twin_gap:
            ambiguous = True

    if best_sim < face_threshold:
        return MatchResult(abs_path="", subject_sim=best_sim, subject_face_index=None, ambiguous=ambiguous)

    return MatchResult(
        abs_path="",
        subject_sim=best_sim,
        subject_face_index=best_i,
        ambiguous=ambiguous,
    )
