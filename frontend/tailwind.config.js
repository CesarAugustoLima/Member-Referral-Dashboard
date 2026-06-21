/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // brand colors
        copper: {
          DEFAULT: '#C17A5F',
          light: '#D49580',
          dark: '#A86249',
        },
        dark: {
          bg: '#1a1a1a',
          card: '#2a2a2a',
          border: '#374151',
        },
        success: {
          DEFAULT: '#10B981',
          light: '#34D399',
          dark: '#059669',
        },
        gray: {
          primary: '#FFFFFF',
          secondary: '#9CA3AF',
          tertiary: '#6B7280',
        },
      },
    },
  },
  plugins: [],
}
