import { createRouter, createWebHistory } from 'vue-router';
import { useShopStore } from '@/stores/shop';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/UserLayout.vue'),
      children: [
        { path: '', name: 'home', component: () => import('@/views/user/HomeView.vue') },
        { path: 'catalog', name: 'catalog', component: () => import('@/views/user/CatalogView.vue') },
        { path: 'product/:id', name: 'detail', component: () => import('@/views/user/DetailView.vue') },
        { path: 'bundles', name: 'bundles', component: () => import('@/views/user/BundlesView.vue') },
        { path: 'about', name: 'about', component: () => import('@/views/user/AboutView.vue') }
      ]
    },
    { path: '/admin/login', name: 'admin-login', component: () => import('@/views/admin/LoginView.vue') },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        { path: '', name: 'admin-dash', component: () => import('@/views/admin/DashboardView.vue') },
        { path: 'products', name: 'admin-products', component: () => import('@/views/admin/ProductsView.vue') },
        { path: 'theme', name: 'admin-theme', component: () => import('@/views/admin/ThemeView.vue') }
      ]
    }
  ]
});

router.beforeEach((to) => {
  if (to.meta.requiresAdmin) {
    const shop = useShopStore();
    if (!shop.adminSession) return { name: 'admin-login' };
  }
  return true;
});

export default router;
