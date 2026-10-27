<template>
  <div class="page">
    <h2 class="title">全部项目</h2>
    <t-cell v-for="p in shop.productsForUser" :key="p.id" arrow @click="go(p.id)">
      <template #title>{{ p.name }}</template>
      <template #description>{{ p.desc }}</template>
      <template #note>
        <span class="price">{{ p.priceLabel }}</span>
        <span v-if="p.stock === 0" class="sold">售罄</span>
        <span v-else-if="p.stock != null" class="stock">剩 {{ p.stock }}</span>
      </template>
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
.title {
  margin: 0 0 12px;
  font-size: 18px;
}
.price {
  color: var(--diy-accent);
  font-weight: 600;
}
.stock,
.sold {
  display: block;
  font-size: 11px;
  color: #888;
}
</style>
