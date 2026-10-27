# 公园 DIY · 设计先行交付包

你要的流程：**先在即时设计里定稿 → 再按稿开发**。本目录是 **第 ① 步** 的交付物（云端无法代你登录 js.design 建文件）。

| 文件 | 作用 |
|------|------|
| [DESIGN-WORKFLOW.md](./DESIGN-WORKFLOW.md) | 设计 → 开发 → 走查流程 |
| [SPEC-v1.md](./SPEC-v1.md) | 画板清单、尺寸、组件映射（搭稿依据） |
| [tokens.json](./tokens.json) | Design Token（与开发 CSS 变量一致） |
| [JSDESIGN-STEP-BY-STEP.md](./JSDESIGN-STEP-BY-STEP.md) | 在即时设计里搭出真稿的步骤 |
| [screens/](./screens/) | 高保真参考图（可拖入即时设计） |

## 生成参考截图（可选）

```bash
cd ../diy-stall-design && npm install && npm run build
cd ../design/scripts && npm init -y && npm i playwright && npx playwright install chromium
node capture-screens.mjs
```

生成后把 `screens/*.png` 拖进即时设计画布作参考，**用 TDesign 组件重绘** 后分享链接，即「真实 UI 设计稿」。

## 定稿后

把即时设计链接写入 `SPEC-v1.md` 顶部，再按 `DESIGN-WORKFLOW.md` 进入小程序开发走查。
