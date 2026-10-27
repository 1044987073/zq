# 打印照片人脸筛选 + 质量清理工具 · 交接执行文档

> 目的：把前面所有分析与决策沉淀成一份"另一个 Agent 拿到就能开工"的 Brief。执行者不需要重新问需求，只需按下面开工。
> 生成时间：2026-10-23（Asia/Shanghai）
> 平台：macOS（darwin, arm64），QoderWork 桌面版
> 交接对象：任何具备本机 Shell + Python + 文件操作能力的执行 Agent

---

## 1. 原始需求（用户原话，保留不动）

> 在一堆照片、图片、视频中找到满足打印条件的。这一堆可能是手机相册、电脑相册，也可能是百度网盘中的相册。允许上传图片用来识别人脸，这样就能在这个文件夹里面找到有这张人脸的照片，然后放到一个文件夹中。识别出的人脸图片不允许有重复动作背景、要清晰度高、好看的、适合打印的、可以单人也可以多人，但都要像素好。也支持直接操作手机相册或电脑相册或文件夹，删除重复图片，删除过暗、模糊图片。

---

## 2. 已经拍板的关键决策（D1–D7，勿再问用户）

| 编号 | 决策项 | 结论 | 依据 |
|---|---|---|---|
| **D1** | 数据源范围 | Phase 1 只做**本机文件夹**；iCloud / 百度网盘同步盘（已完整下载到本地）作为兼容路径；iPhone DCIM、Android MTP、百度网盘 OpenAPI 推到 Phase 3+ | iPhone DCIM 从 PC 侧不能删除；百度 API 要 OAuth + 配额 |
| **D2** | 视频处理 | Phase 1 **不做**，只处理图片；Phase 2 加 | ffmpeg 抽帧成本大，先跑通图片链路 |
| **D3** | 分辨率 / DPI 检查 | **不做**。用户明确"不考虑分辨率合格问题" | 从"质量三维"降为"清晰度 + 曝光"两维 + 可选美学 |
| **D4** | 多人合照合格口径 | **主体人脸（匹配参考 embedding 的那张）清晰即可，路人不管** | 用户回答"主体脸清晰，路人不管" |
| **D5** | "重复"严格度 | **同一次拍摄 session（±5 分钟 + 同 GPS 100m）算一组，组内保留 Top-1** | 用户回答"同一次拍摄 session"，且补充"同一人同一场景换角度算重复" |
| **D6** | 删除策略 | **二次确认** + 送系统回收站。本机走 `host_safe_delete`；网盘走原生回收站 API；**永远不硬删** | 用户回答"删除让用户 review，同意后进回收站" |
| **D7** | 人脸隐私 | 参考人脸 embedding 与图索引**全部本地存储**（sqlite），不上云 | 用户回答"存本地" |

---

## 3. 合格判定标准（Locked）

一张图判为"合格"必须同时满足以下 5 条：

1. **主体人脸匹配**：InsightFace ArcFace embedding 与参考人脸余弦相似度 ≥ **0.45**（可 CLI 参数调）
2. **主体不模糊**：InsightFace `face_quality.blur_score` ≥ 阈值 AND 人脸 crop 区域 Laplacian 方差 ≥ **60**
3. **主体不闭眼**：Eye Aspect Ratio（EAR，基于 InsightFace 106 landmark） ≥ **0.21**
4. **主体不严重侧脸**：yaw ≤ 30° AND pitch ≤ 25°（InsightFace pose）
5. **整图曝光正常**：灰度均值 ∈ [50, 220]；高光（>250）像素占比 < 1%；阴影（<15）像素占比 < 3%

**明确不检查**：分辨率、其他人（路人）质量、构图规则、色彩饱和度。

---

## 4. Session 去重规则（Locked）

**分组主键**（按 EXIF 可用性三级降级）：

