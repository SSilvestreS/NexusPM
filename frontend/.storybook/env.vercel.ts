// Configurações de ambiente para Vercel
export const vercelConfig = {
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
  
  // Configurações do Vercel
  vercel: {
    project: {
      id: process.env.VERCEL_PROJECT_ID || 'prj_1234567890abcdef',
      name: process.env.VERCEL_PROJECT_NAME || 'nova-pasta-storybook',
      team: process.env.VERCEL_TEAM_ID || 'team_1234567890abcdef',
    },
    deployment: {
      id: process.env.VERCEL_DEPLOYMENT_ID || 'dpl_1234567890abcdef',
      url: process.env.VERCEL_URL || 'https://nova-pasta-storybook.vercel.app',
      environment: process.env.VERCEL_ENV || 'production',
      branch: process.env.VERCEL_GIT_COMMIT_REF || 'main',
      commit: process.env.VERCEL_GIT_COMMIT_SHA || 'abc123def456',
    },
    functions: {
      region: process.env.VERCEL_REGION || 'iad1',
      runtime: process.env.VERCEL_RUNTIME || 'nodejs18.x',
      memory: parseInt(process.env.VERCEL_FUNCTION_MEMORY || '1024'),
      timeout: parseInt(process.env.VERCEL_FUNCTION_TIMEOUT || '10000'),
    },
    edge: {
      enabled: process.env.VERCEL_EDGE_ENABLED === 'true',
      regions: process.env.VERCEL_EDGE_REGIONS?.split(',') || ['iad1', 'sfo1'],
      cache: process.env.VERCEL_EDGE_CACHE !== 'false',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.vercel.app', '*.vercel.com'],
  },
  
  // Configurações de build
  build: {
    outputDir: process.env.OUTPUT_DIR || '../storybook-static',
    staticDir: process.env.STATIC_DIR || '../public',
    optimize: process.env.OPTIMIZE_BUILD === 'true',
    minify: process.env.MINIFY_BUILD !== 'false',
    sourcemap: process.env.SOURCEMAP_BUILD === 'true',
  },
  
  // Configurações de analytics do Vercel
  vercelAnalytics: {
    enabled: process.env.VERCEL_ANALYTICS_ENABLED === 'true',
    id: process.env.VERCEL_ANALYTICS_ID || '',
    debug: process.env.VERCEL_ANALYTICS_DEBUG === 'true',
    mode: process.env.VERCEL_ANALYTICS_MODE || 'production',
  },
}
