<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
onMounted(() => shop.persist());
</script>
