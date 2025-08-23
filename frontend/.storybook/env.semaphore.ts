// Configurações de ambiente para Semaphore
export const semaphoreConfig = {
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
  
  // Configurações do Semaphore
  semaphore: {
    project: {
      id: process.env.SEMAPHORE_PROJECT_ID || '12345678',
      name: process.env.SEMAPHORE_PROJECT_NAME || 'nova-pasta',
      hashId: process.env.SEMAPHORE_PROJECT_HASH_ID || 'abc123def456',
    },
    pipeline: {
      id: process.env.SEMAPHORE_PIPELINE_ID || '123456789',
      number: process.env.SEMAPHORE_PIPELINE_NUMBER || '1',
      gitSha: process.env.SEMAPHORE_GIT_SHA || 'abc123def456',
      gitBranch: process.env.SEMAPHORE_GIT_BRANCH || 'main',
      gitRef: process.env.SEMAPHORE_GIT_REF || 'refs/heads/main',
      gitTag: process.env.SEMAPHORE_GIT_TAG || '',
      gitCommitMessage: process.env.SEMAPHORE_GIT_COMMIT_MESSAGE || 'Build Storybook',
      gitCommitAuthor: process.env.SEMAPHORE_GIT_COMMIT_AUTHOR || 'caspian',
      gitCommitAuthorEmail: process.env.SEMAPHORE_GIT_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      gitCommitAuthorAvatar: process.env.SEMAPHORE_GIT_COMMIT_AUTHOR_AVATAR || 'https://github.com/caspian.png',
      gitCommitUrl: process.env.SEMAPHORE_GIT_COMMIT_URL || 'https://github.com/caspian/nova-pasta/commit/abc123def456',
      gitCommitRange: process.env.SEMAPHORE_GIT_COMMIT_RANGE || 'def456...abc123',
    },
    workflow: {
      id: process.env.SEMAPHORE_WORKFLOW_ID || '123456789',
      number: process.env.SEMAPHORE_WORKFLOW_NUMBER || '1',
      name: process.env.SEMAPHORE_WORKFLOW_NAME || 'Build and Deploy',
      url: process.env.SEMAPHORE_WORKFLOW_URL || 'https://semaphore.semaphoreci.com/workflows/123456789',
    },
    job: {
      id: process.env.SEMAPHORE_JOB_ID || '123456789',
      number: process.env.SEMAPHORE_JOB_NUMBER || '1',
      name: process.env.SEMAPHORE_JOB_NAME || 'build-storybook',
      status: process.env.SEMAPHORE_JOB_RESULT || 'passed',
      url: process.env.SEMAPHORE_JOB_URL || 'https://semaphore.semaphoreci.com/jobs/123456789',
    },
    agent: {
      id: process.env.SEMAPHORE_AGENT_ID || 'agent-123456',
      name: process.env.SEMAPHORE_AGENT_NAME || 'agent-1',
      os: process.env.SEMAPHORE_AGENT_OS || 'linux',
      arch: process.env.SEMAPHORE_AGENT_ARCH || 'amd64',
      version: process.env.SEMAPHORE_AGENT_VERSION || '3.0.0',
    },
    environment: {
      name: process.env.SEMAPHORE_ENVIRONMENT_NAME || 'production',
      url: process.env.SEMAPHORE_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.semaphoreci.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'semaphore',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do Semaphore
  semaphoreCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$SEMAPHORE_GIT_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
