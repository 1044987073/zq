const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: {
    pageStyle: '',
    settings: {},
    summary: { count: 0, revenue: 0, profit: 0 }
  },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const today = store.formatDate(Date.now());
    const summary = store.ledgerSummaryByDate(today);
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      settings: store.getSettings(),
      summary: {
        count: summary.count,
        revenue: summary.revenue.toFixed(0),
        profit: summary.profit.toFixed(0)
      }
    });
  },

  onField(e) {
    const key = e.currentTarget.dataset.key;
    store.saveSettings({ [key]: e.detail });
    this.setData({ settings: store.getSettings() });
  },

  onOpenToggle(e) {
    store.saveSettings({ isOpen: e.detail });
    this.setData({ settings: store.getSettings() });
  },

  logout() {
    auth.clearSession();
    wx.redirectTo({ url: '/pages-admin/login/login' });
  }
});
