const Toast = require('@vant/weapp/toast/toast');
const auth = require('../../utils/auth');
const { loadTheme, saveTheme, themeToPageStyle, DEFAULT_THEME } = require('../../utils/theme');

const PRESETS = [
  { name: '森林绿（默认）', ...DEFAULT_THEME },
  {
    name: '秋日南瓜',
    primary: '#BC6C25',
    primaryLight: '#DDA15E',
    secondary: '#FEFAE0',
    accent: '#606C38',
    background: '#FFFBF5',
    surface: '#FFFFFF',
    text: '#283618',
    textMuted: '#606C38',
    danger: '#BC4749',
    radius: 16
  },
  {
    name: '海洋蓝',
    primary: '#0077B6',
    primaryLight: '#48CAE4',
    secondary: '#CAF0F8',
    accent: '#FFB703',
    background: '#F8FCFD',
    surface: '#FFFFFF',
    text: '#023047',
    textMuted: '#457B9D',
    danger: '#E63946',
    radius: 16
  },
  {
    name: '樱花粉',
    primary: '#C9184A',
    primaryLight: '#FF4D6D',
    secondary: '#FFE5EC',
    accent: '#590D22',
    background: '#FFF8FA',
    surface: '#FFFFFF',
    text: '#590D22',
    textMuted: '#A4133C',
    danger: '#E5383B',
    radius: 20
  }
];

Page({
  data: {
    pageStyle: '',
    theme: {},
    presets: PRESETS
  },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const theme = loadTheme();
    this.setData({
      theme,
      pageStyle: themeToPageStyle(theme)
    });
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: theme.primary
    });
  },

  onThemeField(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({
      theme: { ...this.data.theme, [key]: e.detail },
      pageStyle: themeToPageStyle({ ...this.data.theme, [key]: e.detail })
    });
  },

  applyPreset(e) {
    const idx = Number(e.currentTarget.dataset.index);
    const t = PRESETS[idx];
    if (!t) return;
    this.setData({ theme: t, pageStyle: themeToPageStyle(t) });
  },

  save() {
    saveTheme(this.data.theme);
    Toast.success('已保存');
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: this.data.theme.primary
    });
  }
});
