// Configurações de ambiente para Buildkite
export const buildkiteConfig = {
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
  
  // Configurações do Buildkite
  buildkite: {
    build: {
      id: process.env.BUILDKITE_BUILD_ID || '123456789',
      number: process.env.BUILDKITE_BUILD_NUMBER || '1',
      url: process.env.BUILDKITE_BUILD_URL || 'https://buildkite.com/caspian/nova-pasta/builds/1',
      branch: process.env.BUILDKITE_BRANCH || 'main',
      commit: process.env.BUILDKITE_COMMIT || 'abc123def456',
      message: process.env.BUILDKITE_MESSAGE || 'Build Storybook',
      author: process.env.BUILDKITE_BUILD_AUTHOR || 'caspian',
      creator: process.env.BUILDKITE_BUILD_CREATOR || 'caspian',
      source: process.env.BUILDKITE_BUILD_CREATOR_EMAIL || 'caspian@example.com',
      pullRequest: process.env.BUILDKITE_PULL_REQUEST || 'false',
      tag: process.env.BUILDKITE_TAG || '',
      environment: process.env.BUILDKITE_BUILD_ENV || 'production',
    },
    pipeline: {
      name: process.env.BUILDKITE_PIPELINE_NAME || 'nova-pasta',
      slug: process.env.BUILDKITE_PIPELINE_SLUG || 'nova-pasta',
      organization: process.env.BUILDKITE_ORGANIZATION_SLUG || 'caspian',
      url: process.env.BUILDKITE_PIPELINE_URL || 'https://buildkite.com/caspian/nova-pasta',
    },
    job: {
      id: process.env.BUILDKITE_JOB_ID || '123456789',
      label: process.env.BUILDKITE_LABEL || 'build-storybook',
      parallel: process.env.BUILDKITE_PARALLEL_JOB || '0',
      parallelCount: process.env.BUILDKITE_PARALLEL_JOB_COUNT || '1',
      retryCount: process.env.BUILDKITE_RETRY_COUNT || '0',
      retryCountMax: process.env.BUILDKITE_RETRY_COUNT_MAX || '3',
    },
    agent: {
      id: process.env.BUILDKITE_AGENT_ID || 'agent-123456',
      name: process.env.BUILDKITE_AGENT_NAME || 'agent-1',
      hostname: process.env.BUILDKITE_AGENT_HOSTNAME || 'agent-1.example.com',
      version: process.env.BUILDKITE_AGENT_VERSION || '3.45.0',
    },
    repository: {
      url: process.env.BUILDKITE_REPO || 'https://github.com/caspian/nova-pasta.git',
      ssh: process.env.BUILDKITE_REPO_SSH_KEY || '',
      https: process.env.BUILDKITE_REPO_HTTPS || 'https://github.com/caspian/nova-pasta.git',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.buildkite.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'buildkite',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do Buildkite
  buildkiteCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BUILDKITE_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
