// Configurações de ambiente para desenvolvimento
export const devConfig = {
  // Configurações da API
  api: {
    baseUrl: 'http://localhost:3001',
    wsUrl: 'ws://localhost:3001',
    timeout: 10000,
  },
  
  // Configurações de debug
  debug: {
    enabled: true,
    level: 'debug',
    showReduxDevTools: true,
    showReactDevTools: true,
  },
  
  // Configurações de performance
  performance: {
    enableProfiling: true,
    enableReactProfiler: true,
    enableWebVitals: true,
  },
  
  // Configurações de cache
  cache: {
    enabled: true,
    maxAge: 5 * 60 * 1000, // 5 minutos
    storage: 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: false,
    debug: true,
    trackErrors: true,
    trackPerformance: true,
  },
}
