const store = require('../../utils/store');
const { decorateProduct } = require('../../utils/productDisplay');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', product: null },
  onLoad(query) {
    const theme = loadTheme();
    const list = store.getProductsForUser();
    const raw = list.find((p) => p.id === query.id) || list[0];
    const product = raw ? decorateProduct(raw) : null;
    this.setData({
      pageStyle: themeToPageStyle(theme),
      product
    });
    if (product) {
      wx.setNavigationBarTitle({ title: product.name });
    }
  }
});
