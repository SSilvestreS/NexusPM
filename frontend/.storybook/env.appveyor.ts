// Configurações de ambiente para AppVeyor
export const appveyorConfig = {
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
  
  // Configurações do AppVeyor
  appveyor: {
    build: {
      id: process.env.APPVEYOR_BUILD_ID || '123456789',
      number: process.env.APPVEYOR_BUILD_NUMBER || '1',
      version: process.env.APPVEYOR_BUILD_VERSION || '1.0.0',
      folder: process.env.APPVEYOR_BUILD_FOLDER || 'C:\\projects\\nova-pasta',
      workingDirectory: process.env.APPVEYOR_BUILD_WORKING_DIRECTORY || 'C:\\projects\\nova-pasta',
      url: process.env.APPVEYOR_BUILD_URL || 'https://ci.appveyor.com/project/caspian/nova-pasta/build/1',
      status: process.env.APPVEYOR_BUILD_STATUS || 'success',
      message: process.env.APPVEYOR_BUILD_MESSAGE || 'Build Storybook',
      branch: process.env.APPVEYOR_REPO_BRANCH || 'main',
      commit: process.env.APPVEYOR_REPO_COMMIT || 'abc123def456',
      commitAuthor: process.env.APPVEYOR_REPO_COMMIT_AUTHOR || 'caspian',
      commitAuthorEmail: process.env.APPVEYOR_REPO_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      commitDate: process.env.APPVEYOR_REPO_COMMIT_DATE || '2024-01-01T00:00:00Z',
      commitMessage: process.env.APPVEYOR_REPO_COMMIT_MESSAGE || 'Build Storybook',
      commitMessageExtended: process.env.APPVEYOR_REPO_COMMIT_MESSAGE_EXTENDED || 'Build Storybook for production',
      tag: process.env.APPVEYOR_REPO_TAG || '',
      tagName: process.env.APPVEYOR_REPO_TAG_NAME || '',
    },
    project: {
      id: process.env.APPVEYOR_PROJECT_ID || '12345678',
      name: process.env.APPVEYOR_PROJECT_NAME || 'nova-pasta',
      slug: process.env.APPVEYOR_PROJECT_SLUG || 'caspian/nova-pasta',
      accountName: process.env.APPVEYOR_ACCOUNT_NAME || 'caspian',
      accountType: process.env.APPVEYOR_ACCOUNT_TYPE || 'github',
      url: process.env.APPVEYOR_PROJECT_URL || 'https://ci.appveyor.com/project/caspian/nova-pasta',
    },
    repository: {
      name: process.env.APPVEYOR_REPO_NAME || 'nova-pasta',
      branch: process.env.APPVEYOR_REPO_BRANCH || 'main',
      tag: process.env.APPVEYOR_REPO_TAG || '',
      commit: process.env.APPVEYOR_REPO_COMMIT || 'abc123def456',
      commitAuthor: process.env.APPVEYOR_REPO_COMMIT_AUTHOR || 'caspian',
      commitAuthorEmail: process.env.APPVEYOR_REPO_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      commitDate: process.env.APPVEYOR_REPO_COMMIT_DATE || '2024-01-01T00:00:00Z',
      commitMessage: process.env.APPVEYOR_REPO_COMMIT_MESSAGE || 'Build Storybook',
      commitMessageExtended: process.env.APPVEYOR_REPO_COMMIT_MESSAGE_EXTENDED || 'Build Storybook for production',
      provider: process.env.APPVEYOR_REPO_PROVIDER || 'github',
      scm: process.env.APPVEYOR_REPO_SCM || 'git',
      url: process.env.APPVEYOR_REPO_URL || 'https://github.com/caspian/nova-pasta',
      remoteUrl: process.env.APPVEYOR_REPO_REMOTE_URL || 'https://github.com/caspian/nova-pasta.git',
    },
    job: {
      id: process.env.APPVEYOR_JOB_ID || '123456789',
      name: process.env.APPVEYOR_JOB_NAME || 'build-storybook',
      number: process.env.APPVEYOR_JOB_NUMBER || '1',
      status: process.env.APPVEYOR_JOB_STATUS || 'success',
      platform: process.env.APPVEYOR_JOB_PLATFORM || 'x64',
      configuration: process.env.APPVEYOR_JOB_CONFIGURATION || 'Release',
      workerImage: process.env.APPVEYOR_JOB_WORKER_IMAGE || 'Visual Studio 2022',
    },
    environment: {
      name: process.env.APPVEYOR_ENVIRONMENT_NAME || 'production',
      url: process.env.APPVEYOR_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.appveyor.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'appveyor',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
  },
  
  // Configurações de cache do AppVeyor
  appveyorCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$APPVEYOR_REPO_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