1. 有 EXIF `DateTimeOriginal` + GPS → 时间窗口 ±5 分钟 AND Haversine 半径 ≤ 100m
2. 有 `DateTimeOriginal` 无 GPS → 时间窗口 ±5 分钟 AND pHash 汉明距离 ≤ 8 AND 同目录
3. EXIF 全无 → 文件 mtime ±5 分钟 AND pHash 汉明距离 ≤ 8 AND 同目录

**组内 Top-1 打分**（0~1 归一化后加权）：

```
score = 0.40 × blur_norm
      + 0.25 × exposure_norm
      + 0.20 × eye_open_norm
      + 0.15 × face_area_ratio_norm
```

Phase 2 再叠加 NIMA 美学分（权重 0.15 起步）。

**关键细节**：Top-2 与 Top-1 分差 < 0.05 时，Top-2 也**保留**，但打上"次优·可复核"标签，不直接判重复。避免主观误杀。

---

## 5. 输出目录结构

```
{output_dir}/
├── 合格/                    # 复制过来的精选（Top-1 per session 且通过全部校验）
│   ├── 2024-08-15_海边/    # 按拍摄日期分子目录（Phase 1 可先扁平）
│   └── ...
├── 待清理/
│   ├── 重复/                # session 内非 Top-1
│   ├── 模糊/                # 主体糊
│   ├── 闭眼/                # 主体闭眼
│   ├── 侧脸/                # 主体严重侧脸
│   ├── 曝光/                # 太暗或过曝
│   └── 无匹配/              # 图里没这个人（可选：留在原位）
├── review.html              # 审阅页
├── report.json              # 结构化结果（含每张图的判定标签、session id、score）
└── delete_manifest.json     # 用户在 review.html 上勾选后导出的删除清单
```

Phase 1 **只做复制 + 移动到"待清理"，不删除**。用户在 `review.html` 勾选 → 导出 `delete_manifest.json` → 回到主 Agent → Agent 二次询问确认 → 调 `host_safe_delete` 分批（≤100 项/次）送废纸篓。

---

## 6. 技术栈

- **Python 3.11**（本机 arm64）
- 核心依赖：
  - `insightface>=0.7.3`（检测+识别+landmark+pose，模型 `buffalo_l` 首次运行自动下载 ~280MB）
  - `onnxruntime>=1.17`（Apple Silicon 走 `CPUExecutionProvider` 已够，可选换 `CoreMLExecutionProvider`）
  - `opencv-python-headless`
  - `pillow` + `pillow-heif`（读 HEIC）
  - `piexif`（EXIF 读取，比 exifread 更稳）
  - `imagehash`（pHash / dHash）
  - `scipy.spatial.distance`（Haversine + 余弦）
  - `sqlalchemy` + `sqlite`（增量索引缓存）
  - `typer` 或 `argparse`（CLI）
- 可选：`rawpy`（读 CR2/NEF/ARW），`nima-ordinal-keras` / `deep-image-aesthetics`（美学分，Phase 2）
- 交付形态：QoderWork Skill（`~/.qwenworkcn/skills/print-photo-picker/SKILL.md`）+ Python 包 + HTML 模板

---

## 7. Pipeline 流程

