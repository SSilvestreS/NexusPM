/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Habilita modo escuro baseado em classes
  theme: {
    extend: {
      // Cores personalizadas
      colors: {
        primary: {
          50: 'var(--primary-50)',
          100: 'var(--primary-100)',
          200: 'var(--primary-200)',
          300: 'var(--primary-300)',
          400: 'var(--primary-400)',
          500: 'var(--primary-500)',
          600: 'var(--primary-600)',
          700: 'var(--primary-700)',
          800: 'var(--primary-800)',
          900: 'var(--primary-900)',
        },
        neutral: {
          50: 'var(--neutral-50)',
          100: 'var(--neutral-100)',
          200: 'var(--neutral-200)',
          300: 'var(--neutral-300)',
          400: 'var(--neutral-400)',
          500: 'var(--neutral-500)',
          600: 'var(--neutral-600)',
          700: 'var(--neutral-700)',
          800: 'var(--neutral-800)',
          900: 'var(--neutral-900)',
        },
        success: {
          50: 'var(--success-50)',
          100: 'var(--success-100)',
          200: 'var(--success-200)',
          300: 'var(--success-300)',
          400: 'var(--success-400)',
          500: 'var(--success-500)',
          600: 'var(--success-600)',
          700: 'var(--success-700)',
          800: 'var(--success-800)',
          900: 'var(--success-900)',
        },
        warning: {
          50: 'var(--warning-50)',
          100: 'var(--warning-100)',
          200: 'var(--warning-200)',
          300: 'var(--warning-300)',
          400: 'var(--warning-400)',
          500: 'var(--warning-500)',
          600: 'var(--warning-600)',
          700: 'var(--warning-700)',
          800: 'var(--warning-800)',
          900: 'var(--warning-900)',
        },
        error: {
          50: 'var(--error-50)',
          100: 'var(--error-100)',
          200: 'var(--error-200)',
          300: 'var(--error-300)',
          400: 'var(--error-400)',
          500: 'var(--error-500)',
          600: 'var(--error-600)',
          700: 'var(--error-700)',
          800: 'var(--error-800)',
          900: 'var(--error-900)',
        },
        info: {
          50: 'var(--info-50)',
          100: 'var(--info-100)',
          200: 'var(--info-200)',
          300: 'var(--info-300)',
          400: 'var(--info-400)',
          500: 'var(--info-500)',
          600: 'var(--info-600)',
          700: 'var(--info-700)',
          800: 'var(--info-800)',
          900: 'var(--info-900)',
        },
      },
      // Fonte personalizada
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'],
      },
      // Sombras personalizadas
      boxShadow: {
        'sm': 'var(--shadow-sm)',
        'md': 'var(--shadow-md)',
        'lg': 'var(--shadow-lg)',
        'xl': 'var(--shadow-xl)',
      },
      // Bordas personalizadas
      borderRadius: {
        'sm': 'var(--border-radius-sm)',
        'md': 'var(--border-radius-md)',
        'lg': 'var(--border-radius-lg)',
        'xl': 'var(--border-radius-xl)',
        '2xl': 'var(--border-radius-2xl)',
      },
      // Espaçamentos personalizados
      spacing: {
        'xs': 'var(--spacing-xs)',
        'sm': 'var(--spacing-sm)',
        'md': 'var(--spacing-md)',
        'lg': 'var(--spacing-lg)',
        'xl': 'var(--spacing-xl)',
        '2xl': 'var(--spacing-2xl)',
        '3xl': 'var(--spacing-3xl)',
      },
      // Animações personalizadas
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin': 'spin 1s linear infinite',
        'bounce': 'bounce 1s infinite',
        'ping': 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
        'pong': 'pong 1s cubic-bezier(0, 0, 0.2, 1) infinite',
      },
      // Transições personalizadas
      transitionDuration: {
        'fast': 'var(--transition-fast)',
        'normal': 'var(--transition-normal)',
        'slow': 'var(--transition-slow)',
      },
      // Breakpoints personalizados
      screens: {
        'xs': '475px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
      // Grid personalizado
      gridTemplateColumns: {
        'auto-fit': 'repeat(auto-fit, minmax(250px, 1fr))',
        'auto-fill': 'repeat(auto-fill, minmax(200px, 1fr))',
      },
      // Flexbox personalizado
      flex: {
        '2': '2 2 0%',
        '3': '3 3 0%',
        '4': '4 4 0%',
      },
      // Z-index personalizado
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },
      // Backdrop blur personalizado
      backdropBlur: {
        'xs': '2px',
      },
      // Skeleton loading
      keyframes: {
        'shimmer': {
          '100%': {
            transform: 'translateX(100%)',
          },
        },
        'pulse-soft': {
          '0%, 100%': {
            opacity: '1',
          },
          '50%': {
            opacity: '0.8',
          },
        },
      },
      animation: {
        'shimmer': 'shimmer 1.5s infinite',
        'pulse-soft': 'pulse-soft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [
    // Plugin para scrollbar personalizada
    function({ addUtilities }) {
      const newUtilities = {
        '.scrollbar-thin': {
          scrollbarWidth: 'thin',
          scrollbarColor: 'var(--neutral-300) var(--neutral-100)',
        },
        '.scrollbar-thin::-webkit-scrollbar': {
          width: '8px',
          height: '8px',
        },
        '.scrollbar-thin::-webkit-scrollbar-track': {
          background: 'var(--neutral-100)',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb': {
          background: 'var(--neutral-300)',
          borderRadius: 'var(--border-radius-md)',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb:hover': {
          background: 'var(--neutral-400)',
        },
        '.dark .scrollbar-thin::-webkit-scrollbar-track': {
          background: 'var(--neutral-800)',
        },
        '.dark .scrollbar-thin::-webkit-scrollbar-thumb': {
          background: 'var(--neutral-600)',
        },
        '.dark .scrollbar-thin::-webkit-scrollbar-thumb:hover': {
          background: 'var(--neutral-500)',
        },
      }
      addUtilities(newUtilities)
    },
    // Plugin para animações de entrada
    function({ addUtilities }) {
      const newUtilities = {
        '.animate-in': {
          animation: 'fadeIn 0.3s ease-out',
        },
        '.animate-in-up': {
          animation: 'fadeInUp 0.3s ease-out',
        },
        '.animate-in-down': {
          animation: 'fadeInDown 0.3s ease-out',
        },
        '.animate-in-left': {
          animation: 'fadeInLeft 0.3s ease-out',
        },
        '.animate-in-right': {
          animation: 'fadeInRight 0.3s ease-out',
        },
      }
      addUtilities(newUtilities)
    },
  ],
}
