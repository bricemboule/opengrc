import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const BACKEND_TARGET = process.env.VITE_BACKEND_TARGET || "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      "/ws": {
        target: BACKEND_TARGET.replace(/^http/, "ws"),
        ws: true,
        changeOrigin: true,
      },
    },
  },
});
