// Configurações de ambiente para Netlify
export const netlifyConfig = {
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
  
  // Configurações do Netlify
  netlify: {
    site: {
      id: process.env.NETLIFY_SITE_ID || '12345678-1234-1234-1234-123456789012',
      name: process.env.NETLIFY_SITE_NAME || 'nova-pasta-storybook',
      url: process.env.URL || 'https://nova-pasta-storybook.netlify.app',
    },
    build: {
      id: process.env.NETLIFY_BUILD_ID || '1234567890abcdef',
      deployId: process.env.NETLIFY_DEPLOY_ID || '1234567890abcdef',
      context: process.env.CONTEXT || 'production',
      branch: process.env.BRANCH || 'main',
      commit: process.env.COMMIT_REF || 'abc123def456',
    },
    functions: {
      directory: process.env.NETLIFY_FUNCTIONS_DIR || 'netlify/functions',
      nodeVersion: process.env.NODE_VERSION || '18',
      timeout: parseInt(process.env.NETLIFY_FUNCTIONS_TIMEOUT || '10000'),
    },
    redirects: {
      enabled: true,
      file: process.env.NETLIFY_REDIRECTS_FILE || '_redirects',
      rules: [
        '/* /index.html 200',
        '/api/* https://api.nova-pasta.com/:splat 200',
      ],
    },
    headers: {
      enabled: true,
      file: process.env.NETLIFY_HEADERS_FILE || '_headers',
      rules: [
        '/* X-Frame-Options: DENY',
        '/* X-XSS-Protection: 1; mode=block',
        '/* X-Content-Type-Options: nosniff',
        '/static/* Cache-Control: public, max-age=31536000',
      ],
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.netlify.app', '*.netlify.com'],
  },
  
  // Configurações de build
  build: {
    command: process.env.BUILD_COMMAND || 'npm run build:storybook',
    publish: process.env.PUBLISH_DIR || '../storybook-static',
    functions: process.env.FUNCTIONS_DIR || 'netlify/functions',
    edgeFunctions: process.env.EDGE_FUNCTIONS_DIR || 'netlify/edge-functions',
  },
  
  // Configurações de forms
  forms: {
    enabled: process.env.NETLIFY_FORMS_ENABLED === 'true',
    honeypot: process.env.NETLIFY_FORMS_HONEYPOT === 'true',
    spamFilter: process.env.NETLIFY_FORMS_SPAM_FILTER === 'true',
  },
}
