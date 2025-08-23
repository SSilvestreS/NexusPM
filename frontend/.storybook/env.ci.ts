// Configurações de ambiente para CI/CD
export const ciConfig = {
  // Configurações da API
  api: {
    baseUrl: process.env.API_BASE_URL || 'http://localhost:3001',
    wsUrl: process.env.API_WS_URL || 'ws://localhost:3001',
    timeout: parseInt(process.env.API_TIMEOUT || '10000'),
  },
  
  // Configurações de debug
  debug: {
    enabled: process.env.DEBUG_ENABLED === 'true',
    level: process.env.DEBUG_LEVEL || 'warn',
    showReduxDevTools: false,
    showReactDevTools: false,
  },
  
  // Configurações de performance
  performance: {
    enableProfiling: false,
    enableReactProfiler: false,
    enableWebVitals: false,
  },
  
  // Configurações de cache
  cache: {
    enabled: false,
    maxAge: 0,
    storage: 'memory',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: false,
    debug: false,
    trackErrors: false,
    trackPerformance: false,
  },
  
  // Configurações de build
  build: {
    minify: true,
    sourcemap: false,
    optimizeDeps: true,
    chunkSizeWarningLimit: 1000,
  },
  
  // Configurações de teste
  test: {
    coverage: true,
    watch: false,
    failOnError: true,
    timeout: 30000,
  },
}
