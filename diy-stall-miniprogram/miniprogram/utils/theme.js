/** 设计令牌默认值 — 与 docs/UI-DESIGN.md 一致，管理端可改并持久化 */
const DEFAULT_THEME = {
  primary: '#2D6A4F',
  primaryLight: '#52B788',
  secondary: '#D8F3DC',
  accent: '#F4A261',
  background: '#F7F9F8',
  surface: '#FFFFFF',
  text: '#1B4332',
  textMuted: '#52796F',
  danger: '#E76F51',
  radius: 16
};

const STORAGE_KEY = 'shopTheme';

function hexToRgba(hex, alpha) {
  const h = hex.replace('#', '');
  const full = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
  const n = parseInt(full, 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

function themeToPageStyle(theme) {
  const t = { ...DEFAULT_THEME, ...theme };
  return [
    `--color-primary:${t.primary}`,
    `--color-primary-light:${t.primaryLight}`,
    `--color-secondary:${t.secondary}`,
    `--color-accent:${t.accent}`,
    `--color-bg:${t.background}`,
    `--color-surface:${t.surface}`,
    `--color-text:${t.text}`,
    `--color-text-muted:${t.textMuted}`,
    `--color-danger:${t.danger}`,
    `--radius-md:${t.radius}rpx`,
    `--shadow-card:0 8rpx 32rpx ${hexToRgba(t.primary, 0.08)}`,
    `--van-primary-color:${t.primary}`,
    `--van-button-primary-background-color:${t.primary}`,
    `--van-button-primary-border-color:${t.primary}`,
    `--td-brand-color:${t.primary}`
  ].join(';');
}

function loadTheme() {
  try {
    const stored = wx.getStorageSync(STORAGE_KEY);
    if (stored && typeof stored === 'object') {
      return { ...DEFAULT_THEME, ...stored };
    }
  } catch (e) {
    /* ignore */
  }
  return { ...DEFAULT_THEME };
}

function saveTheme(partial) {
  const next = { ...loadTheme(), ...partial };
  wx.setStorageSync(STORAGE_KEY, next);
  const app = getApp();
  if (app) {
    app.globalData.theme = next;
    app.globalData.pageStyle = themeToPageStyle(next);
  }
  return next;
}

function applyThemeToApp(app) {
  const theme = loadTheme();
  app.globalData.theme = theme;
  app.globalData.pageStyle = themeToPageStyle(theme);
}

module.exports = {
  DEFAULT_THEME,
  STORAGE_KEY,
  themeToPageStyle,
  loadTheme,
  saveTheme,
  applyThemeToApp,
  hexToRgba
};
