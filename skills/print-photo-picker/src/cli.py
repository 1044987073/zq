"""CLI entry — default dry-run; --apply writes files."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import List, Optional

import typer

from . import __version__
from .constants import (
    DEFAULT_BLUR_LAPLACIAN_MIN,
    DEFAULT_BLUR_SCORE_MIN,
    DEFAULT_EAR_MIN,
    DEFAULT_EXPOSURE_MEAN_MAX,
    DEFAULT_EXPOSURE_MEAN_MIN,
    DEFAULT_FACE_SIM_THRESHOLD,
    DEFAULT_HIGHLIGHT_RATIO_MAX,
    DEFAULT_NEAR_TOP_SCORE_DELTA,
    DEFAULT_PHASH_HAMMING_MAX,
    DEFAULT_PITCH_MAX,
    DEFAULT_SESSION_RADIUS_M,
    DEFAULT_SESSION_WINDOW_MINUTES,
    DEFAULT_SHADOW_RATIO_MAX,
    DEFAULT_YAW_MAX,
)
from .index import index_files
from .match import build_reference_embedding, match_subject
from .organize import organize_files, write_report, write_review_html
from .quality import evaluate_quality
from .scan import scan_directory
from .session import ImageDecision, cluster_sessions

app = typer.Typer(add_completion=False, help="打印照片人脸筛选 + 质量清理 (Phase 1)")
logger = logging.getLogger("print_photo_picker")


@app.command()
def run(
    source_dir: Path = typer.Argument(..., help="相册根目录"),
    ref_faces: List[Path] = typer.Option(..., "--ref-face", help="参考人脸图，可重复传入 1~3 张"),
    output_dir: Path = typer.Option(..., "--output", help="输出根目录"),
    apply: bool = typer.Option(False, "--apply", help="实际复制/移动；默认 dry-run"),
    face_threshold: float = typer.Option(DEFAULT_FACE_SIM_THRESHOLD, "--face-threshold"),
    blur_laplacian_min: float = typer.Option(DEFAULT_BLUR_LAPLACIAN_MIN, "--blur-laplacian-min"),
    blur_score_min: float = typer.Option(DEFAULT_BLUR_SCORE_MIN, "--blur-score-min"),
    ear_min: float = typer.Option(DEFAULT_EAR_MIN, "--ear-min"),
    yaw_max: float = typer.Option(DEFAULT_YAW_MAX, "--yaw-max"),
    pitch_max: float = typer.Option(DEFAULT_PITCH_MAX, "--pitch-max"),
    exposure_mean_min: float = typer.Option(DEFAULT_EXPOSURE_MEAN_MIN, "--exposure-mean-min"),
    exposure_mean_max: float = typer.Option(DEFAULT_EXPOSURE_MEAN_MAX, "--exposure-mean-max"),
    highlight_max: float = typer.Option(DEFAULT_HIGHLIGHT_RATIO_MAX, "--highlight-ratio-max"),
    shadow_max: float = typer.Option(DEFAULT_SHADOW_RATIO_MAX, "--shadow-ratio-max"),
    session_window: int = typer.Option(DEFAULT_SESSION_WINDOW_MINUTES, "--session-window"),
    session_radius: float = typer.Option(DEFAULT_SESSION_RADIUS_M, "--session-radius"),
    phash_hamming_max: int = typer.Option(DEFAULT_PHASH_HAMMING_MAX, "--phash-hamming-max"),
    near_top_delta: float = typer.Option(DEFAULT_NEAR_TOP_SCORE_DELTA, "--near-top-delta"),
    workers: int = typer.Option(1, "--workers", help="索引并发 worker 数 (InsightFace 每 worker 独立实例)"),
    db_path: Optional[Path] = typer.Option(None, "--db-path", help="sqlite 索引路径，默认 output/face_index.db"),
    include_raw: bool = typer.Option(False, "--include-raw"),
    verbose: bool = typer.Option(False, "--verbose"),
) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    if not ref_faces:
        typer.echo("至少提供一张 --ref-face", err=True)
        raise typer.Exit(2)

    output_dir = output_dir.expanduser().resolve()
    source_dir = source_dir.expanduser().resolve()
    db_path = (db_path or output_dir / "face_index.db").expanduser().resolve()
    template = Path(__file__).parent.parent / "templates" / "review.html"

    t_all = time.perf_counter()
    ref = build_reference_embedding(
        ref_faces,
        face_threshold=face_threshold,
        blur_laplacian_min=blur_laplacian_min,
        blur_score_min=blur_score_min,
        ear_min=ear_min,
    )
    for w in ref.warnings:
        logger.warning(w)

    scanned = scan_directory(source_dir, output_dir=output_dir, include_raw=include_raw)
    indexed, index_elapsed = index_files(scanned, db_path=db_path, workers=workers)

    decisions: List[ImageDecision] = []
    ambiguous_samples: List[dict] = []

    for item in indexed:
        rec = item.record
        faces = rec.get("faces") or []
        m = match_subject(faces, ref.embedding, face_threshold)
        m.abs_path = item.abs_path
        q = evaluate_quality(
            faces=faces,
            subject_idx=m.subject_face_index,
            gray_mean=rec.get("gray_mean") or 128.0,
            highlight_ratio=rec.get("highlight_ratio") or 0.0,
            shadow_ratio=rec.get("shadow_ratio") or 0.0,
            face_threshold=face_threshold,
            subject_sim=m.subject_sim,
            blur_laplacian_min=blur_laplacian_min,
            blur_score_min=blur_score_min,
            ear_min=ear_min,
            yaw_max=yaw_max,
            pitch_max=pitch_max,
            exposure_mean_min=exposure_mean_min,
            exposure_mean_max=exposure_mean_max,
            highlight_max=highlight_max,
            shadow_max=shadow_max,
        )
        rec_out = dict(rec)
        rec_out["subject_face"] = q.subject_face
        dec = ImageDecision(
            abs_path=item.abs_path,
            quality_label=q.label,
            record=rec_out,
            subject_sim=m.subject_sim,
            ambiguous_match=m.ambiguous,
        )
        if m.ambiguous:
            ambiguous_samples.append({"path": item.abs_path, "reason": "twin_or_multi_high_sim"})
        if q.label != "pass":
            if q.label == "no_match":
                dec.disposition = "stay"
            else:
                dec.disposition = "cleanup"
        decisions.append(dec)

    pass_items = [d for d in decisions if d.quality_label == "pass"]
    cluster_sessions(
        pass_items,
        window_min=session_window,
        radius_m=session_radius,
        phash_max=phash_hamming_max,
        near_delta=near_top_delta,
    )

    actions = organize_files(output_dir, decisions, apply=apply)

    report = {
        "version": __version__,
        "dry_run": not apply,
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "thresholds": {
            "face_threshold": face_threshold,
            "blur_laplacian_min": blur_laplacian_min,
            "blur_score_min": blur_score_min,
            "ear_min": ear_min,
            "yaw_max": yaw_max,
            "pitch_max": pitch_max,
            "session_window_minutes": session_window,
            "session_radius_m": session_radius,
            "phash_hamming_max": phash_hamming_max,
            "near_top_delta": near_top_delta,
        },
        "stats": {
            "scanned": len(scanned),
            "indexed": len(indexed),
            "index_seconds": round(index_elapsed, 3),
            "qualified": sum(1 for d in decisions if d.disposition == "qualified"),
            "duplicate": sum(1 for d in decisions if d.disposition == "duplicate"),
            "cleanup": sum(1 for d in decisions if d.disposition == "cleanup"),
            "no_match_stay": sum(1 for d in decisions if d.disposition == "stay"),
        },
        "images": [
            {
                "path": d.abs_path,
                "quality_label": d.quality_label,
                "disposition": d.disposition,
                "session_id": d.session_id,
                "session_score": round(d.session_score, 4),
                "subject_sim": round(d.subject_sim, 4),
                "tags": d.tags,
            }
            for d in decisions
        ],
        "actions": actions,
        "ambiguous_samples": ambiguous_samples,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_report(output_dir, report)
    write_review_html(output_dir, template, report)

    ambiguous_md = output_dir / "AMBIGUOUS.md"
    if ambiguous_samples:
        lines = ["# 歧义样本（需人工复核）\n", "保守策略：已保留或打标签，未自动删除。\n\n"]
        for s in ambiguous_samples:
            lines.append(f"- `{s['path']}` — {s['reason']}\n")
        ambiguous_md.write_text("".join(lines), encoding="utf-8")

    total = time.perf_counter() - t_all
    typer.echo(json.dumps({"index_seconds": index_elapsed, "total_seconds": total, **report["stats"]}, ensure_ascii=False))
    if not apply:
        typer.echo("dry-run: 加 --apply 才会复制/移动文件")


@app.command()
def version() -> None:
    typer.echo(__version__)


if __name__ == "__main__":
    app()
