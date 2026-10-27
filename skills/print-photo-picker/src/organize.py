"""Copy/move into output tree — no hard delete (HANDOFF §5–§7)."""

from __future__ import annotations

import json
import logging
import os
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import List

from .session import ImageDecision

logger = logging.getLogger(__name__)

LABEL_TO_SUBDIR = {
    "blur": "模糊",
    "eyes_closed": "闭眼",
    "pose_bad": "侧脸",
    "exposure_bad": "曝光",
    "no_match": "无匹配",
    "duplicate": "重复",
}


def _unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    parent = dest.parent
    for i in range(1, 10000):
        candidate = parent / f"{stem}__dup{i}{suffix}"
        if not candidate.exists():
            return candidate
    return dest


def organize_files(
    output_dir: Path,
    decisions: List[ImageDecision],
    apply: bool,
) -> List[dict]:
    output_dir = Path(os.path.realpath(output_dir))
    qualified_root = output_dir / "合格"
    cleanup_root = output_dir / "待清理"
    actions: List[dict] = []

    for d in decisions:
        src = Path(d.abs_path)
        if d.disposition == "stay" or d.quality_label == "no_match":
            actions.append({"op": "skip", "src": str(src), "reason": "no_match_stay_in_place"})
            continue
        if d.disposition == "qualified":
            dest = _unique_dest(qualified_root / src.name)
            action = {"op": "copy", "src": str(src), "dest": str(dest), "tags": d.tags}
            if apply:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            actions.append(action)
            continue
        if d.disposition == "duplicate":
            sub = d.cleanup_subdir or "重复"
        else:
            sub = d.cleanup_subdir or LABEL_TO_SUBDIR.get(d.quality_label, "无匹配")
        dest = _unique_dest(cleanup_root / sub / src.name)
        action = {
            "op": "move",
            "src": str(src),
            "dest": str(dest),
            "label": d.quality_label,
            "tags": d.tags,
        }
        if apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
        actions.append(action)

    return actions


def write_report(output_dir: Path, payload: dict) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def write_review_html(output_dir: Path, template_path: Path, report: dict) -> Path:
    html = template_path.read_text(encoding="utf-8")
    data_json = json.dumps(report, ensure_ascii=False)
    html = html.replace("/*__REPORT_JSON__*/", data_json)
    out = output_dir / "review.html"
    out.write_text(html, encoding="utf-8")
    return out
