/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./**/*.html', '!./node_modules/**'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Rubik', 'sans-serif'],
        body: ['Nunito Sans', 'sans-serif'],
      },
      colors: {
        primary: '#2563EB',
        'primary-dark': '#1D4ED8',
        secondary: '#3B82F6',
        accent: '#059669',
        'accent-dark': '#047857',
        surface: '#F8FAFC',
        muted: '#F1F5FD',
        border: '#E4ECFC',
        foreground: '#0F172A',
        'dark-surface': '#0B1120',
        'dark-card': '#111827',
        'dark-elevated': '#1A2235',
        'dark-border': '#1E293B',
        'dark-muted': '#334155',
        'dark-foreground': '#F1F5F9',
        'dark-dim': '#94A3B8',
      },
      boxShadow: {
        soft: '0 10px 40px -10px rgba(37, 99, 235, 0.15)',
        glow: '0 0 40px rgba(37, 99, 235, 0.15)',
      },
      animation: {
        float: 'float 6s ease-in-out infinite',
        glow: 'glow 4s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%, 100%': { opacity: '0.45' },
          '50%': { opacity: '0.8' },
        },
      },
    },
  },
  plugins: [],
};
