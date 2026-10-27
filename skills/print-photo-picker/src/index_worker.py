"""InsightFace worker (one FaceAnalysis per process — HANDOFF §8.4)."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import cv2
import imagehash
import numpy as np
from PIL import Image

from .exif_read import read_exif
from .face_metrics import (
    exposure_stats_rgb,
    eye_aspect_ratio_106,
    laplacian_variance_bgr,
    laplacian_variance_crop,
)
from .image_io import load_rgb_array

logger = logging.getLogger(__name__)

_FACE_APP = None


def init_face_app(model_name: str = "buffalo_l") -> None:
    global _FACE_APP
    if _FACE_APP is not None:
        return
    from insightface.app import FaceAnalysis

    providers = ["CPUExecutionProvider"]
    try:
        import onnxruntime as ort

        if "CoreMLExecutionProvider" in ort.get_available_providers():
            providers = ["CoreMLExecutionProvider", "CPUExecutionProvider"]
    except Exception:
        pass

    app = FaceAnalysis(name=model_name, providers=providers)
    app.prepare(ctx_id=0, det_size=(640, 640))
    _FACE_APP = app


def _face_to_dict(face, img_bgr: np.ndarray, img_area: int) -> Dict[str, Any]:
    bbox = face.bbox.astype(float).tolist()
    emb = face.embedding.astype(float).tolist() if face.embedding is not None else None
    lmk = face.landmark_2d_106.astype(float) if getattr(face, "landmark_2d_106", None) is not None else None
    ear = eye_aspect_ratio_106(lmk) if lmk is not None else 0.0
    lap_face = laplacian_variance_crop(img_bgr, face.bbox)

    blur_score = None
    if hasattr(face, "blur") and face.blur is not None:
        blur_score = float(face.blur)
    elif hasattr(face, "face_quality") and face.face_quality is not None:
        fq = face.face_quality
        if isinstance(fq, dict):
            blur_score = float(fq.get("blur_score", fq.get("blur", 0)))
        else:
            blur_score = float(getattr(fq, "blur_score", getattr(fq, "blur", 0)))

    pose = getattr(face, "pose", None)
    yaw = pitch = roll = 0.0
    if pose is not None:
        if isinstance(pose, (list, tuple, np.ndarray)) and len(pose) >= 3:
            yaw, pitch, roll = float(pose[0]), float(pose[1]), float(pose[2])
        else:
            yaw = float(getattr(pose, "yaw", 0))
            pitch = float(getattr(pose, "pitch", 0))
            roll = float(getattr(pose, "roll", 0))

    x1, y1, x2, y2 = bbox[:4]
    face_area = max(0.0, (x2 - x1) * (y2 - y1))
    return {
        "bbox": bbox,
        "embedding": emb,
        "ear": ear,
        "laplacian_face": lap_face,
        "blur_score": blur_score,
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll,
        "face_area_ratio": face_area / max(img_area, 1),
        "det_score": float(getattr(face, "det_score", 0.0)),
    }


def index_single_image(path_str: str, model_name: str = "buffalo_l") -> Dict[str, Any]:
    init_face_app(model_name)
    path = path_str
    rgb, err = load_rgb_array(__import__("pathlib").Path(path))
    if rgb is None:
        return {"abs_path": path, "error": err or "load_failed", "faces": []}

    exif = read_exif(__import__("pathlib").Path(path))
    img_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    gray_mean, hi, sh = exposure_stats_rgb(rgb)
    lap_full = laplacian_variance_bgr(img_bgr)
    ph = str(imagehash.phash(Image.fromarray(rgb)))

    faces_out: List[Dict[str, Any]] = []
    if _FACE_APP is not None:
        detected = _FACE_APP.get(img_bgr)
        img_area = rgb.shape[0] * rgb.shape[1]
        for face in detected:
            faces_out.append(_face_to_dict(face, img_bgr, img_area))

    return {
        "abs_path": path,
        "exif_datetime": exif.datetime_original.isoformat() if exif.datetime_original else None,
        "exif_gps_lat": exif.gps_lat,
        "exif_gps_lon": exif.gps_lon,
        "phash": ph,
        "gray_mean": gray_mean,
        "highlight_ratio": hi,
        "shadow_ratio": sh,
        "laplacian_full": lap_full,
        "faces": faces_out,
        "error": None,
    }
