// Configurações de ambiente para staging
export const stagingConfig = {
  // Configurações da API
  api: {
    baseUrl: 'https://staging-api.nova-pasta.com',
    wsUrl: 'wss://staging-api.nova-pasta.com',
    timeout: 15000,
  },
  
  // Configurações de debug
  debug: {
    enabled: true,
    level: 'info',
    showReduxDevTools: true,
    showReactDevTools: false,
  },
  
  // Configurações de performance
  performance: {
    enableProfiling: true,
    enableReactProfiler: false,
    enableWebVitals: true,
  },
  
  // Configurações de cache
  cache: {
    enabled: true,
    maxAge: 30 * 60 * 1000, // 30 minutos
    storage: 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: true,
    debug: true,
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações de segurança
  security: {
    enableCSP: true,
    enableHSTS: false,
    enableXSSProtection: true,
    enableContentTypeSniffing: false,
  },
}
