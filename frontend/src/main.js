import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue';
import routers from "@/routers";
import axios from 'axios';
import 'ant-design-vue/dist/reset.css';


const app = createApp(App)
app.config.globalProperties.axios = axios;

app.use(routers)
app.use(Antd)
app.mount('#app')
