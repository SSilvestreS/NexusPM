// Configurações de ambiente para CircleCI
export const circleciConfig = {
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
  
  // Configurações do CircleCI
  circleci: {
    project: {
      name: process.env.CIRCLE_PROJECT_NAME || 'nova-pasta',
      username: process.env.CIRCLE_PROJECT_USERNAME || 'caspian',
      reponame: process.env.CIRCLE_PROJECT_REPONAME || 'nova-pasta',
      url: process.env.CIRCLE_PROJECT_URL || 'https://github.com/caspian/nova-pasta',
    },
    build: {
      num: process.env.CIRCLE_BUILD_NUM || '1',
      url: process.env.CIRCLE_BUILD_URL || 'https://circleci.com/gh/caspian/nova-pasta/1',
      job: process.env.CIRCLE_JOB || 'build-storybook',
      nodeIndex: process.env.CIRCLE_NODE_INDEX || '0',
      nodeTotal: process.env.CIRCLE_NODE_TOTAL || '1',
    },
    workflow: {
      id: process.env.CIRCLE_WORKFLOW_ID || '12345678-1234-1234-1234-123456789012',
      jobId: process.env.CIRCLE_WORKFLOW_JOB_ID || '12345678-1234-1234-1234-123456789012',
      workspaceId: process.env.CIRCLE_WORKFLOW_WORKSPACE_ID || '12345678-1234-1234-1234-123456789012',
    },
    git: {
      branch: process.env.CIRCLE_BRANCH || 'main',
      tag: process.env.CIRCLE_TAG || '',
      commit: process.env.CIRCLE_SHA1 || 'abc123def456',
      commitRange: process.env.CIRCLE_COMPARE_URL || 'https://github.com/caspian/nova-pasta/compare/abc123...def456',
    },
    environment: {
      home: process.env.CIRCLE_HOME || '/home/circleci',
      workspace: process.env.CIRCLE_WORKING_DIRECTORY || '/home/circleci/project',
      temp: process.env.CIRCLE_TEMP || '/tmp',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.circleci.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'circleci',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do CircleCI
  circleciCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CIRCLE_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
