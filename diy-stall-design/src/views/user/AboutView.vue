<template>
  <div class="page">
    <h2 class="title">关于摊位</h2>
    <t-cell title="摊位" :note="shop.stallName" />
    <t-cell title="时间" :note="shop.openHours" />
    <template v-if="shop.wechatPayQr || shop.alipayPayQr">
      <h3>现场付款（可选）</h3>
      <img v-if="shop.wechatPayQr" :src="shop.wechatPayQr" alt="微信收款" class="qr" />
      <img v-if="shop.alipayPayQr" :src="shop.alipayPayQr" alt="支付宝" class="qr" />
    </template>
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
  margin: 0 0 8px;
}
h3 {
  margin: 20px 0 8px;
  font-size: 15px;
}
.qr {
  width: 100%;
  max-width: 200px;
  display: block;
  margin: 8px 0;
  border-radius: 8px;
}
</style>
