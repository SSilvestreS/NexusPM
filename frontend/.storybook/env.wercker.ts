// Configurações de ambiente para Wercker
export const werckerConfig = {
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
    maxAge: parseInt(process.env.CACHE_MAX_AGE || '3600000'),
    storage: process.env.CACHE_STORAGE || 'localStorage',
  },
  
  // Configurações de analytics
  analytics: {
    enabled: true,
    debug: false,
    trackErrors: true,
    trackPerformance: true,
  },
  
  // Configurações do Wercker
  wercker: {
    application: {
      name: process.env.WERCKER_APPLICATION_NAME || 'nova-pasta',
      ownerName: process.env.WERCKER_APPLICATION_OWNER_NAME || 'caspian',
      url: process.env.WERCKER_APPLICATION_URL || 'https://app.wercker.com/caspian/nova-pasta',
    },
    build: {
      id: process.env.WERCKER_BUILD_ID || '123456789',
      url: process.env.WERCKER_BUILD_URL || 'https://app.wercker.com/caspian/nova-pasta/runs/123456789',
      status: process.env.WERCKER_BUILD_STATUS || 'passed',
      result: process.env.WERCKER_BUILD_RESULT || 'passed',
      startedAt: process.env.WERCKER_BUILD_STARTED_AT || '1640995200',
      finishedAt: process.env.WERCKER_BUILD_FINISHED_AT || '1640995500',
      duration: process.env.WERCKER_BUILD_DURATION || '300',
      message: process.env.WERCKER_BUILD_MESSAGE || 'Build Storybook',
      branch: process.env.WERCKER_GIT_BRANCH || 'main',
      commit: process.env.WERCKER_GIT_COMMIT || 'abc123def456',
      author: process.env.WERCKER_GIT_OWNER || 'caspian',
      repository: process.env.WERCKER_GIT_REPOSITORY || 'nova-pasta',
      domain: process.env.WERCKER_GIT_DOMAIN || 'github.com',
    },
    step: {
      name: process.env.WERCKER_STEP_NAME || 'build-storybook',
      id: process.env.WERCKER_STEP_ID || '123456789',
      url: process.env.WERCKER_STEP_URL || 'https://app.wercker.com/caspian/nova-pasta/runs/123456789',
      status: process.env.WERCKER_STEP_STATUS || 'passed',
      result: process.env.WERCKER_STEP_RESULT || 'passed',
      startedAt: process.env.WERCKER_STEP_STARTED_AT || '1640995200',
      finishedAt: process.env.WERCKER_STEP_FINISHED_AT || '1640995500',
      duration: process.env.WERCKER_STEP_DURATION || '300',
    },
    environment: {
      name: process.env.WERCKER_ENVIRONMENT_NAME || 'production',
      url: process.env.WERCKER_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.wercker.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'wercker',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do Wercker
  werckerCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$WERCKER_GIT_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
