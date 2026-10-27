<template>
  <t-layout class="admin tdesign-demo__admin">
    <t-aside width="220px">
      <div class="admin-brand">公园 DIY · 管理</div>
      <t-menu :value="active" @change="onMenu">
        <t-menu-item value="admin-dash">控制台</t-menu-item>
        <t-menu-item value="admin-products">商品管理</t-menu-item>
        <t-menu-item value="admin-theme">主题配色</t-menu-item>
      </t-menu>
      <t-button class="logout" theme="danger" variant="outline" block @click="logout">退出</t-button>
    </t-aside>
    <t-layout>
      <t-header class="admin-header">
        <span>TDesign Vue Next · 与即时设计物料一致</span>
        <t-button variant="text" @click="$router.push('/')">预览用户端</t-button>
      </t-header>
      <t-content class="admin-content">
        <router-view />
      </t-content>
    </t-layout>
  </t-layout>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useShopStore } from '@/stores/shop';

const route = useRoute();
const router = useRouter();
const shop = useShopStore();

const active = computed(() => String(route.name || 'admin-dash'));

function onMenu(v: string) {
  router.push({ name: v });
}

function logout() {
  shop.logout();
  router.push('/admin/login');
}
</script>

<style scoped>
.admin {
  min-height: 100vh;
}
.admin-brand {
  padding: 20px 16px;
  font-weight: 700;
  color: var(--diy-primary);
}
.logout {
  margin: 24px 16px;
  width: calc(100% - 32px);
}
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e7e7e7;
}
.admin-content {
  padding: 24px;
  background: #f5f6f7;
}
</style>
