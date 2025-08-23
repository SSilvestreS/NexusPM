// Configurações de ambiente para CodeShip
export const codeshipConfig = {
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
  
  // Configurações do CodeShip
  codeship: {
    project: {
      id: process.env.CODESHIP_PROJECT_ID || '12345678',
      name: process.env.CODESHIP_PROJECT_NAME || 'nova-pasta',
      url: process.env.CODESHIP_PROJECT_URL || 'https://app.codeship.com/projects/12345678',
    },
    build: {
      id: process.env.CODESHIP_BUILD_ID || '123456789',
      number: process.env.CODESHIP_BUILD_NUMBER || '1',
      url: process.env.CODESHIP_BUILD_URL || 'https://app.codeship.com/projects/12345678/builds/123456789',
      status: process.env.CODESHIP_BUILD_STATUS || 'success',
      branch: process.env.CODESHIP_BRANCH || 'main',
      commit: process.env.CODESHIP_COMMIT_ID || 'abc123def456',
      message: process.env.CODESHIP_COMMIT_MESSAGE || 'Build Storybook',
      author: process.env.CODESHIP_COMMIT_AUTHOR || 'caspian',
      timestamp: process.env.CODESHIP_COMMIT_TIMESTAMP || '1640995200',
    },
    repository: {
      name: process.env.CODESHIP_REPO_NAME || 'nova-pasta',
      owner: process.env.CODESHIP_REPO_OWNER || 'caspian',
      fullName: process.env.CODESHIP_REPO_FULL_NAME || 'caspian/nova-pasta',
      url: process.env.CODESHIP_REPO_URL || 'https://github.com/caspian/nova-pasta',
      cloneUrl: process.env.CODESHIP_REPO_CLONE_URL || 'https://github.com/caspian/nova-pasta.git',
      sshUrl: process.env.CODESHIP_REPO_SSH_URL || 'git@github.com:caspian/nova-pasta.git',
      provider: process.env.CODESHIP_REPO_PROVIDER || 'github',
      branch: process.env.CODESHIP_BRANCH || 'main',
      tag: process.env.CODESHIP_TAG || '',
      pullRequest: process.env.CODESHIP_PULL_REQUEST || 'false',
      pullRequestNumber: process.env.CODESHIP_PULL_REQUEST_NUMBER || '',
      pullRequestTitle: process.env.CODESHIP_PULL_REQUEST_TITLE || '',
      pullRequestAuthor: process.env.CODESHIP_PULL_REQUEST_AUTHOR || '',
      pullRequestSourceBranch: process.env.CODESHIP_PULL_REQUEST_SOURCE_BRANCH || '',
      pullRequestTargetBranch: process.env.CODESHIP_PULL_REQUEST_TARGET_BRANCH || '',
    },
    environment: {
      name: process.env.CODESHIP_ENVIRONMENT_NAME || 'production',
      url: process.env.CODESHIP_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.codeship.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'codeship',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do CodeShip
  codeshipCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CODESHIP_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
