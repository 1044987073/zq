# 公园手工 DIY 摆摊小程序

用户端展示价目与玩法；管理后台支持 **上传图片、改价、记账、主题配色**，带口令 + OpenID 白名单权限控制。

详细 UI 规范见 [docs/UI-DESIGN.md](docs/UI-DESIGN.md)。

## 快速开始

```bash
cd diy-stall-miniprogram
npm install
```

1. 微信开发者工具导入本项目根目录。
2. **工具 → 构建 npm**（生成 `miniprogram/miniprogram_npm`）。
3. `cp miniprogram/config/private.example.js miniprogram/config/private.js`，修改 `adminPassphrase`。
4. 将 `project.config.json` 里的 `appid` 换成你的小程序 AppID。

## 管理后台

- 入口：用户端首页底部「摊主管理入口」，或直达 `/pages-admin/login/login`。
- 仅口令：留空 `adminOpenIds` 即可（仅防路人误点，安全性一般）。
- 仅自己：开通云开发、部署 `login` 云函数，把 openid 写入 `adminOpenIds`。

## 技术栈

- 原生微信小程序
- [@vant/weapp](https://github.com/youzan/vant-weapp)（MIT）
- [tdesign-miniprogram](https://github.com/Tencent/tdesign-miniprogram)（MIT，已安装便于后续扩展 ColorPicker 等）

数据默认存本地 Storage；适合摆摊试跑。后续可迁云开发数据库做多端同步。
