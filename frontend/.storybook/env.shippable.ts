// Configurações de ambiente para Shippable
export const shippableConfig = {
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
  
  // Configurações do Shippable
  shippable: {
    project: {
      id: process.env.SHIPPABLE_PROJECT_ID || '12345678',
      name: process.env.SHIPPABLE_PROJECT_NAME || 'nova-pasta',
      owner: process.env.SHIPPABLE_PROJECT_OWNER || 'caspian',
      url: process.env.SHIPPABLE_PROJECT_URL || 'https://app.shippable.com/github/caspian/nova-pasta',
    },
    build: {
      id: process.env.SHIPPABLE_BUILD_ID || '123456789',
      number: process.env.SHIPPABLE_BUILD_NUMBER || '1',
      url: process.env.SHIPPABLE_BUILD_URL || 'https://app.shippable.com/github/caspian/nova-pasta/runs/123456789',
      status: process.env.SHIPPABLE_BUILD_STATUS || 'success',
      result: process.env.SHIPPABLE_BUILD_RESULT || 'success',
      startedAt: process.env.SHIPPABLE_BUILD_STARTED_AT || '1640995200',
      finishedAt: process.env.SHIPPABLE_BUILD_FINISHED_AT || '1640995500',
      duration: process.env.SHIPPABLE_BUILD_DURATION || '300',
      message: process.env.SHIPPABLE_BUILD_MESSAGE || 'Build Storybook',
      branch: process.env.SHIPPABLE_BRANCH || 'main',
      commit: process.env.SHIPPABLE_COMMIT || 'abc123def456',
      author: process.env.SHIPPABLE_COMMIT_AUTHOR || 'caspian',
      authorEmail: process.env.SHIPPABLE_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      commitMessage: process.env.SHIPPABLE_COMMIT_MESSAGE || 'Build Storybook',
      commitRange: process.env.SHIPPABLE_COMMIT_RANGE || 'def456...abc123',
      pullRequest: process.env.SHIPPABLE_PULL_REQUEST || 'false',
      pullRequestNumber: process.env.SHIPPABLE_PULL_REQUEST_NUMBER || '',
      pullRequestTitle: process.env.SHIPPABLE_PULL_REQUEST_TITLE || '',
      pullRequestAuthor: process.env.SHIPPABLE_PULL_REQUEST_AUTHOR || '',
      pullRequestSourceBranch: process.env.SHIPPABLE_PULL_REQUEST_SOURCE_BRANCH || '',
      pullRequestTargetBranch: process.env.SHIPPABLE_PULL_REQUEST_TARGET_BRANCH || '',
      tag: process.env.SHIPPABLE_TAG || '',
      tagName: process.env.SHIPPABLE_TAG_NAME || '',
    },
    repository: {
      name: process.env.SHIPPABLE_REPO_NAME || 'nova-pasta',
      owner: process.env.SHIPPABLE_REPO_OWNER || 'caspian',
      fullName: process.env.SHIPPABLE_REPO_FULL_NAME || 'caspian/nova-pasta',
      url: process.env.SHIPPABLE_REPO_URL || 'https://github.com/caspian/nova-pasta',
      cloneUrl: process.env.SHIPPABLE_REPO_CLONE_URL || 'https://github.com/caspian/nova-pasta.git',
      sshUrl: process.env.SHIPPABLE_REPO_SSH_URL || 'git@github.com:caspian/nova-pasta.git',
      provider: process.env.SHIPPABLE_REPO_PROVIDER || 'github',
      branch: process.env.SHIPPABLE_BRANCH || 'main',
      tag: process.env.SHIPPABLE_TAG || '',
      commit: process.env.SHIPPABLE_COMMIT || 'abc123def456',
      commitAuthor: process.env.SHIPPABLE_COMMIT_AUTHOR || 'caspian',
      commitAuthorEmail: process.env.SHIPPABLE_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      commitMessage: process.env.SHIPPABLE_COMMIT_MESSAGE || 'Build Storybook',
      commitRange: process.env.SHIPPABLE_COMMIT_RANGE || 'def456...abc123',
      pullRequest: process.env.SHIPPABLE_PULL_REQUEST || 'false',
      pullRequestNumber: process.env.SHIPPABLE_PULL_REQUEST_NUMBER || '',
      pullRequestTitle: process.env.SHIPPABLE_PULL_REQUEST_TITLE || '',
      pullRequestAuthor: process.env.SHIPPABLE_PULL_REQUEST_AUTHOR || '',
      pullRequestSourceBranch: process.env.SHIPPABLE_PULL_REQUEST_SOURCE_BRANCH || '',
      pullRequestTargetBranch: process.env.SHIPPABLE_PULL_REQUEST_TARGET_BRANCH || '',
    },
    job: {
      id: process.env.SHIPPABLE_JOB_ID || '123456789',
      number: process.env.SHIPPABLE_JOB_NUMBER || '1',
      name: process.env.SHIPPABLE_JOB_NAME || 'build-storybook',
      status: process.env.SHIPPABLE_JOB_STATUS || 'success',
      result: process.env.SHIPPABLE_JOB_RESULT || 'success',
      startedAt: process.env.SHIPPABLE_JOB_STARTED_AT || '1640995200',
      finishedAt: process.env.SHIPPABLE_JOB_FINISHED_AT || '1640995500',
      duration: process.env.SHIPPABLE_JOB_DURATION || '300',
    },
    environment: {
      name: process.env.SHIPPABLE_ENVIRONMENT_NAME || 'production',
      url: process.env.SHIPPABLE_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.shippable.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'shippable',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do Shippable
  shippableCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$SHIPPABLE_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
