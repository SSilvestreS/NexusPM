// Configurações de ambiente para GitHub Actions
export const githubActionsConfig = {
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
  
  // Configurações do GitHub Actions
  githubActions: {
    workflow: {
      name: process.env.GITHUB_WORKFLOW || 'Build Storybook',
      runId: process.env.GITHUB_RUN_ID || '1234567890',
      runNumber: process.env.GITHUB_RUN_NUMBER || '1',
      attempt: process.env.GITHUB_RUN_ATTEMPT || '1',
      job: process.env.GITHUB_JOB || 'build-storybook',
      matrix: process.env.GITHUB_MATRIX || '{}',
    },
    repository: {
      owner: process.env.GITHUB_REPOSITORY_OWNER || 'caspian',
      name: process.env.GITHUB_REPOSITORY || 'caspian/nova-pasta',
      fullName: process.env.GITHUB_REPOSITORY || 'caspian/nova-pasta',
      url: process.env.GITHUB_REPOSITORY_URL || 'https://github.com/caspian/nova-pasta',
    },
    ref: {
      name: process.env.GITHUB_REF_NAME || 'main',
      ref: process.env.GITHUB_REF || 'refs/heads/main',
      sha: process.env.GITHUB_SHA || 'abc123def456',
      headRef: process.env.GITHUB_HEAD_REF || '',
      baseRef: process.env.GITHUB_BASE_REF || '',
    },
    actor: {
      name: process.env.GITHUB_ACTOR || 'caspian',
      email: process.env.GITHUB_ACTOR_EMAIL || 'caspian@example.com',
    },
    server: {
      url: process.env.GITHUB_SERVER_URL || 'https://github.com',
      apiUrl: process.env.GITHUB_API_URL || 'https://api.github.com',
      graphqlUrl: process.env.GITHUB_GRAPHQL_URL || 'https://api.github.com/graphql',
    },
    environment: {
      workspace: process.env.GITHUB_WORKSPACE || '/home/runner/work/nova-pasta/nova-pasta',
      eventPath: process.env.GITHUB_EVENT_PATH || '/home/runner/work/_temp/_github_workflow/event.json',
      stepSummary: process.env.GITHUB_STEP_SUMMARY || '/home/runner/work/_temp/_github_workflow/step_summary_1.md',
      env: process.env.GITHUB_ENV || '/home/runner/work/_temp/_github_workflow/command_1.env',
      path: process.env.GITHUB_PATH || '/home/runner/work/_temp/_github_workflow/command_1.txt',
      output: process.env.GITHUB_OUTPUT || '/home/runner/work/_temp/_github_workflow/command_1.txt',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.github.com', '*.githubusercontent.com'],
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
      retentionDays: parseInt(process.env.ARTIFACT_RETENTION_DAYS || '90'),
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'github-actions',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GITHUB_TOKEN: process.env.GITHUB_TOKEN || '',
      GITHUB_PAT: process.env.GITHUB_PAT || '',
      DEPLOY_KEY: process.env.DEPLOY_KEY || '',
    },
  },
  
  // Configurações de cache do GitHub Actions
  githubActionsCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-${{ github.ref }}',
    restoreKeys: process.env.CACHE_RESTORE_KEYS?.split(',') || ['storybook-'],
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    version: process.env.CACHE_VERSION || '1',
  },
  
  // Configurações de segurança
  security: {
    enableDependencyReview: process.env.ENABLE_DEPENDENCY_REVIEW === 'true',
    enableCodeScanning: process.env.ENABLE_CODE_SCANNING === 'true',
    enableSecretScanning: process.env.ENABLE_SECRET_SCANNING === 'true',
    enableVulnerabilityAlerts: process.env.ENABLE_VULNERABILITY_ALERTS === 'true',
  },
}