```
Inputs:
  source_dir   : 相册根目录（递归扫描）
  ref_faces    : 1~3 张参考人脸图（同一人，取 embedding 均值）
  output_dir   : 输出根目录

Step 1  Scan
  ├── 递归列文件：*.jpg/*.jpeg/*.heic/*.png/*.webp/*.tif
  ├── 排除：output_dir 自身、隐藏文件、*.AAE、.DS_Store、Photos Library.photoslibrary
  ├── 精确 hash（MD5）去重：同一文件多副本只索引一次
  └── 完整性探针：PIL 打不开的记为 corrupt，跳过（占位符/损坏）

Step 2  Index（增量，落 sqlite）
  缓存键：(abs_path, file_mtime, file_size)
  对每张未缓存图：
    ├── 加载图像（HEIC → RGB）
    ├── 读 EXIF：DateTimeOriginal, GPS, Orientation
    ├── 按 Orientation 转正 → 再喂模型（避免闭眼误判）
    ├── InsightFace 检全部脸 → 每张脸存 (bbox, embedding, landmarks, pose, blur, illum)
    ├── 灰度直方图统计（mean, >250 占比, <15 占比）
    ├── Laplacian 方差（全图 + 每个 face crop）
    ├── EAR（每个 face）
    └── pHash（全图，64 bit）

Step 3  Match
  ref_emb = mean(normalize(embeddings_of(ref_faces)))
  对每张图：subject_sim = max(cos_sim(face_emb, ref_emb) for face in faces)
  subject_sim ≥ 阈值 → subject_face = argmax face
  （双胞胎等歧义情况：按最大相似度当主体）

Step 4  Quality Gate
  按第 3 节 5 条规则，给每张有 subject_face 的图打标签：
  pass / blur / eyes_closed / pose_bad / exposure_bad
  没匹配到主体 → label = no_match

Step 5  Session Clustering（只对 label=pass 做）
  按第 4 节三级主键分组
  组内 score 排序 → Top-1 进合格
                  → Top-2..N 进 待清理/重复
                  → 与 Top-1 分差 <0.05 的 Top-2..3 打 "次优·可复核" 标签

Step 6  Organize（默认 dry-run）
  cp 合格 → output_dir/合格/
  mv 不合格 → output_dir/待清理/{label}/
  生成 review.html + report.json

Step 7  Human Review
  Agent 用 qoderwork_file_present_files 展示 review.html
  用户在页面上勾选"这些确认删" → 浏览器下载 delete_manifest.json
  用户把 manifest 路径交给 Agent → Agent 二次口头确认 →
  Agent 分批（≤100 项/次）调 host_safe_delete
```

---

## 8. 已知坑（务必规避）

1. **iPhone HEIC**：`pillow-heif` 能读常规 HEIC，但 iOS 17+ 的 HEIF-with-alpha、Live Photo paired 文件可能失败；加 `try/except` 走 `sips -s format jpeg -out <tmp>` 兜底。
2. **EXIF Orientation**：InsightFace 方向不对会误判闭眼/侧脸，**必须先按 EXIF Orientation 转正**再喂模型。
3. **RAW 图**：默认不处理 CR2/NEF/ARW，除非用户显式开 `--include-raw`（依赖 rawpy，转换耗时）。
4. **大相册 5w+ 张**：首次索引 30~60 分钟；用 `ProcessPoolExecutor(max_workers=4~6)` 并发，**注意 InsightFace app 不 fork-safe，每个 worker 单独 `FaceAnalysis()` 建实例**。
5. **iCloud / 百度网盘同步盘**：文件可能是"占位符"（size 有但内容不在本地）—— 检测 `os.stat().st_blocks == 0` 或 PIL 打开失败 → 提示用户先完整下载。
6. **微信下载图**：文件名带 `wx_camera_` 前缀，无 GPS、无 DateTimeOriginal → 走第 4 节降级分组。
7. **`host_safe_delete` 上限 100 items/call**：批量删除要分片，别一次扔 500 张。
8. **`insightface` 首次运行下载模型**：国内网络不稳 → `install.sh` 里预下 `buffalo_l` zip 到 `~/.insightface/models/`，或用 hf-mirror。
9. **参考脸质量太差**：如果 `ref_faces` 本身糊/侧脸 → embedding 不稳 → 加一步预检：任一 ref 图检不到脸或质量分低于阈值 → 直接拒绝并提示用户换图。
10. **重复文件跨目录**：MD5 精确 hash 去重放在 pipeline 最前面，省 30%+ 时间。
11. **软删/硬删边界**：**永远不写 `rm`、`shutil.rmtree`、`Path.unlink` 到用户目录**。所有删除走 `host_safe_delete`。
12. **中文路径 / 空格 / emoji 文件名**：`subprocess.run([...])` 用列表形式，别拼字符串；sqlite 存绝对路径前先 `os.path.realpath`。

---

## 9. MVP 任务拆解（Phase 1，执行 checklist）

