# print-photo-picker (Phase 1)

打印照片人脸筛选 + 质量清理工具。完整规格见 `DESIGN.md` 与交接 `HANDOFF.md`。

## 安装 (macOS arm64, Python 3.11)

```bash
chmod +x install.sh
./install.sh
```

或手动复制本目录到 `~/.qwenworkcn/skills/print-photo-picker` 后 `pip install -r requirements.txt`。

## 使用

```bash
python3.11 -m src.cli run \
  /path/to/photos \
  --ref-face /path/to/ref1.jpg \
  --output /path/to/out \
  --workers 4
```

默认 **dry-run**（只写 `report.json` / `review.html`，不移动源文件）。加 `--apply` 执行复制/移动。

### 常用阈值参数

| Flag | 默认 | 说明 |
|------|------|------|
| `--face-threshold` | 0.45 | 主体人脸余弦相似度 |
| `--blur-laplacian-min` | 60 | 人脸 crop Laplacian |
| `--ear-min` | 0.21 | 睁眼 EAR |
| `--session-window` | 5 | session 时间窗（分钟） |
| `--session-radius` | 100 | GPS 半径（米） |
| `--phash-hamming-max` | 8 | 无 GPS 时 pHash 距离 |
| `--near-top-delta` | 0.05 | Top-2 与 Top-1 保留标签 |

## 输出

见 `HANDOFF.md` §5：`合格/`、`待清理/*`、`review.html`、`report.json`。

## 测试数据

```bash
python3.11 scripts/generate_test_set.py --out /tmp/photo-picker-test --count 520
```

## 删除流程

本工具 **不** 调用 `host_safe_delete`。用户在 `review.html` 导出 manifest → 由 QoderWork 主 Agent 分批删除。
