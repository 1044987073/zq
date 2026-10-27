<template>
  <div class="user-shell tdesign-demo__user">
    <div class="phone">
      <router-view />
      <t-tab-bar v-model="active" fixed @change="onTab">
        <t-tab-bar-item value="home" icon="home">首页</t-tab-bar-item>
        <t-tab-bar-item value="catalog" icon="app">项目</t-tab-bar-item>
        <t-tab-bar-item value="bundles" icon="gift">套餐</t-tab-bar-item>
        <t-tab-bar-item value="about" icon="info-circle">关于</t-tab-bar-item>
      </t-tab-bar>
    </div>
    <div class="user-shell__aside">
      <p>用户端预览 · TDesign Mobile Vue</p>
      <t-button theme="primary" variant="outline" size="small" @click="$router.push('/admin/login')">
        管理后台
      </t-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const active = ref('home');

const map: Record<string, string> = {
  home: '/',
  catalog: '/catalog',
  bundles: '/bundles',
  about: '/about'
};

watch(
  () => route.name,
  (n) => {
    if (n === 'detail') return;
    if (n === 'home') active.value = 'home';
    else if (n === 'catalog') active.value = 'catalog';
    else if (n === 'bundles') active.value = 'bundles';
    else if (n === 'about') active.value = 'about';
  },
  { immediate: true }
);

function onTab(v: string | number) {
  const path = map[String(v)];
  if (path) router.push(path);
}
</script>

<style scoped>
.user-shell {
  min-height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 32px;
  padding: 24px;
}
.phone {
  width: 390px;
  min-height: 780px;
  background: var(--diy-bg);
  border-radius: 32px;
  box-shadow: 0 16px 48px rgba(45, 106, 79, 0.15);
  border: 10px solid #1d1d1f;
  overflow: hidden;
  position: relative;
  padding-bottom: 56px;
}
.user-shell__aside {
  max-width: 220px;
  padding-top: 40px;
  color: #52796f;
  font-size: 14px;
}
</style>
