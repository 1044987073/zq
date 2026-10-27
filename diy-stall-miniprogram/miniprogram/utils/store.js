const PRODUCTS_KEY = 'shopProducts';
const LEDGER_KEY = 'shopLedger';
const BANNERS_KEY = 'shopBanners';
const SETTINGS_KEY = 'shopSettings';

const DEFAULT_PRODUCTS = [
  {
    id: 'mask',
    name: 'DIY 面具绘画',
    price: 15,
    priceLabel: '15 元/个',
    cost: 2.1,
    tag: '热门',
    duration: '约 15 分钟',
    age: '4–10 岁',
    cover: '/assets/products/mask.png',
    steps: ['选空白面具', '丙烯自由涂色', '现场晾干带走'],
    desc: '可加羽毛贴纸提价，适合低龄小朋友。'
  },
  {
    id: 'pumpkin-s',
    name: '南瓜石膏娃娃（小）',
    price: 10,
    priceLabel: '10–12 元/个',
    cost: 2.8,
    tag: '招牌',
    duration: '约 20 分钟',
    age: '5 岁+',
    cover: '/assets/products/pumpkin.png',
    steps: ['小锤敲开石膏壳', '取出南瓜娃娃', '涂色装饰带走'],
    desc: '「砸」的过程很解压，围观引流效果好。'
  },
  {
    id: 'pumpkin-l',
    name: '南瓜石膏娃娃（大）',
    price: 15,
    priceLabel: '15–18 元/个',
    cost: 4.8,
    tag: '招牌',
    duration: '约 25 分钟',
    age: '5 岁+',
    cover: '/assets/products/pumpkin.png',
    steps: ['敲开大石膏', '取出娃娃', '精细涂色'],
    desc: '体验感更强，建议垫布防飞溅。'
  },
  {
    id: 'fan',
    name: '涂鸦扇子',
    price: 8,
    priceLabel: '8–10 元/把',
    cost: 0.34,
    tag: '走量',
    duration: '约 10 分钟',
    age: '全年龄',
    cover: '/assets/products/fan.png',
    steps: ['选空白扇面', '现场绘画', '即取即用'],
    desc: '成本低、周转快，试营业可先用 8 元聚人气。'
  },
  {
    id: 'wish-20',
    name: '许愿瓶 20ml',
    price: 10,
    priceLabel: '10–15 元/个',
    cost: 0.98,
    tag: '',
    duration: '约 10 分钟',
    age: '6 岁+',
    cover: '/assets/products/wish.png',
    steps: ['装泡大珠', '加纸条亮片', '拧盖带走'],
    desc: '小款便宜款；泡大珠 +2 元，灯串/纸条 +3 元。'
  },
  {
    id: 'wish-55',
    name: '许愿瓶 55ml',
    price: 15,
    priceLabel: '15–20 元/个',
    cost: 1.34,
    tag: '推荐',
    duration: '约 15 分钟',
    age: '6 岁+',
    cover: '/assets/products/wish.png',
    steps: ['大瓶更多装饰', '泡大珠变色', '许愿带走'],
    desc: '提醒 3 岁以下勿误吞小珠。'
  },
  {
    id: 'dig',
    name: '考古挖掘',
    price: 20,
    priceLabel: '20–25 元/个',
    cost: 5.9,
    tag: '打卡',
    duration: '10–20 分钟',
    age: '6 岁+',
    cover: '/assets/products/dig.png',
    steps: ['选挖掘块', '工具挖化石', '取出模型收藏'],
    desc: '高价体验项，人多时可引导先选面具/扇子。'
  }
];

const DEFAULT_BUNDLES = [
  {
    id: 'combo-a',
    name: '小朋友套餐 A',
    price: 48,
    items: ['面具绘画', '小石膏娃娃', '小许愿瓶 20ml'],
    saveHint: '比单买更划算'
  },
  {
    id: 'combo-b',
    name: '体验套餐 B',
    price: 58,
    items: ['大石膏娃娃', '考古挖掘', '大许愿瓶 55ml'],
    saveHint: '重磅体验组合'
  }
];

const DEFAULT_SETTINGS = {
  stallName: '公园手工 DIY 小摊',
  slogan: '砸石膏 · 涂面具 · 把创意带回家',
  openHours: '16:00 – 20:00（周末及节假日）',
  isOpen: true,
  locationName: '公园儿童游乐区附近',
  notice: '颜料为水洗丙烯；许愿瓶含小珠，3 岁以下请在家长陪同下体验。',
  payHint: '现场扫码付款，付款后请告知摊主开始体验',
  wechatPayQr: '',
  alipayPayQr: ''
};

function readJson(key, fallback) {
  try {
    const v = wx.getStorageSync(key);
    if (v !== undefined && v !== '' && v !== null) return v;
  } catch (e) {
    /* ignore */
  }
  return fallback;
}

function getProducts() {
  return readJson(PRODUCTS_KEY, DEFAULT_PRODUCTS);
}

function saveProducts(list) {
  wx.setStorageSync(PRODUCTS_KEY, list);
}

function getBundles() {
  return readJson('shopBundles', DEFAULT_BUNDLES);
}

function getSettings() {
  return { ...DEFAULT_SETTINGS, ...readJson(SETTINGS_KEY, {}) };
}

function saveSettings(partial) {
  const next = { ...getSettings(), ...partial };
  wx.setStorageSync(SETTINGS_KEY, next);
  return next;
}

function getBanners() {
  const list = readJson(BANNERS_KEY, []);
  return Array.isArray(list) ? list : [];
}

function saveBanners(list) {
  wx.setStorageSync(BANNERS_KEY, list);
}

function getLedger() {
  const list = readJson(LEDGER_KEY, []);
  return Array.isArray(list) ? list : [];
}

function addLedgerEntry(entry) {
  const list = getLedger();
  const row = {
    id: `L${Date.now()}`,
    createdAt: Date.now(),
    ...entry
  };
  list.unshift(row);
  wx.setStorageSync(LEDGER_KEY, list);
  return row;
}

function ledgerSummaryByDate(dateStr) {
  const list = getLedger().filter((r) => formatDate(r.createdAt) === dateStr);
  let revenue = 0;
  let cost = 0;
  const byProduct = {};
  list.forEach((r) => {
    const amount = (r.price || 0) * (r.qty || 1);
    revenue += amount;
    cost += (r.cost || 0) * (r.qty || 1);
    const key = r.productName || '其他';
    byProduct[key] = (byProduct[key] || 0) + (r.qty || 1);
  });
  return { count: list.length, revenue, profit: revenue - cost, byProduct, rows: list };
}

function formatDate(ts) {
  const d = new Date(ts);
  const y = d.getFullYear();
  const m = `${d.getMonth() + 1}`.padStart(2, '0');
  const day = `${d.getDate()}`.padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function resetCatalogToDefault() {
  wx.setStorageSync(PRODUCTS_KEY, DEFAULT_PRODUCTS);
  wx.setStorageSync('shopBundles', DEFAULT_BUNDLES);
}

module.exports = {
  DEFAULT_PRODUCTS,
  DEFAULT_BUNDLES,
  getProducts,
  saveProducts,
  getBundles,
  getSettings,
  saveSettings,
  getBanners,
  saveBanners,
  getLedger,
  addLedgerEntry,
  ledgerSummaryByDate,
  formatDate,
  resetCatalogToDefault
};
