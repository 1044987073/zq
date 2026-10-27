<template>
  <t-card title="主题配色（Design Token）">
    <t-form label-width="120px">
      <t-form-item label="主色">
        <t-color-picker v-model="shop.theme.primary" format="HEX" @change="shop.persist()" />
      </t-form-item>
      <t-form-item label="强调色">
        <t-color-picker v-model="shop.theme.accent" format="HEX" @change="shop.persist()" />
      </t-form-item>
    </t-form>
    <p class="hint">与即时设计中使用 TDesign 变量、小程序 theme.js 保持一致命名习惯。</p>
  </t-card>
</template>

<script setup lang="ts">
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
</script>

<style scoped>
.hint {
  margin-top: 16px;
  color: #666;
  font-size: 13px;
}
</style>
