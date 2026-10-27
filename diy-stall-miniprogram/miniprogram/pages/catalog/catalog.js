const store = require('../../utils/store');
const { decorateList } = require('../../utils/productDisplay');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', products: [] },
  onShow() {
    const theme = loadTheme();
    this.setData({
      pageStyle: themeToPageStyle(theme),
      products: decorateList(store.getProductsForUser())
    });
  },
  goDetail(e) {
    wx.navigateTo({ url: `/pages/detail/detail?id=${e.currentTarget.dataset.id}` });
  }
});
