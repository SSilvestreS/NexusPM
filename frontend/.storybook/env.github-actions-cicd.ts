// Configurações de ambiente para GitHub Actions CI/CD
export const githubActionsCicdConfig = {
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
  
  // Configurações do GitHub Actions CI/CD
  githubActionsCicd: {
    workflow: {
      name: process.env.GITHUB_WORKFLOW || 'Build and Deploy Storybook',
      runId: process.env.GITHUB_RUN_ID || '1234567890',
      runNumber: process.env.GITHUB_RUN_NUMBER || '1',
      attempt: process.env.GITHUB_RUN_ATTEMPT || '1',
      displayName: process.env.GITHUB_WORKFLOW || 'Build and Deploy Storybook',
      job: process.env.GITHUB_JOB || 'build-storybook',
      matrix: process.env.GITHUB_MATRIX_CONTEXT || '{}',
    },
    repository: {
      owner: process.env.GITHUB_REPOSITORY_OWNER || 'caspian',
      name: process.env.GITHUB_REPOSITORY_NAME || 'nova-pasta',
      fullName: process.env.GITHUB_REPOSITORY || 'caspian/nova-pasta',
      url: process.env.GITHUB_REPOSITORY_URL || 'https://github.com/caspian/nova-pasta',
      defaultBranch: process.env.GITHUB_DEFAULT_BRANCH || 'main',
      visibility: process.env.GITHUB_REPOSITORY_VISIBILITY || 'public',
    },
    event: {
      name: process.env.GITHUB_EVENT_NAME || 'push',
      path: process.env.GITHUB_EVENT_PATH || '/home/runner/work/_temp/_github_workflow/event.json',
      ref: process.env.GITHUB_REF || 'refs/heads/main',
      refName: process.env.GITHUB_REF_NAME || 'main',
      refType: process.env.GITHUB_REF_TYPE || 'branch',
      sha: process.env.GITHUB_SHA || 'abc123def456',
      headRef: process.env.GITHUB_HEAD_REF || '',
      baseRef: process.env.GITHUB_BASE_REF || '',
      actor: process.env.GITHUB_ACTOR || 'caspian',
      author: process.env.GITHUB_AUTHOR || 'caspian',
      committer: process.env.GITHUB_COMMITTER || 'caspian',
      trigger: process.env.GITHUB_TRIGGERING_ACTOR || 'caspian',
    },
    server: {
      url: process.env.GITHUB_SERVER_URL || 'https://github.com',
      apiUrl: process.env.GITHUB_API_URL || 'https://api.github.com',
      graphqlUrl: process.env.GITHUB_GRAPHQL_URL || 'https://api.github.com/graphql',
    },
    environment: {
      name: process.env.GITHUB_ENV || 'production',
      url: process.env.GITHUB_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
      deploymentUrl: process.env.GITHUB_ENVIRONMENT_DEPLOYMENT_URL || 'https://nova-pasta.example.com',
    },
    runner: {
      name: process.env.RUNNER_NAME || 'GitHub Actions 1',
      os: process.env.RUNNER_OS || 'Linux',
      arch: process.env.RUNNER_ARCH || 'X64',
      temp: process.env.RUNNER_TEMP || '/home/runner/work/_temp',
      toolCache: process.env.RUNNER_TOOL_CACHE || '/opt/hostedtoolcache',
      workspace: process.env.GITHUB_WORKSPACE || '/home/runner/work/nova-pasta/nova-pasta',
      environment: process.env.RUNNER_ENVIRONMENT || 'github-hosted',
    },
    actions: {
      cache: process.env.ACTIONS_CACHE_URL || 'https://actions-cache.github.com',
      runtimeUrl: process.env.ACTIONS_RUNTIME_URL || 'https://actions-runtime.github.com',
      runtimeToken: process.env.ACTIONS_RUNTIME_TOKEN || '',
      stepSummary: process.env.GITHUB_STEP_SUMMARY || '/home/runner/work/_temp/_github_workflow/step_summary_1.md',
      stepDebug: process.env.GITHUB_STEP_DEBUG || 'false',
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
      name: process.env.ARTIFACT_NAME || 'storybook-build',
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
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
      GIT_FETCH_EXTRA_FLAGS: process.env.GIT_FETCH_EXTRA_FLAGS || '',
      GIT_LFS_SKIP_SMUDGE: process.env.GIT_LFS_SKIP_SMUDGE || '0',
    },
  },
  
  // Configurações de cache do GitHub Actions CI/CD
  githubActionsCicdCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-${{ github.ref_name }}',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    restoreKeys: process.env.CACHE_RESTORE_KEYS?.split(',') || ['storybook-'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
