// Configurações de ambiente para GitLab Pages
export const gitlabPagesConfig = {
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
  
  // Configurações do GitLab Pages
  gitlabPages: {
    project: {
      id: process.env.CI_PROJECT_ID || '12345678',
      name: process.env.CI_PROJECT_NAME || 'nova-pasta',
      path: process.env.CI_PROJECT_PATH || 'caspian/nova-pasta',
      url: process.env.CI_PROJECT_URL || 'https://gitlab.com/caspian/nova-pasta',
    },
    pipeline: {
      id: process.env.CI_PIPELINE_ID || '123456789',
      url: process.env.CI_PIPELINE_URL || 'https://gitlab.com/caspian/nova-pasta/-/pipelines/123456789',
      job: process.env.CI_JOB_ID || '123456789',
      stage: process.env.CI_JOB_STAGE || 'deploy',
    },
    deployment: {
      environment: process.env.CI_ENVIRONMENT_NAME || 'gitlab-pages',
      url: process.env.CI_ENVIRONMENT_URL || 'https://caspian.gitlab.io/nova-pages',
      branch: process.env.CI_COMMIT_REF_NAME || 'main',
      commit: process.env.CI_COMMIT_SHA || 'abc123def456',
    },
    runner: {
      id: process.env.CI_RUNNER_ID || '123456',
      description: process.env.CI_RUNNER_DESCRIPTION || 'gitlab-runner',
      tags: process.env.CI_RUNNER_TAGS?.split(',') || ['docker', 'linux'],
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.gitlab.io', '*.gitlab.com'],
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
      expireIn: process.env.ARTIFACT_EXPIRE_IN || '1 week',
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'gitlab-pages',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    variables: {
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do GitLab
  gitlabCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CI_COMMIT_REF_SLUG',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
