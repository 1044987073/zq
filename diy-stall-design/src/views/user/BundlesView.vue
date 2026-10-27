<template>
  <div class="page">
    <h2 class="title">优惠套餐</h2>
    <t-card v-for="b in shop.bundles" :key="b.id" bordered class="combo">
      <div class="combo-head">
        <span>{{ b.name }}</span>
        <span class="price">¥{{ b.price }}</span>
      </div>
      <t-tag v-for="item in b.items" :key="item" variant="outline" size="small">{{ item }}</t-tag>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
</script>

<style scoped>
.page {
  padding: 16px;
}
.title {
  margin: 0 0 12px;
}
.combo {
  margin-bottom: 12px;
}
.combo-head {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  margin-bottom: 8px;
}
.price {
  color: var(--diy-accent);
  font-size: 20px;
}
</style>
