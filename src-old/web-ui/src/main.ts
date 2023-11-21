import 'bootstrap/dist/css/bootstrap.css'
import {createApp, VueElement} from 'vue'
import App from './App.vue'
import 'bootstrap/dist/js/bootstrap'
import {createPinia} from 'pinia'
import {createWebHistory, createRouter} from 'vue-router'
import Login from './components/Login.vue'
import Users from './components/Users.vue'
import Rooms from './components/Rooms.vue'
import Purge from './components/Purge.vue'
import TestPage from './components/TestPage.vue'
import {useStore} from "./data/store";

const routes = [
    {path: '/login', component: Login},
    {path: '/users', component: Users},
    {path: '/rooms', component: Rooms},
    {path: '/purge', component: Purge},
    {path: '/test', component: TestPage},
];

export const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App)
    .use(createPinia())
    .use(router)
    .mount('#app');

// 路由特殊处理，没登录的情况下自动跳转到登陆界面
router.beforeEach((to, from) => {
    if (to.path == '/test')
        return;

    const store = useStore();
    if (to.path != "/login" && !store.isLogin)
        return '/login';
});
