# UI 设计稿（蓝湖 / Figma 式网页预览）

在浏览器里打开 **整页设计交付工具**：左侧画板列表、中间可缩放画布、右侧标注与改色。

## 打开方式

### 1. 本地（推荐）

用 Chrome / Edge 打开同目录下的 **`index.html`**（需保持 `viewer.css`、`boards.js`、`viewer.js` 在同一文件夹）。

### 2. 在线（GitHub Pages）

合并代码后，若仓库已开启 Pages（见下方「部署」），访问：

`https://<你的用户名>.github.io/<仓库名>/`

（工作流会把本目录发布为站点根目录。）

### 3. 临时预览（未开 Pages 时）

[HtmlPreview 打开 index.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/1044987073/zq/cursor/diy-miniprogram-ui-f2de/diy-stall-miniprogram/design-preview/index.html)

> HtmlPreview 对部分多文件站点支持不稳定；**本地打开 index.html 最可靠**。

## 操作说明

| 操作 | 说明 |
|------|------|
| 左侧画板 | 切换屏幕，画布自动滚到对应画板 |
| 顶部 + / − | 缩放 |
| Ctrl + 滚轮 | 缩放（Mac：⌘ + 滚轮） |
| 右侧色块 | 修改主题 Token，所有画板同步 |

## 和 Figma / 蓝湖的关系

| 工具 | 说明 |
|------|------|
| **本设计稿** | 免费、即开即用，贴近小程序真实布局；适合你自己看稿、给合伙人演示。 |
| **Figma** | 需在 [figma.com](https://www.figma.com) 建稿；可把本页各画板截图导入 Figma，或按右侧色值建 Variables。 |
| **蓝湖** | 通常 **从 Figma / Sketch 上传** 后才能在 lanhuapp.com 看标注；不能直接从本仓库一键同步。 |

当前云环境无法代你登录 Figma 账号；若你需要 **原生 .fig 文件**，可在 Figma 中按本预览搭一版后分享链接。

## 部署 GitHub Pages（可选）

仓库已包含 workflow：推送 `master` 后自动发布 `design-preview/`。在 GitHub 仓库 **Settings → Pages** 中选择 **GitHub Actions** 源即可。
