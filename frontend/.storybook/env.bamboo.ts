// Configurações de ambiente para Bamboo
export const bambooConfig = {
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
  
  // Configurações do Bamboo
  bamboo: {
    server: {
      url: process.env.BAMBOO_SERVER_URL || 'http://bamboo.example.com',
      name: process.env.BAMBOO_SERVER_NAME || 'Bamboo',
      version: process.env.BAMBOO_SERVER_VERSION || '9.3.0',
    },
    plan: {
      key: process.env.BAMBOO_PLAN_KEY || 'NOVA-PASTA-STORYBOOK',
      name: process.env.BAMBOO_PLAN_NAME || 'Nova Pasta Storybook',
      shortName: process.env.BAMBOO_PLAN_SHORT_NAME || 'Storybook',
      shortKey: process.env.BAMBOO_PLAN_SHORT_KEY || 'STORYBOOK',
    },
    build: {
      number: process.env.BAMBOO_BUILD_NUMBER || '1',
      key: process.env.BAMBOO_BUILD_KEY || 'NOVA-PASTA-STORYBOOK-1',
      resultKey: process.env.BAMBOO_BUILD_RESULT_KEY || 'NOVA-PASTA-STORYBOOK-1',
      url: process.env.BAMBOO_BUILD_URL || 'http://bamboo.example.com/browse/NOVA-PASTA-STORYBOOK-1',
      timestamp: process.env.BAMBOO_BUILD_TIMESTAMP || '2024-01-01T00:00:00Z',
      duration: process.env.BAMBOO_BUILD_DURATION || '300000',
      result: process.env.BAMBOO_BUILD_RESULT || 'SUCCESS',
    },
    job: {
      key: process.env.BAMBOO_JOB_KEY || 'NOVA-PASTA-STORYBOOK-1',
      name: process.env.BAMBOO_JOB_NAME || 'Build Storybook',
      url: process.env.BAMBOO_JOB_URL || 'http://bamboo.example.com/browse/NOVA-PASTA-STORYBOOK-1',
    },
    repository: {
      name: process.env.BAMBOO_REPOSITORY_NAME || 'nova-pasta',
      revision: process.env.BAMBOO_REPOSITORY_REVISION || 'abc123def456',
      branch: process.env.BAMBOO_REPOSITORY_BRANCH || 'main',
      url: process.env.BAMBOO_REPOSITORY_URL || 'https://github.com/caspian/nova-pasta.git',
    },
    environment: {
      home: process.env.BAMBOO_HOME || '/opt/atlassian/bamboo',
      working: process.env.BAMBOO_WORKING_DIRECTORY || '/opt/atlassian/bamboo/xml-data/build-dir/NOVA-PASTA-STORYBOOK',
      temp: process.env.BAMBOO_TEMP || '/tmp',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.bamboo.com', '*.github.com'],
  },
  
  // Configurações de build
  build: {
    command: process.env.BUILD_COMMAND || 'npm run build:storybook',
    outputDir: process.env.OUTPUT_DIR || '../storybook-static',
    sourceDir: process.env.SOURCE_DIR || '../src',
    publicDir: process.env.PUBLIC_DIR || '../public',
    artifacts: {
      enabled: true,
      paths: process.env.ARTIFACT_PATHS?.split(',') || ['../storybook-static'],
      destination: process.env.ARTIFACT_DESTINATION || 'storybook-build',
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'bamboo',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do Bamboo
  bambooCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BAMBOO_REPOSITORY_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
