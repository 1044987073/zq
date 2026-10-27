const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: {
    pageStyle: '',
    settings: {},
    products: [],
    banners: []
  },

  onShow() {
    const theme = loadTheme();
    const settings = store.getSettings();
    this.setData({
      pageStyle: themeToPageStyle(theme),
      settings,
      products: store.getProducts().slice(0, 4),
      banners: store.getBanners()
    });
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: theme.primary
    });
  },

  goDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  tapAdmin() {
    wx.navigateTo({ url: '/pages-admin/login/login' });
  }
});
