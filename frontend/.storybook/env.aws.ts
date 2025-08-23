// Configurações de ambiente para AWS
export const awsConfig = {
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
  
  // Configurações da AWS
  aws: {
    region: process.env.AWS_REGION || 'us-east-1',
    cloudFront: {
      domain: process.env.CLOUDFRONT_DOMAIN || 'd1234567890.cloudfront.net',
      distributionId: process.env.CLOUDFRONT_DISTRIBUTION_ID || 'E1234567890',
    },
    s3: {
      bucket: process.env.S3_BUCKET || 'nova-pasta-storybook',
      region: process.env.S3_REGION || 'us-east-1',
    },
    cloudWatch: {
      logGroup: process.env.CLOUDWATCH_LOG_GROUP || '/aws/lambda/nova-pasta-storybook',
      logStream: process.env.CLOUDWATCH_LOG_STREAM || 'storybook-logs',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.amazonaws.com', '*.cloudfront.net'],
  },
  
  // Configurações de CDN
  cdn: {
    enabled: true,
    domain: process.env.CDN_DOMAIN || 'cdn.nova-pasta.com',
    version: process.env.CDN_VERSION || 'v1',
    cacheControl: process.env.CDN_CACHE_CONTROL || 'public, max-age=31536000',
  },
}
