const Toast = require('@vant/weapp/toast/toast');
const auth = require('../../utils/auth');
const store = require('../../utils/store');
const { loadTheme, themeToPageStyle } = require('../../utils/theme');

Page({
  data: {
    pageStyle: '',
    form: { productName: '', qty: 1, price: '', cost: '', note: '' },
    productNames: [],
    pickerLabel: '点击选择',
    rows: []
  },

  onShow() {
    if (!auth.requireAdmin(this)) return;
    const products = store.getProducts();
    const today = store.formatDate(Date.now());
    const summary = store.ledgerSummaryByDate(today);
    const rows = summary.rows.map((r) => ({
      ...r,
      amount: ((r.price || 0) * (r.qty || 1)).toFixed(0),
      time: new Date(r.createdAt).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    }));
    this.setData({
      pageStyle: themeToPageStyle(loadTheme()),
      productNames: products.map((p) => p.name),
      rows
    });
  },

  onForm(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ form: { ...this.data.form, [key]: e.detail } });
  },

  pickProduct(e) {
    const idx = Number(e.detail.value);
    const name = this.data.productNames[idx];
    const p = store.getProducts().find((x) => x.name === name);
    this.setData({
      pickerLabel: name,
      form: {
        ...this.data.form,
        productName: name,
        price: p ? String(p.price) : this.data.form.price,
        cost: p ? String(p.cost) : this.data.form.cost
      }
    });
  },

  submit() {
    const f = this.data.form;
    if (!f.productName || !f.price) {
      Toast.fail('请填写项目和实收单价');
      return;
    }
    const qty = Number(f.qty) || 1;
    store.addLedgerEntry({
      productName: f.productName,
      qty,
      price: Number(f.price),
      cost: Number(f.cost) || 0,
      note: f.note || ''
    });
    store.adjustStockByProductName(f.productName, -qty);
    Toast.success('已记账');
    this.setData({ form: { productName: '', qty: 1, price: '', cost: '', note: '' }, pickerLabel: '点击选择' });
    this.onShow();
  }
});
