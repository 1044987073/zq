/* 画板数据：与小程序页面对应 */
window.DH_BOARDS = [
  {
    id: 'home',
    name: '用户端 · 首页',
    desc: 'Hero 营业状态、主推商品、项目列表、底部 Tab。轮播由管理端上传。',
    tab: true,
    html: `
      <div class="dh-hero">
        <h2>公园手工 DIY 小摊</h2>
        <p>砸石膏 · 涂面具 · 把创意带回家</p>
        <p style="margin-top:12px;font-size:12px"><span class="dh-dot"></span>今日营业中 · 16:00 – 20:00</p>
      </div>
      <div class="dh-section">主推体验</div>
      <div class="dh-card">
        <div class="dh-thumb-lg c1"></div>
        <div><h3>南瓜石膏娃娃（小）<span class="dh-pill">招牌</span></h3><div class="dh-muted">约 20 分钟 · 5 岁+</div><div class="dh-price">10–12 元/个</div></div>
      </div>
      <div class="dh-section">全部项目</div>
      <div class="dh-card"><div class="dh-thumb-lg c2"></div><div><h3>DIY 面具绘画</h3><div class="dh-muted">约 15 分钟</div><div class="dh-price">15 元/个</div></div></div>
      <div class="dh-card"><div class="dh-thumb-lg c3"></div><div><h3>许愿瓶 55ml</h3><div class="dh-muted">剩余 10</div><div class="dh-price">15–20 元/个</div></div></div>
    `
  },
  {
    id: 'catalog',
    name: '用户端 · 项目列表',
    desc: '全部上架商品：图、简介、价格、库存状态。',
    tab: true,
    html: `
      <div class="dh-card"><div class="dh-thumb-lg c2"></div><div><h3>DIY 面具绘画</h3><div class="dh-muted">可加羽毛贴纸提价</div><div class="dh-price">15 元/个</div></div></div>
      <div class="dh-card"><div class="dh-thumb-lg c1"></div><div><h3>南瓜石膏（大）</h3><div class="dh-muted">招牌</div><div class="dh-price">15–18 元/个</div></div></div>
      <div class="dh-card"><div class="dh-thumb-lg"></div><div><h3>涂鸦扇子</h3><div class="dh-muted">走量</div><div class="dh-price">8–10 元/把</div></div></div>
    `
  },
  {
    id: 'detail',
    name: '用户端 · 商品详情',
    desc: '大图、价格、玩法步骤、说明文案，数据来自管理端商品管理。',
    tab: false,
    html: `
      <div class="dh-cover"></div>
      <h2 style="margin:0 0 8px;font-size:20px">南瓜石膏娃娃（小）</h2>
      <div class="dh-price">10–12 元/个</div>
      <div class="dh-muted">约 20 分钟 · 适合 5 岁+ · 剩余 15</div>
      <div class="dh-section">玩法步骤</div>
      <div class="dh-card dh-card--col">
        <div class="dh-step"><i>1</i>小锤敲开石膏壳</div>
        <div class="dh-step"><i>2</i>取出南瓜娃娃</div>
        <div class="dh-step"><i>3</i>涂色装饰带走</div>
      </div>
      <div class="dh-section">说明</div>
      <div class="dh-card dh-card--col"><div class="dh-muted">「砸」的过程很解压，围观引流效果好。</div></div>
    `
  },
  {
    id: 'bundles',
    name: '用户端 · 套餐',
    desc: '套餐 A/B 与许愿瓶加项说明。',
    tab: true,
    html: `
      <div class="dh-card dh-card--col">
        <div style="display:flex;justify-content:space-between;align-items:baseline"><h3>小朋友套餐 A</h3><span class="dh-combo-price">¥48</span></div>
        <div class="dh-muted">面具 + 小石膏 + 小许愿瓶</div>
      </div>
      <div class="dh-card dh-card--col">
        <div style="display:flex;justify-content:space-between;align-items:baseline"><h3>体验套餐 B</h3><span class="dh-combo-price">¥58</span></div>
        <div class="dh-muted">大石膏 + 考古 + 大许愿瓶</div>
      </div>
      <div class="dh-section">加项</div>
      <div class="dh-muted">泡大珠 +2 元 · 灯串/纸条 +3 元</div>
    `
  },
  {
    id: 'about',
    name: '用户端 · 关于',
    desc: '摊位信息；可选展示收款码（管理端上传后才显示）。',
    tab: true,
    html: `
      <div class="dh-card dh-card--col">
        <div class="dh-muted">时间：16:00 – 20:00</div>
        <div class="dh-muted">位置：公园儿童游乐区附近</div>
      </div>
      <div class="dh-section">现场付款（可选）</div>
      <div class="dh-card dh-card--col" style="align-items:center;text-align:center">
        <div class="dh-muted">微信 / 支付宝收款码占位</div>
        <div style="width:160px;height:160px;background:var(--color-secondary);border-radius:12px;margin:12px auto"></div>
      </div>
    `
  },
  {
    id: 'admin-products',
    name: '管理端 · 商品管理',
    desc: '换图、定价、库存、玩法与步骤；轮播与收款码在同页底部。',
    tab: false,
    html: `
      <div class="dh-section">商品</div>
      <div class="dh-card">
        <div class="dh-thumb-lg c1"></div>
        <div style="flex:1">
          <div class="dh-field"><label>名称</label>南瓜石膏娃娃（小）</div>
          <div class="dh-field"><label>售价 / 库存</label>10 · 15</div>
        </div>
      </div>
      <div class="dh-field"><label>玩法说明</label>砸石膏后现场涂色</div>
      <div class="dh-field"><label>步骤</label>敲开 → 取出 → 涂色</div>
      <button type="button" class="dh-btn">新增商品</button>
    `
  },
  {
    id: 'admin-ledger',
    name: '管理端 · 记账',
    desc: '记一笔销售；自动扣减库存；控制台展示今日汇总。',
    tab: false,
    html: `
      <div class="dh-field"><label>项目</label>涂鸦扇子</div>
      <div class="dh-field"><label>数量 / 实收</label>2 · ¥8</div>
      <button type="button" class="dh-btn">保存</button>
      <div class="dh-section">今日记录</div>
      <div class="dh-card dh-card--col"><div class="dh-muted">面具 × 1 · ¥15</div></div>
    `
  }
];

window.DH_TOKENS = [
  { var: '--color-primary', label: '主色' },
  { var: '--color-primary-light', label: '主色浅' },
  { var: '--color-secondary', label: '辅色底' },
  { var: '--color-accent', label: '强调色' },
  { var: '--color-bg', label: '页面背景' },
  { var: '--color-text', label: '正文色' }
];
