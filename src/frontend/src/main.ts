import './assets/main.css';

import axios from 'axios';
import {createApp} from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';

axios.defaults.baseURL = import.meta.env.VITE_APP_API_ENDPOINT;
createApp(App).use(PrimeVue).mount('#app');
