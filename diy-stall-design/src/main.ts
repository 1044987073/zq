import { createApp } from 'vue';
import { createPinia } from 'pinia';
import TDesign from 'tdesign-vue-next';
import TDesignMobile from 'tdesign-mobile-vue';
import 'tdesign-vue-next/es/style/index.css';
import 'tdesign-mobile-vue/es/style/index.css';
import App from './App.vue';
import router from './router';
import './styles/theme.css';

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(TDesign);
app.use(TDesignMobile);
app.mount('#app');
