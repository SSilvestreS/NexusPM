// Configurações de ambiente para teste
export const testConfig = {
  // Configurações da API
  api: {
    baseUrl: 'http://localhost:3001',
    wsUrl: 'ws://localhost:3001',
    timeout: 5000,
  },
  
  // Configurações de debug
  debug: {
    enabled: true,
    level: 'warn',
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
  
  // Configurações de mock
  mock: {
    enabled: true,
    delay: 100,
    errorRate: 0.1,
  },
}
