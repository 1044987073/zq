const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

function withStepsText(list) {
  return list.map((p) => ({
    ...p,
    stepsText: (p.steps || []).join('\n')
  }));
}

Page({
  data: {
    pageStyle: '',
    products: [],
    bannerList: [],
    wechatList: [],
    alipayList: []
  },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const settings = store.getSettings();
    const banners = store.getBanners();
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      products: withStepsText(store.getProducts()),
      bannerList: banners.map((b, i) => ({ url: b.url, name: `banner-${i}`, isImage: true })),
      wechatList: settings.wechatPayQr ? [{ url: settings.wechatPayQr, isImage: true }] : [],
      alipayList: settings.alipayPayQr ? [{ url: settings.alipayPayQr, isImage: true }] : []
    });
  },

  persist(list) {
    store.saveProducts(list);
    this.setData({ products: withStepsText(list) });
  },

  onProductField(e) {
    const { id, field } = e.currentTarget.dataset;
    const value = e.detail;
    const list = store.getProducts().map((p) => {
      if (p.id !== id) return p;
      const next = { ...p };
      if (field === 'price' || field === 'cost') {
        next[field] = value === '' ? '' : Number(value);
      } else if (field === 'stock') {
        next.stock = value === '' ? null : Number(value);
      } else {
        next[field] = value;
      }
      return next;
    });
    this.persist(list);
  },

  onStepsField(e) {
    const id = e.currentTarget.dataset.id;
    const lines = (e.detail || '')
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean);
    const list = store.getProducts().map((p) => (p.id === id ? { ...p, steps: lines } : p));
    this.persist(list);
  },

  onEnabled(e) {
    const id = e.currentTarget.dataset.id;
    const enabled = e.detail;
    const list = store.getProducts().map((p) => (p.id === id ? { ...p, enabled } : p));
    this.persist(list);
  },

  changeCover(e) {
    const id = e.currentTarget.dataset.id;
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      success: (res) => {
        const path = res.tempFiles[0].tempFilePath;
        const list = store.getProducts().map((p) => (p.id === id ? { ...p, cover: path } : p));
        this.persist(list);
      }
    });
  },

  addProduct() {
    const list = store.getProducts();
    const id = `custom-${Date.now()}`;
    list.push({
      id,
      name: '新商品',
      price: 0,
      priceLabel: '面议',
      cost: 0,
      stock: null,
      enabled: true,
      tag: '',
      duration: '',
      age: '',
      cover: '/assets/products/mask.png',
      steps: ['现场体验'],
      desc: ''
    });
    this.persist(list);
    wx.showToast({ title: '已添加', icon: 'success' });
  },

  resetDefault() {
    wx.showModal({
      title: '确认恢复',
      content: '将覆盖当前商品为计划文档默认值',
      success: (r) => {
        if (r.confirm) {
          store.resetCatalogToDefault();
          this.onShow();
        }
      }
    });
  },

  onBannerAdd(e) {
    const { file } = e.detail;
    const files = Array.isArray(file) ? file : [file];
    const banners = store.getBanners();
    files.forEach((f) => banners.push({ url: f.url || f.tempFilePath }));
    store.saveBanners(banners);
    this.onShow();
  },

  onBannerDelete(e) {
    const banners = store.getBanners();
    banners.splice(e.detail.index, 1);
    store.saveBanners(banners);
    this.onShow();
  },

  onWechatQr(e) {
    const file = e.detail.file;
    const f = Array.isArray(file) ? file[0] : file;
    store.saveSettings({ wechatPayQr: f.url || f.tempFilePath });
    this.onShow();
  },

  clearWechat() {
    store.saveSettings({ wechatPayQr: '' });
    this.onShow();
  },

  onAlipayQr(e) {
    const file = e.detail.file;
    const f = Array.isArray(file) ? file[0] : file;
    store.saveSettings({ alipayPayQr: f.url || f.tempFilePath });
    this.onShow();
  },

  clearAlipay() {
    store.saveSettings({ alipayPayQr: '' });
    this.onShow();
  }
});
