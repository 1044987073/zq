# 公园 DIY · TDesign 设计实现（Vue 3）

与微信小程序业务一致的高保真 **可运行设计稿**：用户端（TDesign Mobile）+ 管理端（TDesign Vue Next）。

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
