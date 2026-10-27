<template>
  <div class="page">
    <div class="hero">
      <h1>{{ shop.stallName }}</h1>
      <p>{{ shop.slogan }}</p>
      <t-tag theme="success" variant="light" size="small">{{ shop.isOpen ? '营业中' : '休息' }}</t-tag>
      <span class="hours">{{ shop.openHours }}</span>
    </div>
    <h3 class="section">主推体验</h3>
    <t-cell v-if="shop.featured" arrow @click="go(shop.featured!.id)">
      <template #title>{{ shop.featured!.name }}</template>
      <template #description>{{ shop.featured!.desc }}</template>
      <template #note>
        <span class="price">{{ shop.featured!.priceLabel }}</span>
      </template>
    </t-cell>
    <h3 class="section">全部项目</h3>
    <t-cell
      v-for="p in shop.productsForUser.slice(0, 5)"
      :key="p.id"
      arrow
      @click="go(p.id)"
    >
      <template #title>
        {{ p.name }}
        <t-tag v-if="p.tag" size="small" theme="primary" variant="light">{{ p.tag }}</t-tag>
      </template>
      <template #description>{{ p.duration }} · {{ p.age }}</template>
      <template #note><span class="price">{{ p.priceLabel }}</span></template>
    </t-cell>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
const router = useRouter();
function go(id: string) {
  router.push(`/product/${id}`);
}
</script>

<style scoped>
.page {
  padding: 16px;
}
.hero {
  background: var(--diy-primary);
  color: #fff;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
}
.hero h1 {
  margin: 0 0 8px;
  font-size: 20px;
}
.hero p {
  margin: 0 0 12px;
  font-size: 13px;
  opacity: 0.95;
}
.hours {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  opacity: 0.9;
}
.section {
  margin: 16px 0 8px;
  font-size: 15px;
}
.price {
  color: var(--diy-accent);
  font-weight: 600;
}
</style>
