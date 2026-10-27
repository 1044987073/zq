const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', settings: {} },
  onShow() {
    const theme = loadTheme();
    const settings = store.getSettings();
    this.setData({
      pageStyle: themeToPageStyle(theme),
      settings,
      hasPayQr: !!(settings.wechatPayQr || settings.alipayPayQr)
    });
  },

  preview(e) {
    const url = e.currentTarget.dataset.url;
    if (url) wx.previewImage({ urls: [url], current: url });
  },
  openMap() {
    const s = store.getSettings();
    if (s.latitude && s.longitude) {
      wx.openLocation({
        latitude: s.latitude,
        longitude: s.longitude,
        name: s.stallName,
        address: s.locationName
      });
    } else {
      wx.showModal({
        title: '尚未配置坐标',
        content: '请在管理后台「经营设置」中填写经纬度，或先在关于页本地 storage 写入。',
        showCancel: false
      });
    }
  }
});
