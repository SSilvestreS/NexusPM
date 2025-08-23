// Configurações de ambiente para Kubernetes
export const k8sConfig = {
  // Configurações da API
  api: {
    baseUrl: process.env.API_BASE_URL || 'http://api-service:3001',
    wsUrl: process.env.API_WS_URL || 'ws://api-service:3001',
    timeout: parseInt(process.env.API_TIMEOUT || '20000'),
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
    enableWebVitals: true,
  },
  
  // Configurações de cache
  cache: {
    enabled: process.env.CACHE_ENABLED !== 'false',
    maxAge: parseInt(process.env.CACHE_MAX_AGE || '600000'), // 10 minutos
    storage: process.env.CACHE_STORAGE || 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: process.env.ANALYTICS_ENABLED === 'true',
    debug: false,
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações de Kubernetes
  kubernetes: {
    namespace: process.env.K8S_NAMESPACE || 'default',
    podName: process.env.K8S_POD_NAME || 'storybook-pod',
    nodeName: process.env.K8S_NODE_NAME || 'unknown',
    serviceAccount: process.env.K8S_SERVICE_ACCOUNT || 'default',
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*'],
  },
  
  // Configurações de health check
  health: {
    enabled: true,
    path: process.env.HEALTH_CHECK_PATH || '/health',
    interval: parseInt(process.env.HEALTH_CHECK_INTERVAL || '30000'),
    timeout: parseInt(process.env.HEALTH_CHECK_TIMEOUT || '5000'),
  },
}
