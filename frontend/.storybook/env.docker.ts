// Configurações de ambiente para Docker
export const dockerConfig = {
  // Configurações da API
  api: {
    baseUrl: process.env.API_BASE_URL || 'http://localhost:3001',
    wsUrl: process.env.API_WS_URL || 'ws://localhost:3001',
    timeout: parseInt(process.env.API_TIMEOUT || '15000'),
  },
  
  // Configurações de debug
  debug: {
    enabled: process.env.DEBUG_ENABLED === 'true',
    level: process.env.DEBUG_LEVEL || 'info',
    showReduxDevTools: process.env.SHOW_REDUX_DEVTOOLS === 'true',
    showReactDevTools: false,
  },
  
  // Configurações de performance
  performance: {
    enableProfiling: process.env.ENABLE_PROFILING === 'true',
    enableReactProfiler: false,
    enableWebVitals: true,
  },
  
  // Configurações de cache
  cache: {
    enabled: process.env.CACHE_ENABLED !== 'false',
    maxAge: parseInt(process.env.CACHE_MAX_AGE || '300000'), // 5 minutos
    storage: process.env.CACHE_STORAGE || 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: process.env.ANALYTICS_ENABLED === 'true',
    debug: process.env.ANALYTICS_DEBUG === 'true',
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['localhost', '.localhost'],
  },
  
  // Configurações de volume
  volume: {
    storiesDir: process.env.STORIES_DIR || '../src',
    staticDir: process.env.STATIC_DIR || '../public',
    outputDir: process.env.OUTPUT_DIR || '../storybook-static',
  },
}
