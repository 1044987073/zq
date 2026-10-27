const store = require('../../utils/store');
const { decorateList, decorateProduct } = require('../../utils/productDisplay');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: {
    pageStyle: '',
    settings: {},
    products: [],
    featured: null,
    banners: []
  },

  onShow() {
    const theme = loadTheme();
    const settings = store.getSettings();
    const list = decorateList(store.getProductsForUser());
    const featured =
      list.find((p) => p.tag === '招牌') ||
      list.find((p) => p.id === 'pumpkin-s') ||
      list[0];
    this.setData({
      pageStyle: themeToPageStyle(theme),
      settings,
      products: list.slice(0, 4),
      featured: featured ? decorateProduct(featured) : null,
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
