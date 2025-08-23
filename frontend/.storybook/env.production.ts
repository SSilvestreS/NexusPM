// Configurações de ambiente para produção
export const prodConfig = {
  // Configurações da API
  api: {
    baseUrl: 'https://api.nova-pasta.com',
    wsUrl: 'wss://api.nova-pasta.com',
    timeout: 30000,
  },
  
  // Configurações de debug
  debug: {
    enabled: false,
    level: 'error',
    showReduxDevTools: false,
    showReactDevTools: false,
  },
  
  // Configurações de performance
  performance: {
    enableProfiling: false,
    enableReactProfiler: false,
    enableWebVitals: true,
  },
  
  // Configurações de cache
  cache: {
    enabled: true,
    maxAge: 60 * 60 * 1000, // 1 hora
    storage: 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: true,
    debug: false,
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações de segurança
  security: {
    enableCSP: true,
    enableHSTS: true,
    enableXSSProtection: true,
    enableContentTypeSniffing: false,
  },
}
