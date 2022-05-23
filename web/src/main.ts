import { createApp } from 'vue'
import App from './App.vue'
import {createProxyMiddleware} from 'http-proxy-middleware'

const app = createApp(App)
app.use(
    createProxyMiddleware('/v1' {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
        pathRewrite: {
            '^/v1': '/v1',
        },
    })
)

createApp(App).mount('#app')
