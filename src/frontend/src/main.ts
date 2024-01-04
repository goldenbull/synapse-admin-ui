import './assets/main.css';

import axios from 'axios';
import {createApp} from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-green/theme.css';
import "primeflex/primeflex.css";
import Config from "@/components/Config.vue";
import Users from '@/components/Users.vue';
import Rooms from '@/components/Rooms.vue';
import Purge from '@/components/Purge.vue';
import TestPage from '@/components/TestPage.vue';
import {createRouter, createWebHistory} from "vue-router";
import {createPinia} from "pinia";
import {useStore} from "./data/store";

axios.defaults.baseURL = import.meta.env.VITE_APP_API_ENDPOINT;

axios.get("/echo").then(v => {
    console.log(v.data);
})

const routes = [
    {path: '/config', component: Config},
    {path: '/users', component: Users},
    {path: '/rooms', component: Rooms},
    {path: '/purge', component: Purge},
    {path: '/test', component: TestPage},
];

export const router = createRouter({
    history: createWebHistory(),
    routes,
});

createApp(App)
    .use(createPinia())
    .use(router)
    .use(PrimeVue)
    .mount('#app');

// 路由特殊处理，没登录的情况下自动跳转到登陆界面
// router.beforeEach((to: any, from: any) => {
//     if (to.path == '/test')
//         return;
//
//     const store = useStore();
//     if (to.path != "/login" && !store.isLogin)
//         return '/login';
// });
