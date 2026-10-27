const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', products: [] },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      products: store.getProducts()
    });
  },

  persist(list) {
    store.saveProducts(list);
    this.setData({ products: list });
  },

  onProductField(e) {
    const { id, field } = e.currentTarget.dataset;
    const value = e.detail;
    const list = this.data.products.map((p) => {
      if (p.id !== id) return p;
      const next = { ...p, [field]: field === 'price' ? Number(value) : value };
      return next;
    });
    this.persist(list);
  },

  changeCover(e) {
    const id = e.currentTarget.dataset.id;
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      success: (res) => {
        const path = res.tempFiles[0].tempFilePath;
        const list = this.data.products.map((p) => (p.id === id ? { ...p, cover: path } : p));
        this.persist(list);
      }
    });
  },

  resetDefault() {
    wx.showModal({
      title: '确认恢复',
      content: '将覆盖当前项目价格为计划文档默认值',
      success: (r) => {
        if (r.confirm) {
          store.resetCatalogToDefault();
          this.setData({ products: store.getProducts() });
        }
      }
    });
  }
});
