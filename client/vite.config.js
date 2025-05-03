// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag === 'deep-chat'
        }
      }
    })
  ],
  server: {
    allowedHosts: ['916c-31-207-9-142.ngrok-free.app'] // <-- add this line
  },
  test: {
    globals: true,
    environment: 'jsdom',
    testMatch: [
      'src/**/*.spec.js',
      'tests/**/*.spec.js'
    ]
  }
})