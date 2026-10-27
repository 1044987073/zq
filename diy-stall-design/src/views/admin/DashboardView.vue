<template>
  <div>
    <t-row :gutter="16">
      <t-col :span="4">
        <t-card title="摊位名">
          <t-input v-model="shop.stallName" @blur="shop.persist()" />
        </t-card>
      </t-col>
      <t-col :span="4">
        <t-card title="营业">
          <t-switch v-model="shop.isOpen" @change="shop.persist()" />
        </t-card>
      </t-col>
      <t-col :span="4">
        <t-card title="商品数">
          <div class="stat">{{ shop.products.length }}</div>
        </t-card>
      </t-col>
    </t-row>
    <t-card title="标语 / 营业时间" class="mt">
      <t-textarea v-model="shop.slogan" placeholder="标语" @blur="shop.persist()" />
      <t-input v-model="shop.openHours" class="mt" @blur="shop.persist()" />
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
</script>

<style scoped>
.stat {
  font-size: 32px;
  font-weight: 700;
  color: var(--diy-primary);
}
.mt {
  margin-top: 16px;
}
</style>
