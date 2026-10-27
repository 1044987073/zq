<template>
  <div>
    <t-button theme="primary" @click="shop.addProduct()">新增商品</t-button>
    <t-collapse v-model="expanded" class="mt">
      <t-collapse-panel v-for="p in shop.products" :key="p.id" :value="p.id" :header="p.name">
        <t-form label-width="100px">
          <t-form-item label="名称">
            <t-input v-model="p.name" @blur="shop.updateProduct(p.id, { name: p.name })" />
          </t-form-item>
          <t-form-item label="售价">
            <t-input-number v-model="p.price" @change="shop.updateProduct(p.id, { price: p.price })" />
          </t-form-item>
          <t-form-item label="展示价">
            <t-input v-model="p.priceLabel" @blur="shop.updateProduct(p.id, { priceLabel: p.priceLabel })" />
          </t-form-item>
          <t-form-item label="库存">
            <t-input-number
              :value="p.stock ?? undefined"
              placeholder="空=不限"
              @change="(v: number) => shop.updateProduct(p.id, { stock: v })"
            />
          </t-form-item>
          <t-form-item label="玩法说明">
            <t-textarea v-model="p.desc" @blur="shop.updateProduct(p.id, { desc: p.desc })" />
          </t-form-item>
          <t-form-item label="步骤">
            <t-textarea
              :model-value="p.steps.join('\n')"
              placeholder="每行一步"
              @blur="(val: string) => shop.updateProduct(p.id, { steps: String(val).split('\n').map((s) => s.trim()).filter(Boolean) })"
            />
          </t-form-item>
          <t-form-item label="上架">
            <t-switch v-model="p.enabled" @change="shop.updateProduct(p.id, { enabled: p.enabled })" />
          </t-form-item>
          <t-form-item label="封面图">
            <input type="file" accept="image/*" @change="(e) => onFile(e, p.id)" />
          </t-form-item>
        </t-form>
      </t-collapse-panel>
    </t-collapse>
    <t-card title="收款码（可选）" class="mt">
      <p class="hint">上传后用户端「关于」页展示</p>
      <t-upload theme="image" :auto-upload="false" @change="onWechat" />
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useShopStore } from '@/stores/shop';

const shop = useShopStore();
const expanded = ref<string[]>([]);

function onFile(e: Event, id: string) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  shop.updateProduct(id, { cover: url });
}

function onWechat(files: { url?: string }[]) {
  if (files[0]?.url) {
    shop.wechatPayQr = files[0].url;
    shop.persist();
  }
}
</script>

<style scoped>
.mt {
  margin-top: 16px;
}
.hint {
  color: #888;
  font-size: 13px;
}
</style>
