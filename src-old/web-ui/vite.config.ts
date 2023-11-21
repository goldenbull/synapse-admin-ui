import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({mode}) => {
    process.env = {...process.env, ...loadEnv(mode, process.cwd())};
    return {
        plugins: [vue()],
        server: {
            proxy: {
                // Using the proxy instance
                '/proxy': {
                    target: process.env.VITE_SYNAPSE_SERVER,
                    changeOrigin: true,
                    secure: false,
                    rewrite: (path) => path.replace(/^\/proxy/, '')
                }
            }
        }
    };
})