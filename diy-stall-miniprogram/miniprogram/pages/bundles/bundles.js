const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: { pageStyle: '', bundles: [] },
  onShow() {
    const theme = loadTheme();
    this.setData({
      pageStyle: themeToPageStyle(theme),
      bundles: store.getBundles()
    });
  }
});
