/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#F8FAFC',
        surface: 'rgba(255,255,255,0.68)',
        border: 'rgba(255,255,255,0.25)',
        textPrimary: '#0F172A',
        textSecondary: '#475569',
        muted: '#94A3B8',
        primary: '#0F766E', // Deep Teal
        secondary: '#14532D', // Evergreen
        accent: '#2563EB', // Ocean Blue
        success: '#16A34A',
        warning: '#D97706',
        danger: '#DC2626',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 4px 30px rgba(0, 0, 0, 0.05)',
        'glass-hover': '0 8px 32px rgba(0, 0, 0, 0.08)',
      }
    },
  },
  plugins: [],
}
