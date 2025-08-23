// Configurações de ambiente para Google Cloud Platform
export const gcpConfig = {
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
  
  // Configurações do Google Cloud
  gcp: {
    projectId: process.env.GCP_PROJECT_ID || 'nova-pasta-project',
    region: process.env.GCP_REGION || 'us-central1',
    zone: process.env.GCP_ZONE || 'us-central1-a',
    cloudStorage: {
      bucket: process.env.GCS_BUCKET || 'nova-pasta-storybook',
      location: process.env.GCS_LOCATION || 'US',
    },
    cloudCDN: {
      enabled: true,
      origin: process.env.CDN_ORIGIN || 'nova-pasta-storybook.appspot.com',
      cachePolicy: process.env.CDN_CACHE_POLICY || 'public, max-age=31536000',
    },
    cloudRun: {
      service: process.env.CLOUD_RUN_SERVICE || 'nova-pasta-storybook',
      revision: process.env.CLOUD_RUN_REVISION || 'latest',
    },
    loadBalancer: {
      enabled: true,
      ip: process.env.LOAD_BALANCER_IP || '35.184.0.0',
      ssl: process.env.LOAD_BALANCER_SSL === 'true',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.googleapis.com', '*.gcp.com'],
  },
  
  // Configurações de monitoramento
  monitoring: {
    stackdriver: {
      enabled: true,
      projectId: process.env.STACKDRIVER_PROJECT_ID || 'nova-pasta-project',
      logName: process.env.STACKDRIVER_LOG_NAME || 'nova-pasta-storybook',
    },
    errorReporting: {
      enabled: true,
      service: process.env.ERROR_REPORTING_SERVICE || 'nova-pasta-storybook',
      version: process.env.ERROR_REPORTING_VERSION || '1.0.0',
    },
  },
}
