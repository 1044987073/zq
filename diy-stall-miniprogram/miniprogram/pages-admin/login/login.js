const Toast = require('@vant/weapp/toast/toast');
const auth = require('../../utils/auth');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: {
    pageStyle: '',
    passphrase: '',
    loading: false,
    openid: ''
  },

  onLoad() {
    if (auth.isAdminLoggedIn()) {
      wx.redirectTo({ url: '/pages-admin/dashboard/dashboard' });
      return;
    }
    this.setData({ pageStyle: themeToPageStyle(loadTheme()) });
  },

  onPassChange(e) {
    this.setData({ passphrase: e.detail });
  },

  async onSubmit() {
    this.setData({ loading: true });
    const res = await auth.verifyAdminLogin(this.data.passphrase);
    this.setData({ loading: false });
    if (res.ok) {
      Toast.success('登录成功');
      setTimeout(() => {
        wx.redirectTo({ url: '/pages-admin/dashboard/dashboard' });
      }, 400);
    } else {
      Toast.fail(res.message || '登录失败');
    }
  },

  async loadOpenId() {
    const openid = await auth.fetchOpenIdForDisplay();
    if (openid) {
      this.setData({ openid });
      wx.setClipboardData({ data: openid });
    } else {
      Toast('未开通云开发时无法获取 OpenID');
    }
  }
});
