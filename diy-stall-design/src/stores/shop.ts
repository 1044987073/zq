import { defineStore } from 'pinia';
import { defaultBundles, defaultProducts, type Product } from '@/data/defaults';

const LS = 'diy-stall-design-v1';

function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(`${LS}:${key}`);
    if (raw) return JSON.parse(raw) as T;
  } catch {
    /* ignore */
  }
  return fallback;
}

function save(key: string, value: unknown) {
  localStorage.setItem(`${LS}:${key}`, JSON.stringify(value));
}

export const useShopStore = defineStore('shop', {
  state: () => ({
    stallName: load('stallName', '公园手工 DIY 小摊'),
    slogan: load('slogan', '砸石膏 · 涂面具 · 把创意带回家'),
    openHours: load('openHours', '16:00 – 20:00'),
    isOpen: load('isOpen', true),
    products: load<Product[]>('products', defaultProducts),
    bundles: load('bundles', defaultBundles),
    theme: load('theme', {
      primary: '#2d6a4f',
      accent: '#f4a261'
    }),
    adminPass: load('adminPass', 'demo123'),
    adminSession: false,
    wechatPayQr: load<string>('wechatPayQr', ''),
    alipayPayQr: load<string>('alipayPayQr', '')
  }),
  getters: {
    productsForUser: (s) => s.products.filter((p) => p.enabled),
    featured: (s) =>
      s.products.find((p) => p.enabled && p.tag === '招牌') || s.products.find((p) => p.enabled)
  },
  actions: {
    persist() {
      save('stallName', this.stallName);
      save('slogan', this.slogan);
      save('openHours', this.openHours);
      save('isOpen', this.isOpen);
      save('products', this.products);
      save('bundles', this.bundles);
      save('theme', this.theme);
      save('wechatPayQr', this.wechatPayQr);
      save('alipayPayQr', this.alipayPayQr);
      document.documentElement.style.setProperty('--diy-primary', this.theme.primary);
      document.documentElement.style.setProperty('--diy-accent', this.theme.accent);
    },
    login(pass: string) {
      if (pass === this.adminPass) {
        this.adminSession = true;
        return true;
      }
      return false;
    },
    logout() {
      this.adminSession = false;
    },
    updateProduct(id: string, patch: Partial<Product>) {
      this.products = this.products.map((p) => (p.id === id ? { ...p, ...patch } : p));
      this.persist();
    },
    addProduct() {
      const id = `p-${Date.now()}`;
      this.products.push({
        id,
        name: '新商品',
        price: 0,
        priceLabel: '面议',
        cost: 0,
        stock: null,
        enabled: true,
        tag: '',
        duration: '',
        age: '',
        cover: '',
        steps: ['现场体验'],
        desc: ''
      });
      this.persist();
    }
  }
});
