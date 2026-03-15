import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// If you prefer using a proxy instead of a full API base URL,
// uncomment the `server.proxy` section and call `/api/...` from the frontend.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    // proxy: {
    //   '/api': {
    //     target: 'http://localhost:8000',
    //     changeOrigin: true,
    //     rewrite: (path) => path.replace(/^\/api/, ''),
    //   },
    // },
  },
})
