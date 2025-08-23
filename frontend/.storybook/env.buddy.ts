// Configurações de ambiente para Buddy
export const buddyConfig = {
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
  
  // Configurações do Buddy
  buddy: {
    workspace: {
      id: process.env.BUDDY_WORKSPACE_ID || '12345678',
      name: process.env.BUDDY_WORKSPACE_NAME || 'caspian',
      url: process.env.BUDDY_WORKSPACE_URL || 'https://app.buddy.works/caspian',
    },
    project: {
      id: process.env.BUDDY_PROJECT_ID || '12345678',
      name: process.env.BUDDY_PROJECT_NAME || 'nova-pasta',
      url: process.env.BUDDY_PROJECT_URL || 'https://app.buddy.works/caspian/nova-pasta',
    },
    pipeline: {
      id: process.env.BUDDY_PIPELINE_ID || '123456789',
      name: process.env.BUDDY_PIPELINE_NAME || 'Build and Deploy',
      url: process.env.BUDDY_PIPELINE_URL || 'https://app.buddy.works/caspian/nova-pasta/pipelines/123456789',
      status: process.env.BUDDY_PIPELINE_STATUS || 'success',
      result: process.env.BUDDY_PIPELINE_RESULT || 'success',
      startedAt: process.env.BUDDY_PIPELINE_STARTED_AT || '1640995200',
      finishedAt: process.env.BUDDY_PIPELINE_FINISHED_AT || '1640995500',
      duration: process.env.BUDDY_PIPELINE_DURATION || '300',
      message: process.env.BUDDY_PIPELINE_MESSAGE || 'Build Storybook',
      branch: process.env.BUDDY_PIPELINE_BRANCH || 'main',
      commit: process.env.BUDDY_PIPELINE_COMMIT || 'abc123def456',
      author: process.env.BUDDY_PIPELINE_AUTHOR || 'caspian',
      authorEmail: process.env.BUDDY_PIPELINE_AUTHOR_EMAIL || 'caspian@example.com',
      commitMessage: process.env.BUDDY_PIPELINE_COMMIT_MESSAGE || 'Build Storybook',
      commitRange: process.env.BUDDY_PIPELINE_COMMIT_RANGE || 'def456...abc123',
      pullRequest: process.env.BUDDY_PIPELINE_PULL_REQUEST || 'false',
      pullRequestNumber: process.env.BUDDY_PIPELINE_PULL_REQUEST_NUMBER || '',
      pullRequestTitle: process.env.BUDDY_PIPELINE_PULL_REQUEST_TITLE || '',
      pullRequestAuthor: process.env.BUDDY_PIPELINE_PULL_REQUEST_AUTHOR || '',
      pullRequestSourceBranch: process.env.BUDDY_PIPELINE_PULL_REQUEST_SOURCE_BRANCH || '',
      pullRequestTargetBranch: process.env.BUDDY_PIPELINE_PULL_REQUEST_TARGET_BRANCH || '',
      tag: process.env.BUDDY_PIPELINE_TAG || '',
      tagName: process.env.BUDDY_PIPELINE_TAG_NAME || '',
    },
    execution: {
      id: process.env.BUDDY_EXECUTION_ID || '123456789',
      number: process.env.BUDDY_EXECUTION_NUMBER || '1',
      url: process.env.BUDDY_EXECUTION_URL || 'https://app.buddy.works/caspian/nova-pasta/pipelines/123456789/executions/1',
      status: process.env.BUDDY_EXECUTION_STATUS || 'success',
      result: process.env.BUDDY_EXECUTION_RESULT || 'success',
      startedAt: process.env.BUDDY_EXECUTION_STARTED_AT || '1640995200',
      finishedAt: process.env.BUDDY_EXECUTION_FINISHED_AT || '1640995500',
      duration: process.env.BUDDY_EXECUTION_DURATION || '300',
    },
    action: {
      id: process.env.BUDDY_ACTION_ID || '123456789',
      name: process.env.BUDDY_ACTION_NAME || 'build-storybook',
      type: process.env.BUDDY_ACTION_TYPE || 'build',
      status: process.env.BUDDY_ACTION_STATUS || 'success',
      result: process.env.BUDDY_ACTION_RESULT || 'success',
      startedAt: process.env.BUDDY_ACTION_STARTED_AT || '1640995200',
      finishedAt: process.env.BUDDY_ACTION_FINISHED_AT || '1640995500',
      duration: process.env.BUDDY_ACTION_DURATION || '300',
    },
    repository: {
      name: process.env.BUDDY_REPO_NAME || 'nova-pasta',
      owner: process.env.BUDDY_REPO_OWNER || 'caspian',
      fullName: process.env.BUDDY_REPO_FULL_NAME || 'caspian/nova-pasta',
      url: process.env.BUDDY_REPO_URL || 'https://github.com/caspian/nova-pasta',
      cloneUrl: process.env.BUDDY_REPO_CLONE_URL || 'https://github.com/caspian/nova-pasta.git',
      sshUrl: process.env.BUDDY_REPO_SSH_URL || 'git@github.com:caspian/nova-pasta.git',
      provider: process.env.BUDDY_REPO_PROVIDER || 'github',
      branch: process.env.BUDDY_PIPELINE_BRANCH || 'main',
      tag: process.env.BUDDY_PIPELINE_TAG || '',
      commit: process.env.BUDDY_PIPELINE_COMMIT || 'abc123def456',
      commitAuthor: process.env.BUDDY_PIPELINE_AUTHOR || 'caspian',
      commitAuthorEmail: process.env.BUDDY_PIPELINE_AUTHOR_EMAIL || 'caspian@example.com',
      commitMessage: process.env.BUDDY_PIPELINE_COMMIT_MESSAGE || 'Build Storybook',
      commitRange: process.env.BUDDY_PIPELINE_COMMIT_RANGE || 'def456...abc123',
      pullRequest: process.env.BUDDY_PIPELINE_PULL_REQUEST || 'false',
      pullRequestNumber: process.env.BUDDY_PIPELINE_PULL_REQUEST_NUMBER || '',
      pullRequestTitle: process.env.BUDDY_PIPELINE_PULL_REQUEST_TITLE || '',
      pullRequestAuthor: process.env.BUDDY_PIPELINE_PULL_REQUEST_AUTHOR || '',
      pullRequestSourceBranch: process.env.BUDDY_PIPELINE_PULL_REQUEST_SOURCE_BRANCH || '',
      pullRequestTargetBranch: process.env.BUDDY_PIPELINE_PULL_REQUEST_TARGET_BRANCH || '',
    },
    environment: {
      name: process.env.BUDDY_ENVIRONMENT_NAME || 'production',
      url: process.env.BUDDY_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.buddy.works', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'buddy',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do Buddy
  buddyCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BUDDY_PIPELINE_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
