/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // 10east.co uses Signifier for display; Amiri is in their stack and on Google Fonts.
        serif: ['Amiri', 'Georgia', 'serif'],
        // Primary sans on 10east.co
        sans: ['"Libre Franklin"', 'Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        // Brand copper from 10east.co (#B37D4F, gradient #c78b58 → #956a68)
        copper: {
          DEFAULT: '#B37D4F',
          light: '#C78B58',
          dark: '#956A68',
        },
        dark: {
          bg: '#1C1C1C',
          card: '#272727',
          border: '#3F3F3F',
        },
        success: {
          DEFAULT: '#10B981',
          light: '#34D399',
          dark: '#059669',
        },
        gray: {
          primary: '#FBFBFB',
          secondary: '#A3A3A3',
          tertiary: '#737373',
        },
      },
    },
  },
  plugins: [],
}
