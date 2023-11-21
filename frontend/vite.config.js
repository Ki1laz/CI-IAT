import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  devServer: {
    proxy: {
      '/static': {
        target: 'http://127.0.0.1:5000',  // Flask 后端的地址
        ws: true,
        changeOrigin: true
      }
    }
  }
})
