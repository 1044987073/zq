/**
 * 复制本文件为 private.js（勿提交真实密钥到公开仓库）
 * 管理后台入口校验：口令 + 可选 OpenID 白名单（云开发登录后比对）
 */
module.exports = {
  /** 首次进入管理后台需输入的口令，请自行修改 */
  adminPassphrase: '请改成你的私密口令',
  /**
   * 云开发启用后，把管理员的 openid 填在这里，则仅这些人可进后台（口令可留空作二次验证）
   * 获取方式：云函数 login 返回 openid，或管理页「我的 OpenID」复制
   */
  adminOpenIds: []
};
