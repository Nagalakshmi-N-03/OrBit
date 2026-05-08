/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        orbit: {
          primary: "#6366f1",
          secondary: "#8b5cf6",
          dark: "#0f0f1a",
          card: "#1a1a2e",
          border: "#2a2a3e",
          text: "#e2e8f0",
          muted: "#94a3b8",
          success: "#22c55e",
          error: "#ef4444",
          warning: "#f59e0b",
        }
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      }
    },
  },
  plugins: [],
}