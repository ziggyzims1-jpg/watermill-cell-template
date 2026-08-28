import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000',
    },
  },
  build: {
    outDir: '../static/dist',
    emptyOutDir: true,
  },
  // Vitest shares this config so tests resolve modules exactly as the build
  // does. TZ is pinned west of Greenwich on purpose: CI runners are UTC, the
  // one zone where parse-as-UTC/read-as-local date bugs cannot appear.
  test: {
    environment: 'jsdom',
    globals: true,
    env: { TZ: 'America/New_York' },
    include: ['src/__tests__/**/*.test.{js,jsx}'],
    sequence: { shuffle: false },
    restoreMocks: true,
    testTimeout: 10000,
  },
})
