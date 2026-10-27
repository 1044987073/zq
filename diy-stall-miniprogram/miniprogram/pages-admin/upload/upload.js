const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', fileList: [] },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const banners = store.getBanners();
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      fileList: banners.map((b, i) => ({ url: b.url, name: `banner-${i}`, isImage: true }))
    });
  },

  afterRead(e) {
    const { file } = e.detail;
    const files = Array.isArray(file) ? file : [file];
    const banners = store.getBanners();
    files.forEach((f) => {
      banners.push({ url: f.url || f.tempFilePath });
    });
    store.saveBanners(banners);
    this.onShow();
  },

  onDelete(e) {
    const idx = e.detail.index;
    const banners = store.getBanners();
    banners.splice(idx, 1);
    store.saveBanners(banners);
    this.onShow();
  }
});
