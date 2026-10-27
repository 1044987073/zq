<template>
  <div class="login tdesign-demo__admin">
    <t-card title="管理后台登录" bordered>
      <t-form @submit="submit">
        <t-form-item label="口令">
          <t-input v-model="pass" type="password" placeholder="默认 demo123" />
        </t-form-item>
        <t-button theme="primary" type="submit" block>登录</t-button>
      </t-form>
      <t-button variant="text" block @click="$router.push('/')">返回用户端</t-button>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { MessagePlugin } from 'tdesign-vue-next';
import { useShopStore } from '@/stores/shop';

const pass = ref('');
const router = useRouter();
const shop = useShopStore();

function submit() {
  if (shop.login(pass.value)) {
    router.push('/admin');
  } else {
    MessagePlugin.error('口令错误');
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.login .t-card {
  width: 400px;
}
</style>
