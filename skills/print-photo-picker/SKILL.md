# print-photo-picker

**触发词**：挑照片 / 打印照片 / 找有 XX 的图 / 相册清理 / 去重 / 找糊图

## 能力

对本机文件夹递归扫描照片，按参考人脸筛选主体，做清晰度/闭眼/侧脸/曝光质检，按拍摄 session 去重，输出 `合格/`、`待清理/`、`review.html`、`report.json`。

Phase 1 **不硬删**：仅复制合格、移动不合格到 `待清理/`；真删由宿主 Agent 处理。

## 调用

```bash
cd ~/.qwenworkcn/skills/print-photo-picker
python3.11 -m src.cli run \
  --source /path/to/album \
  --ref-face /path/to/ref.jpg \
  --output /path/to/output \
  --workers 4
# 确认无误后：
python3.11 -m src.cli run ... --apply
```

## 宿主 Agent 集成（T11）

1. 用 `qoderwork_file_present_files` 展示 `{output}/review.html`。
2. 用户在浏览器勾选 → 下载 `delete_manifest.json`。
3. **二次口头确认**后，对 manifest 中路径调用 `host_safe_delete`，**每批 ≤100 条**。

### Prompt 模板

```
用户已确认删除清单 delete_manifest.json（N 条）。
请逐条复述将移入废纸篓的数量与根目录，用户明确说「确认删除」后，
分批调用 host_safe_delete（每批最多 100 个路径）。禁止 rm / unlink / rmtree。
```

## 红线

- 用户目录禁止硬删；本 Skill 的 organize 阶段只用 `copy` / `move`。
- embedding 与 `face_index.db` 仅本地 sqlite。
