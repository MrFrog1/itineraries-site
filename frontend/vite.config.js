import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

const cssFileName = 'index.min.css';

export default defineConfig({
  plugins: [react()],
  publicDir: './public',
  build: {
    assetsInclude: ['**/*.ttf', '**/*.otf', '**/*.woff', '**/*.woff2'],
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (
            assetInfo.name.endsWith('.ttf') ||
            assetInfo.name.endsWith('.otf') ||
            assetInfo.name.endsWith('.woff') ||
            assetInfo.name.endsWith('.woff2')
          ) {
            return 'assets/fonts/[name][extname]';
          }
          if (assetInfo.name.endsWith('.css')) {
            return `assets/css/${cssFileName}`;
          }
          return 'assets/[name][extname]';
        },
        entryFileNames: (file) => {
          return `assets/js/[name].min.js`;
        },
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});