import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// GitHub Pages subpath: https://sinonmoe.github.io/k5-day9-instructor-slides/
export default defineConfig({
  plugins: [react()],
  base: '/k5-day9-instructor-slides/',
})
