// Configurações de ambiente para Bitbucket Pipelines
export const bitbucketConfig = {
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
  
  // Configurações do Bitbucket
  bitbucket: {
    repository: {
      name: process.env.BITBUCKET_REPO_SLUG || 'nova-pasta',
      owner: process.env.BITBUCKET_REPO_OWNER || 'caspian',
      fullName: process.env.BITBUCKET_REPO_FULL_NAME || 'caspian/nova-pasta',
      cloneUrl: process.env.BITBUCKET_GIT_HTTP_ORIGIN || 'https://bitbucket.org/caspian/nova-pasta.git',
    },
    pipeline: {
      buildNumber: process.env.BITBUCKET_BUILD_NUMBER || '1',
      key: process.env.BITBUCKET_PIPELINE_KEY || 'nova-pasta-storybook',
      name: process.env.BITBUCKET_PIPELINE_NAME || 'Deploy Storybook',
      uuid: process.env.BITBUCKET_PIPELINE_UUID || '12345678-1234-1234-1234-123456789012',
    },
    commit: {
      hash: process.env.BITBUCKET_COMMIT || 'abc123def456',
      branch: process.env.BITBUCKET_BRANCH || 'main',
      tag: process.env.BITBUCKET_TAG || '',
      message: process.env.BITBUCKET_COMMIT_MESSAGE || 'Deploy Storybook',
    },
    workspace: {
      name: process.env.BITBUCKET_WORKSPACE || 'caspian',
      uuid: process.env.BITBUCKET_WORKSPACE_UUID || '12345678-1234-1234-1234-123456789012',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.bitbucket.org', '*.bitbucket.io'],
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
      name: process.env.ARTIFACT_NAME || 'storybook-build',
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'bitbucket-pages',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do Bitbucket
  bitbucketCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BITBUCKET_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
