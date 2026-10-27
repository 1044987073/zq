<template>
  <div v-if="product" class="page">
    <t-navbar title="项目详情" left-arrow @left-click="router.back()" />
    <div class="cover" />
    <h2>{{ product.name }}</h2>
    <p class="price">{{ product.priceLabel }}</p>
    <p class="muted">{{ product.duration }} · {{ product.age }}</p>
    <h3>玩法步骤</h3>
    <t-steps layout="vertical" :current="product.steps.length" readonly>
      <t-step-item v-for="(s, i) in product.steps" :key="i" :title="s" />
    </t-steps>
    <h3>说明</h3>
    <p class="muted">{{ product.desc }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useShopStore } from '@/stores/shop';

const route = useRoute();
const router = useRouter();
const shop = useShopStore();
const product = computed(() => shop.productsForUser.find((p) => p.id === route.params.id));
</script>

<style scoped>
.page {
  padding: 0 16px 24px;
}
.cover {
  height: 160px;
  background: var(--diy-secondary, #d8f3dc);
  border-radius: 12px;
  margin: 12px 0;
}
.price {
  color: var(--diy-accent);
  font-weight: 700;
  font-size: 18px;
}
.muted {
  color: #52796f;
  font-size: 13px;
}
h3 {
  font-size: 15px;
  margin: 20px 0 8px;
}
</style>
