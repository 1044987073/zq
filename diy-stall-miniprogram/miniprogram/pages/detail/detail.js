const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', product: null },
  onLoad(query) {
    const theme = loadTheme();
    const list = store.getProducts();
    const product = list.find((p) => p.id === query.id) || list[0];
    this.setData({
      pageStyle: themeToPageStyle(theme),
      product
    });
    if (product) {
      wx.setNavigationBarTitle({ title: product.name });
    }
  }
});
