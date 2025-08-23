// Configurações de ambiente para DigitalOcean
export const digitalOceanConfig = {
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
  
  // Configurações do DigitalOcean
  digitalOcean: {
    region: process.env.DO_REGION || 'nyc1',
    droplet: {
      id: process.env.DO_DROPLET_ID || '123456789',
      name: process.env.DO_DROPLET_NAME || 'nova-pasta-storybook',
      size: process.env.DO_DROPLET_SIZE || 's-1vcpu-1gb',
      image: process.env.DO_DROPLET_IMAGE || 'ubuntu-20-04-x64',
    },
    spaces: {
      region: process.env.DO_SPACES_REGION || 'nyc3',
      bucket: process.env.DO_SPACES_BUCKET || 'nova-pasta-storybook',
      endpoint: process.env.DO_SPACES_ENDPOINT || 'nyc3.digitaloceanspaces.com',
      accessKey: process.env.DO_SPACES_ACCESS_KEY || '',
      secretKey: process.env.DO_SPACES_SECRET_KEY || '',
    },
    loadBalancer: {
      id: process.env.DO_LOAD_BALANCER_ID || '123456789',
      name: process.env.DO_LOAD_BALANCER_NAME || 'nova-pasta-lb',
      ip: process.env.DO_LOAD_BALANCER_IP || '157.230.0.0',
      ssl: process.env.DO_LOAD_BALANCER_SSL === 'true',
    },
    cdn: {
      enabled: true,
      domain: process.env.DO_CDN_DOMAIN || 'cdn.nova-pasta.com',
      origin: process.env.DO_CDN_ORIGIN || 'nova-pasta-storybook.com',
      ttl: parseInt(process.env.DO_CDN_TTL || '3600'),
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.digitaloceanspaces.com', '*.digitalocean.com'],
  },
  
  // Configurações de monitoramento
  monitoring: {
    uptimeRobot: {
      enabled: true,
      apiKey: process.env.UPTIME_ROBOT_API_KEY || '',
      monitorId: process.env.UPTIME_ROBOT_MONITOR_ID || '',
    },
    pingdom: {
      enabled: true,
      apiKey: process.env.PINGDOM_API_KEY || '',
      checkId: process.env.PINGDOM_CHECK_ID || '',
    },
  },
}