- [ ] **T1** 建 Skill 目录 `~/.qwenworkcn/skills/print-photo-picker/`，写 `SKILL.md`（触发词："挑照片 / 打印照片 / 找有 XX 的图 / 相册清理 / 去重 / 找糊图"）
- [ ] **T2** 写 `requirements.txt` + `install.sh`（本机 pip 安装，国内走 tuna 镜像；预下载 `buffalo_l`）
- [ ] **T3** `src/scan.py`：递归列文件 + 完整性探针 + MD5 精确去重
- [ ] **T4** `src/index.py`：sqlite 缓存 + InsightFace + EXIF + Laplacian + pHash 全流程
- [ ] **T5** `src/match.py`：参考脸 embedding 提取（含质量预检）+ 相似度匹配
- [ ] **T6** `src/quality.py`：5 条判定规则实现，输出 label
- [ ] **T7** `src/session.py`：三级降级的 session 分组 + Top-1 打分
- [ ] **T8** `src/organize.py`：复制 / 移动到目标目录结构，dry-run 模式默认
- [ ] **T9** `templates/review.html`：网格展示 + session 分组 + 勾选 + 导出 `delete_manifest.json`
- [ ] **T10** `src/cli.py`：串起 pipeline，参数化所有阈值（`--face-threshold`, `--session-window`, `--session-radius` 等）
- [ ] **T11** Agent 侧集成：`SKILL.md` 里明确说明如何调用 `host_safe_delete` + `qoderwork_file_present_files`；给出 prompt 模板
- [ ] **T12** 端到端测试：500 张混合测试集（单人/多人/连拍/糊/暗/闭眼/GPS 缺失）→ 人工核对 Top-1 命中率 ≥ 80%
- [ ] **T13** 文档：`README.md`（用户） + `DESIGN.md`（后续开发者）

---

## 10. Phase 2 / 3 路线图（**不在本次执行范围，仅记录**）

- **Phase 2**：视频（ffmpeg 抽帧）、NIMA 美学排序、多张参考脸（家庭成员）、按日期分文件夹、增量索引 UI
- **Phase 3**：百度网盘 OpenAPI 直连（原生回收站）、Android MTP 只标记不删、iPhone 走"生成待删清单推回手机相册 App"
- **Phase 4**：Tauri 桌面 App 壳，把 Skill 变成开箱即用产品

---

## 11. 验收标准（Definition of Done）

一份合格的 MVP 交付应该满足：

- **输入**：一个包含至少 500 张真实照片的本机目录 + 1 张参考脸
- **输出**：`合格/` 目录里至少 90% 的图肉眼判定"确实是这个人、且不糊、不闭眼、不太暗"
- **`待清理/` 分类准确**：模糊 / 闭眼 / 曝光 三类误分类率 ≤ 15%
- **Session 分组**：同一次外拍的连拍图能归到一组，跨天不误合并
- **删除安全**：二次确认后调用 `host_safe_delete` 能进废纸篓，恢复测试通过；**全程不产生硬删**
- **隐私**：不上传任何 embedding / 图像到网络；`face_index.db` 仅本地
- **增量性能**：第二次跑同目录，索引阶段 3 秒内完成（无新文件时）
- **审阅体验**：`review.html` 在 macOS 默认浏览器（Safari / Chrome）打开可正常显示缩略图 + 分组 + 勾选 + 导出 manifest

---

## 12. 给接手 Agent 的三句话

1. **所有产品决策已拍板（见第 2 节 D1–D7），不要再回头问用户"要不要考虑分辨率""手机能不能直连"这类已经答过的问题**。
2. **执行中遇到新的岔路**（比如 session 分组边界拿不准、某张图打分并列），**先按最保守的选项做**（宁可少合并、多保留），**不要擅自收紧阈值**；把有歧义的样本单独列出来交给用户复核。
3. **红线只有一条**：**用户目录下的任何文件都不允许硬删**，一律走 `host_safe_delete`；不确定就先复制到 `待清理/`，让用户自己决定。
