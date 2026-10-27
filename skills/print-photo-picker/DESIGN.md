# DESIGN · print-photo-picker Phase 1

## 架构

```
cli.run → scan → index (sqlite cache) → match → quality → session → organize → report/review
```

| 模块 | 职责 |
|------|------|
| `scan.py` | 递归枚举、MD5 去重、PIL 完整性 |
| `image_io.py` | HEIC、EXIF Orientation 转正、占位符检测 |
| `index_worker.py` | 每进程独立 `FaceAnalysis` |
| `index.py` | 增量缓存键 `(path,mtime,size)` |
| `match.py` | 参考脸均值 embedding、主体匹配 |
| `quality.py` | HANDOFF §3 五条规则 |
| `session.py` | §4 三级 session + Top-1 打分 |
| `organize.py` | `copy2` / `move`，无 `unlink` |

## 保守歧义

- `no_match`：不移动源文件（§5 可选留在原位）。
- 双胞胎/多脸高相似：打 `匹配歧义·复核`，不收紧阈值。
- session 边界不确定：宁可少合并（pHash/GPS/时间同时满足才合并）。

## 性能

- 二次运行：缓存命中时仅 sqlite 读取，目标 &lt;3s（无新文件）。
- 大库：建议 `--workers 4~6`，每 worker 独立 InsightFace 实例。

## Phase 2+

见 HANDOFF §10（视频、NIMA、网盘 API 等），本仓库未实现。
