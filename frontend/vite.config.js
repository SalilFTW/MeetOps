import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    // Disable PostCSS completely and rely strictly on standard CSS
    postcss: false,
  },
  server: {
    port: 5173,
  },
});
