# 在即时设计中复刻本套 UI

本仓库 **`diy-stall-design`** 用 **Vue 3 + TDesign** 实现了与小程序一致的用户端 / 管理端，便于你对照像素和在浏览器里改稿。

## 1. 在即时设计里用同一套组件语言

即时设计资源广场提供 **TDesign Web / 移动端** 官方物料，与代码组件一一对应：

| 用途 | 即时设计资源 | 代码 |
|------|----------------|------|
| 管理端（桌面） | [TDesign Web 端组件](https://js.design/community?category=detail&id=625d594eba0a72e19014f0fb&type=resource) | `tdesign-vue-next` |
| 用户端（手机） | 资源广场搜「TDesign 移动端」 | `tdesign-mobile-vue` |
| 官方入口 | [TDesign 设计资源](https://tdesign.tencent.com/source) → 即时设计 | — |

**操作步骤：**

1. 登录 [即时设计](https://js.design)。
2. 资源广场搜索 **TDesign**，使用 **Web 端** + **移动端** 组件库（免费）。
3. 新建画板尺寸：**375×812**（用户端）、**1440×900**（管理端）。
4. 按本仓库运行效果搭页面（见下），或把 `npm run dev` 截图导入即时设计「图片」参考。

## 2. 本地运行可交互稿（推荐对照）

```bash
cd diy-stall-design
npm install
npm run dev
```

- 左侧手机框：**用户端**（Tab：首页 / 项目 / 套餐 / 关于）
- 访问 `/admin/login`，默认口令 **`demo123`**：**管理端**（TDesign 后台布局）

改管理端数据会写入 `localStorage`，用户端即时同步。

## 3. 画板清单（与即时设计文件建议一致）

| 画板名 | 尺寸 | 内容 |
|--------|------|------|
| 用户-首页 | 375×812 | Hero、主推、列表 |
| 用户-项目列表 | 375×812 | Cell 列表 |
| 用户-商品详情 | 375×812 | 封面、步骤、说明 |
| 用户-套餐 | 375×812 | 套餐卡片 |
| 用户-关于 | 375×812 | 信息 + 可选收款码 |
| 管理-控制台 | 1440×900 | 统计 + 经营设置 |
| 管理-商品 | 1440×900 | 表单、折叠面板 |
| 管理-主题 | 1440×900 | 色板 / Token |

## 4. 发布到即时设计资源广场（可选）

完稿后：文件右上角 **分享协作 → 发布至资源广场**，即可生成可分享的网页链接（类似你给团队看的蓝湖/Figma 链接）。

## 5. 为何选 Vue 3 而不是 React

- 小程序侧已用 **TDesign 小程序**；**TDesign Mobile Vue** 与 **tdesign-vue-next** 同一套 Design Token，和即时设计里的 TDesign 物料对齐成本最低。
- 若你更熟 React，可把页面迁到 `tdesign-react` + `tdesign-mobile-react`，画板结构不变。
