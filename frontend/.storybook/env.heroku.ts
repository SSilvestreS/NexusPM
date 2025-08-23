// Configurações de ambiente para Heroku
export const herokuConfig = {
  // Configurações da API
  api: {
    baseUrl: process.env.API_BASE_URL || 'https://api.nova-pasta.com',
    wsUrl: process.env.API_WS_URL || 'wss://api.nova-pasta.com',
    timeout: parseInt(process.env.API_TIMEOUT || '30000'),
  },
  
  // Configurações de debug
  debug: {
    enabled: process.env.DEBUG_ENABLED === 'true',
    level: process.env.DEBUG_LEVEL || 'error',
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
    maxAge: parseInt(process.env.CACHE_MAX_AGE || '3600000'), // 1 hora
    storage: process.env.CACHE_STORAGE || 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: true,
    debug: false,
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações do Heroku
  heroku: {
    app: {
      name: process.env.HEROKU_APP_NAME || 'nova-pasta-storybook',
      id: process.env.HEROKU_APP_ID || '12345678-1234-1234-1234-123456789012',
      dyno: process.env.HEROKU_DYNO || 'web.1',
    },
    release: {
      version: process.env.HEROKU_RELEASE_VERSION || 'v1.0.0',
      commit: process.env.HEROKU_SLUG_COMMIT || 'abc123def456',
      description: process.env.HEROKU_RELEASE_DESCRIPTION || 'Deploy to production',
    },
    config: {
      nodeEnv: process.env.NODE_ENV || 'production',
      port: parseInt(process.env.PORT || '6006'),
      host: process.env.HOST || '0.0.0.0',
    },
    addons: {
      postgres: {
        enabled: process.env.HEROKU_POSTGRESQL_URL !== undefined,
        url: process.env.HEROKU_POSTGRESQL_URL || '',
      },
      redis: {
        enabled: process.env.HEROKU_REDIS_URL !== undefined,
        url: process.env.HEROKU_REDIS_URL || '',
      },
      cloudamqp: {
        enabled: process.env.CLOUDAMQP_URL !== undefined,
        url: process.env.CLOUDAMQP_URL || '',
      },
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.herokuapp.com', '*.herokudns.com'],
  },
  
  // Configurações de build
  build: {
    staticDir: process.env.STATIC_DIR || '../public',
    outputDir: process.env.OUTPUT_DIR || '../storybook-static',
    optimize: process.env.OPTIMIZE_BUILD === 'true',
    minify: process.env.MINIFY_BUILD !== 'false',
    sourcemap: process.env.SOURCEMAP_BUILD === 'true',
  },
  
  // Configurações de logs
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: process.env.LOG_FORMAT || 'json',
    timestamp: process.env.LOG_TIMESTAMP !== 'false',
    colorize: process.env.LOG_COLORIZE === 'true',
  },
}
