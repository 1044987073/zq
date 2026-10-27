# 公园 DIY 小程序 — UI 设计说明

## 1. 选用的免费 UI 库

| 库 | 协议 | 用途 |
|----|------|------|
| [Vant Weapp](https://github.com/youzan/vant-weapp)（`@vant/weapp`） | MIT | 按钮、表单、上传、轮播、Toast |
| [TDesign 小程序](https://tdesign.tencent.com/miniprogram)（`tdesign-miniprogram`） | MIT | 可选扩展；主题变量 `--td-brand-color` 已与主色同步 |

两者均为市面常用、免费开源方案，通过 **CSS 变量** 改色，无需改组件源码。

## 2. 设计定位

- **用户端**：清爽、亲子友好、信息一眼能读完；主色偏自然绿（公园、手工），强调色用于价格与 CTA。
- **管理端**：与 user 端同一套 Design Token，减少割裂感；列表 + 表单为主，操作路径短。

## 3. Design Token（可改色字段）

在 `miniprogram/styles/tokens.wxss` 定义默认值；管理后台 **主题配色** 页修改后写入本地 `shopTheme`，并通过 `pageStyle` 注入到各页。

| Token | 默认值 | 说明 |
|-------|--------|------|
| `--color-primary` | `#2D6A4F` | 导航栏、主按钮、Tab 选中 |
| `--color-primary-light` | `#52B788` | 首页 Hero 渐变 |
| `--color-secondary` | `#D8F3DC` | 标签底、步骤序号底 |
| `--color-accent` | `#F4A261` | 价格、营业额数字 |
| `--color-bg` | `#F7F9F8` | 页面背景 |
| `--color-surface` | `#FFFFFF` | 卡片 |
| `--color-text` | `#1B4332` | 标题正文 |
| `--color-text-muted` | `#52796F` | 辅助说明 |
| `--radius-md` | `16rpx` | 卡片圆角 |

同步覆盖第三方变量：

- Vant：`--van-primary-color`、`--van-button-primary-background-color`
- TDesign：`--td-brand-color`

## 4. 信息架构

```
用户 Tab：首页 | 项目 | 套餐 | 关于
  首页 → 主推 + 轮播 + 项目卡片 → 详情
  项目 → 全列表 → 详情
  套餐 → 套餐 A/B + 加项说明
  关于 → 营业时间、安全提示、地图
  隐藏入口：首页底部「摊主管理入口」

管理（需登录）：
  登录 → 控制台（今日汇总 + 经营开关）
    → 项目与价格（改价、换封面图）
    → 图片上传（首页轮播）
    → 记账
    → 主题配色（预设 + 自定义 hex）
```

## 5. 权限模型

1. **口令**：`config/private.js` 中 `adminPassphrase`（从 `private.example.js` 复制）。
2. **仅自己（推荐）**：配置 `adminOpenIds` + 云函数 `login` 返回 openid，非白名单即使口令正确也拒绝。
3. **会话**：登录成功本地保存 7 天 `adminSession`；各 `pages-admin/*` 在 `onShow` 调用 `requireAdmin`。

## 6. 预设主题

管理端内置四套一键主题：森林绿（默认）、秋日南瓜、海洋蓝、樱花粉。可自行改 hex 后保存。

## 7. 交付物对照

| 需求 | 实现位置 |
|------|----------|
| 用户端主展示 | `pages/home`、`catalog`、`detail`、`bundles`、`about` |
| 上传 | `pages-admin/upload` + 项目封面 `products` |
| 记账 | `pages-admin/ledger` + 控制台今日汇总 |
| 改颜色 | `pages-admin/theme` + `utils/theme.js` |
| 权限 | `utils/auth.js` + `config/private.js` |

## 8. 本地运行

1. 用微信开发者工具打开 `diy-stall-miniprogram` 目录。
2. 填写真实 `appid`（`project.config.json`）。
3. 终端执行 `npm install`，开发者工具 **工具 → 构建 npm**。
4. 复制 `miniprogram/config/private.example.js` → `private.js` 并改口令。
5. （可选）开通云开发并上传 `cloudfunctions/login`，配置 `adminOpenIds`。
