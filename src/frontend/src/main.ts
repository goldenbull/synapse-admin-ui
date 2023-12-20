import './assets/main.css';

import axios from 'axios';
import {createApp} from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-green/theme.css';

axios.defaults.baseURL = import.meta.env.VITE_APP_API_ENDPOINT;

axios.get("/echo").then(v => {
    console.log(v.data);
})

createApp(App).use(PrimeVue).mount('#app');
