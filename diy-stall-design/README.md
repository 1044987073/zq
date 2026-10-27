# 公园 DIY · TDesign 设计实现（Vue 3）

> **流程说明**：正式流程应为 **先在即时设计定稿**（见 `../design/`），再按稿开发。本工程用于定稿前预览、导出 `design/screens` 参考图，或定稿后 UI 走查对照，**不是**替代即时设计源文件。

与微信小程序业务一致的可运行原型：用户端（TDesign Mobile）+ 管理端（TDesign Vue Next）。

## 技术选型

| 端 | 框架 | UI |
|----|------|-----|
| 用户端 | Vue 3 | `tdesign-mobile-vue` |
| 管理端 | Vue 3 | `tdesign-vue-next` |
| 状态 | Pinia + localStorage | 与小程序逻辑对齐 |

与 **即时设计** 中使用的 [TDesign 官方物料](https://tdesign.tencent.com/source) 同源，便于设计师在 js.design 搭稿、开发对照本仓库。

## 快速开始

```bash
npm install
npm run dev
```

- 用户端：`http://localhost:5173/`
- 管理端：`http://localhost:5173/admin/login`（默认口令 `demo123`）

## 即时设计

见 [docs/JSDESIGN.md](docs/JSDESIGN.md)。

## 关联项目

微信小程序实现：`../diy-stall-miniprogram/`
