const { applyThemeToApp } = require('./utils/theme');
const store = require('./utils/store');

App({
  onLaunch() {
    if (wx.cloud) {
      wx.cloud.init({
        traceUser: true
      });
    }
    applyThemeToApp(this);
    this.globalData.settings = store.getSettings();
    this.globalData.products = store.getProducts();
  },

  refreshShopData() {
    this.globalData.settings = store.getSettings();
    this.globalData.products = store.getProducts();
  },

  globalData: {
    theme: null,
    pageStyle: '',
    settings: null,
    products: []
  }
});
