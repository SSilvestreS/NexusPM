// Configurações de ambiente para GoCD
export const gocdConfig = {
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
  
  // Configurações do GoCD
  gocd: {
    server: {
      url: process.env.GO_SERVER_URL || 'https://gocd.example.com',
      name: process.env.GO_SERVER_NAME || 'GoCD',
      version: process.env.GO_SERVER_VERSION || '23.1.0',
    },
    pipeline: {
      name: process.env.GO_PIPELINE_NAME || 'nova-pasta-storybook',
      counter: process.env.GO_PIPELINE_COUNTER || '1',
      label: process.env.GO_PIPELINE_LABEL || '1.0.0',
      groupName: process.env.GO_PIPELINE_GROUP_NAME || 'nova-pasta',
      url: process.env.GO_PIPELINE_URL || 'https://gocd.example.com/go/pipelines/nova-pasta-storybook/1',
    },
    stage: {
      name: process.env.GO_STAGE_NAME || 'build',
      counter: process.env.GO_STAGE_COUNTER || '1',
      url: process.env.GO_STAGE_URL || 'https://gocd.example.com/go/pipelines/nova-pasta-storybook/1/build/1',
      result: process.env.GO_STAGE_RESULT || 'Passed',
      state: process.env.GO_STAGE_STATE || 'Passed',
      approvalType: process.env.GO_STAGE_APPROVAL_TYPE || 'success',
      approvedBy: process.env.GO_STAGE_APPROVED_BY || 'caspian',
    },
    job: {
      name: process.env.GO_JOB_NAME || 'build-storybook',
      counter: process.env.GO_JOB_COUNTER || '1',
      url: process.env.GO_JOB_URL || 'https://gocd.example.com/go/tab/build/detail/nova-pasta-storybook/1/build/1/build-storybook',
      result: process.env.GO_JOB_RESULT || 'Passed',
      state: process.env.GO_JOB_STATE || 'Passed',
      duration: process.env.GO_JOB_DURATION || '300',
      scheduledDate: process.env.GO_JOB_SCHEDULED_DATE || '1640995200',
      completedDate: process.env.GO_JOB_COMPLETED_DATE || '1640995500',
    },
    environment: {
      name: process.env.GO_ENVIRONMENT_NAME || 'production',
      variables: process.env.GO_ENVIRONMENT_VARIABLES || '{}',
    },
    agent: {
      name: process.env.GO_AGENT_NAME || 'agent-1',
      hostname: process.env.GO_AGENT_HOSTNAME || 'agent-1.example.com',
      ip: process.env.GO_AGENT_IP || '192.168.1.100',
      os: process.env.GO_AGENT_OS || 'Linux',
      arch: process.env.GO_AGENT_ARCH || 'amd64',
      version: process.env.GO_AGENT_VERSION || '23.1.0',
      workingDirectory: process.env.GO_AGENT_WORKING_DIRECTORY || '/var/lib/go-agent',
      tempDirectory: process.env.GO_AGENT_TEMP_DIRECTORY || '/tmp',
    },
    material: {
      type: process.env.GO_MATERIAL_TYPE || 'git',
      name: process.env.GO_MATERIAL_NAME || 'nova-pasta',
      url: process.env.GO_MATERIAL_URL || 'https://github.com/caspian/nova-pasta.git',
      branch: process.env.GO_MATERIAL_BRANCH || 'main',
      revision: process.env.GO_MATERIAL_REVISION || 'abc123def456',
      destination: process.env.GO_MATERIAL_DESTINATION || 'nova-pasta',
    },
    trigger: {
      user: process.env.GO_TRIGGER_USER || 'caspian',
      cause: process.env.GO_TRIGGER_CAUSE || 'manual',
      timestamp: process.env.GO_TRIGGER_TIMESTAMP || '1640995200',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.gocd.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'gocd',
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
  
  // Configurações de cache do GoCD
  gocdCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$GO_PIPELINE_NAME',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    when: process.env.CACHE_WHEN || 'on_success',
  },
}
