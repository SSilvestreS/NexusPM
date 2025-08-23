// Configurações de ambiente para Microsoft Azure
export const azureConfig = {
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
  
  // Configurações do Azure
  azure: {
    subscriptionId: process.env.AZURE_SUBSCRIPTION_ID || '12345678-1234-1234-1234-123456789012',
    resourceGroup: process.env.AZURE_RESOURCE_GROUP || 'nova-pasta-rg',
    location: process.env.AZURE_LOCATION || 'East US',
    appService: {
      name: process.env.AZURE_APP_SERVICE_NAME || 'nova-pasta-storybook',
      plan: process.env.AZURE_APP_SERVICE_PLAN || 'nova-pasta-plan',
      sku: process.env.AZURE_APP_SERVICE_SKU || 'B1',
    },
    storage: {
      account: process.env.AZURE_STORAGE_ACCOUNT || 'novapastastorybook',
      container: process.env.AZURE_STORAGE_CONTAINER || 'storybook',
      accessKey: process.env.AZURE_STORAGE_ACCESS_KEY || '',
    },
    cdn: {
      profile: process.env.AZURE_CDN_PROFILE || 'nova-pasta-cdn',
      endpoint: process.env.AZURE_CDN_ENDPOINT || 'nova-pasta-cdn.azureedge.net',
      origin: process.env.AZURE_CDN_ORIGIN || 'nova-pasta-storybook.azurewebsites.net',
    },
    keyVault: {
      name: process.env.AZURE_KEY_VAULT_NAME || 'nova-pasta-kv',
      url: process.env.AZURE_KEY_VAULT_URL || 'https://nova-pasta-kv.vault.azure.net/',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.azurewebsites.net', '*.azureedge.net'],
  },
  
  // Configurações de monitoramento
  monitoring: {
    applicationInsights: {
      enabled: true,
      instrumentationKey: process.env.APPINSIGHTS_INSTRUMENTATIONKEY || '',
      connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING || '',
    },
    logAnalytics: {
      enabled: true,
      workspaceId: process.env.LOG_ANALYTICS_WORKSPACE_ID || '',
      workspaceKey: process.env.LOG_ANALYTICS_WORKSPACE_KEY || '',
    },
  },
}
