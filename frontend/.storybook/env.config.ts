// Configurações de ambiente para o Storybook
export const storybookConfig = {
  // Configurações da API
  api: {
    baseUrl: process.env.STORYBOOK_API_URL || 'http://localhost:3001',
    wsUrl: process.env.STORYBOOK_WS_URL || 'ws://localhost:6006',
  },
  
  // Configurações de tema
  theme: {
    default: process.env.STORYBOOK_THEME || 'light',
    locale: process.env.STORYBOOK_LOCALE || 'pt-BR',
  },
  
  // Configurações de performance
  performance: {
    mode: process.env.STORYBOOK_PERFORMANCE_MODE === 'true',
    lazyCompilation: process.env.STORYBOOK_LAZY_COMPILATION !== 'false',
  },
  
  // Configurações de build
  build: {
    minify: process.env.NODE_ENV === 'production',
    sourcemap: process.env.NODE_ENV !== 'production',
  },
}
