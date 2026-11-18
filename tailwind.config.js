/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          bg: '#FAFAFA',
          surface: '#FFFFFF',
          charcoal: '#111827',
          slate: '#4B5563',
          teal: '#0F766E',
          tealHover: '#0D645E',
          tealActive: '#0B534E',
          tealLight: '#F0FDFA',
          border: '#E5E7EB',
        }
      },
      fontFamily: {
        heading: ['"Plus Jakarta Sans"', 'sans-serif'],
        sans: ['"Inter"', 'sans-serif'],
      },
      keyframes: {
        pulseAmber: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.65', transform: 'scale(0.97)' },
        }
      },
      animation: {
        'pulse-amber': 'pulseAmber 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
