const SESSION_KEY = 'adminSession';
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;

function getPrivateConfig() {
  try {
    return require('../config/private.js');
  } catch (e) {
    return require('../config/private.example.js');
  }
}

function createSession() {
  const session = {
    role: 'admin',
    createdAt: Date.now(),
    expiresAt: Date.now() + SESSION_TTL_MS
  };
  wx.setStorageSync(SESSION_KEY, session);
  return session;
}

function clearSession() {
  wx.removeStorageSync(SESSION_KEY);
}

function getSession() {
  try {
    const s = wx.getStorageSync(SESSION_KEY);
    if (!s || !s.expiresAt || Date.now() > s.expiresAt) {
      clearSession();
      return null;
    }
    return s;
  } catch (e) {
    return null;
  }
}

function isAdminLoggedIn() {
  return !!getSession();
}

/**
 * @param {string} passphrase
 * @returns {Promise<{ok: boolean, message?: string, openid?: string}>}
 */
function verifyAdminLogin(passphrase) {
  const cfg = getPrivateConfig();
  return new Promise((resolve) => {
    const trimmed = (passphrase || '').trim();
    if (!trimmed || trimmed !== cfg.adminPassphrase) {
      resolve({ ok: false, message: '口令错误' });
      return;
    }

    const openIds = cfg.adminOpenIds || [];
    if (openIds.length === 0) {
      createSession();
      resolve({ ok: true });
      return;
    }

    if (!wx.cloud || !wx.cloud.callFunction) {
      resolve({
        ok: false,
        message: '已配置 OpenID 白名单，请先开通云开发并部署 login 云函数'
      });
      return;
    }

    wx.cloud
      .callFunction({ name: 'login' })
      .then((res) => {
        const openid = res.result && res.result.openid;
        if (openid && openIds.includes(openid)) {
          createSession();
          resolve({ ok: true, openid });
        } else {
          resolve({ ok: false, message: '当前微信不是管理员账号' });
        }
      })
      .catch(() => {
        resolve({ ok: false, message: '登录校验失败，请检查云函数' });
      });
  });
}

function requireAdmin(pageInstance) {
  if (isAdminLoggedIn()) return true;
  wx.showToast({ title: '请先登录管理后台', icon: 'none' });
  wx.redirectTo({ url: '/pages-admin/login/login' });
  return false;
}

function fetchOpenIdForDisplay() {
  if (!wx.cloud || !wx.cloud.callFunction) {
    return Promise.resolve('');
  }
  return wx.cloud
    .callFunction({ name: 'login' })
    .then((res) => (res.result && res.result.openid) || '')
    .catch(() => '');
}

module.exports = {
  verifyAdminLogin,
  isAdminLoggedIn,
  requireAdmin,
  clearSession,
  getSession,
  fetchOpenIdForDisplay,
  getPrivateConfig
};
