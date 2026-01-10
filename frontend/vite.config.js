import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({mode}) => {
    const isCI = mode === 'ci'
    return {
    base: isCI ? '/ROLe/' : '/',
    plugins: [
      react(),
      tailwindcss(),
    ],
    // api remover if /api in url, return 0.0.0.0:7878
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:7878',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '') // remove /api
        }
      },
      host: "127.0.0.1",
      port: 5173
    }
  }
})
