// Configurações de ambiente para Concourse CI
export const concourseConfig = {
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
  
  // Configurações do Concourse CI
  concourse: {
    server: {
      url: process.env.CONCOURSE_URL || 'https://concourse.example.com',
      name: process.env.CONCOURSE_NAME || 'Concourse',
      version: process.env.CONCOURSE_VERSION || '7.10.0',
    },
    pipeline: {
      name: process.env.CONCOURSE_PIPELINE_NAME || 'nova-pasta-storybook',
      instanceVars: process.env.CONCOURSE_PIPELINE_INSTANCE_VARS || '{}',
      team: process.env.CONCOURSE_TEAM || 'main',
      url: process.env.CONCOURSE_PIPELINE_URL || 'https://concourse.example.com/teams/main/pipelines/nova-pasta-storybook',
    },
    build: {
      id: process.env.CONCOURSE_BUILD_ID || '123456789',
      name: process.env.CONCOURSE_BUILD_NAME || '1',
      jobName: process.env.CONCOURSE_BUILD_JOB_NAME || 'build-storybook',
      pipelineName: process.env.CONCOURSE_BUILD_PIPELINE_NAME || 'nova-pasta-storybook',
      teamName: process.env.CONCOURSE_BUILD_TEAM_NAME || 'main',
      url: process.env.CONCOURSE_BUILD_URL || 'https://concourse.example.com/teams/main/pipelines/nova-pasta-storybook/jobs/build-storybook/builds/1',
      startTime: process.env.CONCOURSE_BUILD_START_TIME || '1640995200',
      endTime: process.env.CONCOURSE_BUILD_END_TIME || '1640995500',
      status: process.env.CONCOURSE_BUILD_STATUS || 'succeeded',
      cause: process.env.CONCOURSE_BUILD_CAUSE || 'manual',
    },
    task: {
      name: process.env.CONCOURSE_TASK_NAME || 'build-storybook',
      stepName: process.env.CONCOURSE_TASK_STEP_NAME || 'build-storybook',
      planId: process.env.CONCOURSE_TASK_PLAN_ID || '123456789',
      containerId: process.env.CONCOURSE_TASK_CONTAINER_ID || 'container-123456789',
    },
    worker: {
      name: process.env.CONCOURSE_WORKER_NAME || 'worker-1',
      platform: process.env.CONCOURSE_WORKER_PLATFORM || 'linux',
      tags: process.env.CONCOURSE_WORKER_TAGS?.split(',') || ['docker', 'linux'],
      version: process.env.CONCOURSE_WORKER_VERSION || '7.10.0',
    },
    resource: {
      name: process.env.CONCOURSE_RESOURCE_NAME || 'nova-pasta',
      type: process.env.CONCOURSE_RESOURCE_TYPE || 'git',
      version: process.env.CONCOURSE_RESOURCE_VERSION || '{"ref":"abc123def456"}',
      metadata: process.env.CONCOURSE_RESOURCE_METADATA || '{}',
    },
    environment: {
      home: process.env.CONCOURSE_HOME || '/home/concourse',
      working: process.env.CONCOURSE_WORKING_DIRECTORY || '/tmp/build',
      temp: process.env.CONCOURSE_TEMP || '/tmp',
      system: process.env.CONCOURSE_SYSTEM_DIR || '/opt/concourse',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.concourse.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'concourse',
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
  
  // Configurações de cache do Concourse CI
  concourseCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CONCOURSE_BUILD_JOB_NAME',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    when: process.env.CACHE_WHEN || 'on_success',
  },
}
