const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', fileList: [], wechatList: [], alipayList: [] },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const banners = store.getBanners();
    const settings = store.getSettings();
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      fileList: banners.map((b, i) => ({ url: b.url, name: `banner-${i}`, isImage: true })),
      wechatList: settings.wechatPayQr
        ? [{ url: settings.wechatPayQr, name: 'wechat', isImage: true }]
        : [],
      alipayList: settings.alipayPayQr
        ? [{ url: settings.alipayPayQr, name: 'alipay', isImage: true }]
        : []
    });
  },

  onWechatQr(e) {
    const file = e.detail.file;
    const path = (Array.isArray(file) ? file[0] : file).url || (Array.isArray(file) ? file[0] : file).tempFilePath;
    store.saveSettings({ wechatPayQr: path });
    this.onShow();
  },

  clearWechat() {
    store.saveSettings({ wechatPayQr: '' });
    this.onShow();
  },

  onAlipayQr(e) {
    const file = e.detail.file;
    const path = (Array.isArray(file) ? file[0] : file).url || (Array.isArray(file) ? file[0] : file).tempFilePath;
    store.saveSettings({ alipayPayQr: path });
    this.onShow();
  },

  clearAlipay() {
    store.saveSettings({ alipayPayQr: '' });
    this.onShow();
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
