"""Incremental sqlite index + optional ProcessPoolExecutor (HANDOFF §7 Step 2)."""

from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .db import IndexDatabase
from .index_worker import index_single_image
from .scan import ScannedFile

logger = logging.getLogger(__name__)


@dataclass
class IndexedImage:
    abs_path: str
    file_mtime: float
    file_size: int
    md5: str
    from_cache: bool
    record: Dict[str, Any]


def _row_to_record(row) -> Dict[str, Any]:
    return {
        "abs_path": row.abs_path,
        "exif_datetime": row.exif_datetime,
        "exif_gps_lat": row.exif_gps_lat,
        "exif_gps_lon": row.exif_gps_lon,
        "phash": row.phash,
        "gray_mean": row.gray_mean,
        "highlight_ratio": row.highlight_ratio,
        "shadow_ratio": row.shadow_ratio,
        "laplacian_full": row.laplacian_full,
        "faces": row.faces_json or [],
        "error": row.error,
    }


def index_files(
    scanned: List[ScannedFile],
    db_path: Path,
    workers: int = 1,
    model_name: str = "buffalo_l",
) -> tuple[List[IndexedImage], float]:
    db = IndexDatabase(db_path)
    t0 = time.perf_counter()
    to_index: List[ScannedFile] = []
    cached_records: List[IndexedImage] = []

    for sf in scanned:
        if sf.corrupt or sf.skip_reason:
            continue
        abs_path = str(sf.path)
        cached = db.get_cached(abs_path, sf.mtime, sf.size)
        if cached and not cached.error:
            cached_records.append(
                IndexedImage(
                    abs_path=abs_path,
                    file_mtime=sf.mtime,
                    file_size=sf.size,
                    md5=sf.md5,
                    from_cache=True,
                    record=_row_to_record(cached),
                )
            )
            continue
        to_index.append(sf)

    new_records: List[IndexedImage] = []
    if to_index:
        if workers > 1:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = {
                    pool.submit(index_single_image, str(sf.path), model_name): sf for sf in to_index
                }
                for fut in as_completed(futures):
                    sf = futures[fut]
                    try:
                        payload = fut.result()
                    except Exception as exc:
                        payload = {"abs_path": str(sf.path), "error": str(exc), "faces": []}
                    new_records.append(_persist_index(db, sf, payload))
        else:
            for sf in to_index:
                payload = index_single_image(str(sf.path), model_name)
                new_records.append(_persist_index(db, sf, payload))

    elapsed = time.perf_counter() - t0
    return cached_records + new_records, elapsed


def _persist_index(db: IndexDatabase, sf: ScannedFile, payload: Dict[str, Any]) -> IndexedImage:
    from .db import make_cache_key

    row = {
        "abs_path": str(sf.path),
        "file_mtime": sf.mtime,
        "file_size": sf.size,
        "cache_key": make_cache_key(str(sf.path), sf.mtime, sf.size),
        "md5": sf.md5,
        "exif_datetime": payload.get("exif_datetime"),
        "exif_gps_lat": payload.get("exif_gps_lat"),
        "exif_gps_lon": payload.get("exif_gps_lon"),
        "phash": payload.get("phash"),
        "gray_mean": payload.get("gray_mean"),
        "highlight_ratio": payload.get("highlight_ratio"),
        "shadow_ratio": payload.get("shadow_ratio"),
        "laplacian_full": payload.get("laplacian_full"),
        "faces_json": payload.get("faces") or [],
        "error": payload.get("error"),
    }
    db.upsert(row)
    return IndexedImage(
        abs_path=str(sf.path),
        file_mtime=sf.mtime,
        file_size=sf.size,
        md5=sf.md5,
        from_cache=False,
        record=payload,
    )
