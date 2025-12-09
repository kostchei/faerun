/**
 * Path: client/vite.config.ts
 * Purpose: Vite build tool configuration
 * Logic:
 *   - Dev server on port 5173
 *   - host: true enables network access (mobile testing)
 *   - Build target: esnext for modern browsers
 */

import { defineConfig } from 'vite'

export default defineConfig({
    server: {
        port: 5173,
        host: true
    },
    build: {
        target: 'esnext'
    }
})
