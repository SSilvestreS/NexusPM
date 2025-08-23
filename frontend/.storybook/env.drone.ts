// Configurações de ambiente para Drone CI
export const droneConfig = {
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
  
  // Configurações do Drone CI
  drone: {
    server: {
      host: process.env.DRONE_SERVER_HOST || 'drone.example.com',
      proto: process.env.DRONE_SERVER_PROTO || 'https',
      url: process.env.DRONE_SERVER || 'https://drone.example.com',
      version: process.env.DRONE_VERSION || '2.0.0',
    },
    build: {
      number: process.env.DRONE_BUILD_NUMBER || '1',
      event: process.env.DRONE_BUILD_EVENT || 'push',
      action: process.env.DRONE_BUILD_ACTION || 'created',
      status: process.env.DRONE_BUILD_STATUS || 'success',
      link: process.env.DRONE_BUILD_LINK || 'https://drone.example.com/caspian/nova-pasta/1',
      started: process.env.DRONE_BUILD_STARTED || '1640995200',
      finished: process.env.DRONE_BUILD_FINISHED || '1640995500',
      created: process.env.DRONE_BUILD_CREATED || '1640995200',
      updated: process.env.DRONE_BUILD_UPDATED || '1640995500',
      deployTo: process.env.DRONE_DEPLOY_TO || '',
      environment: process.env.DRONE_DEPLOY_ENVIRONMENT || 'production',
      target: process.env.DRONE_DEPLOY_TARGET || '',
    },
    commit: {
      sha: process.env.DRONE_COMMIT_SHA || 'abc123def456',
      ref: process.env.DRONE_COMMIT_REF || 'refs/heads/main',
      branch: process.env.DRONE_COMMIT_BRANCH || 'main',
      tag: process.env.DRONE_COMMIT_TAG || '',
      message: process.env.DRONE_COMMIT_MESSAGE || 'Build Storybook',
      author: process.env.DRONE_COMMIT_AUTHOR || 'caspian <caspian@example.com>',
      authorName: process.env.DRONE_COMMIT_AUTHOR_NAME || 'caspian',
      authorEmail: process.env.DRONE_COMMIT_AUTHOR_EMAIL || 'caspian@example.com',
      authorAvatar: process.env.DRONE_COMMIT_AUTHOR_AVATAR || 'https://github.com/caspian.png',
      before: process.env.DRONE_COMMIT_BEFORE || 'def456abc123',
      after: process.env.DRONE_COMMIT_AFTER || 'abc123def456',
    },
    repository: {
      name: process.env.DRONE_REPO_NAME || 'nova-pasta',
      namespace: process.env.DRONE_REPO_NAMESPACE || 'caspian',
      fullName: process.env.DRONE_REPO || 'caspian/nova-pasta',
      link: process.env.DRONE_REPO_LINK || 'https://github.com/caspian/nova-pasta',
      clone: process.env.DRONE_REPO_CLONE || 'https://github.com/caspian/nova-pasta.git',
      branch: process.env.DRONE_REPO_BRANCH || 'main',
      private: process.env.DRONE_REPO_PRIVATE === 'true',
      visibility: process.env.DRONE_REPO_VISIBILITY || 'public',
      trusted: process.env.DRONE_REPO_TRUSTED === 'true',
      timeout: parseInt(process.env.DRONE_REPO_TIMEOUT || '60'),
    },
    stage: {
      name: process.env.DRONE_STAGE_NAME || 'build',
      number: process.env.DRONE_STAGE_NUMBER || '1',
      kind: process.env.DRONE_STAGE_KIND || 'pipeline',
      type: process.env.DRONE_STAGE_TYPE || 'docker',
      name: process.env.DRONE_STAGE_NAME || 'build',
      status: process.env.DRONE_STAGE_STATUS || 'success',
      started: process.env.DRONE_STAGE_STARTED || '1640995200',
      finished: process.env.DRONE_STAGE_FINISHED || '1640995500',
      dependsOn: process.env.DRONE_STAGE_DEPENDS_ON?.split(',') || [],
      machine: process.env.DRONE_STAGE_MACHINE || '',
      os: process.env.DRONE_STAGE_OS || 'linux',
      arch: process.env.DRONE_STAGE_ARCH || 'amd64',
      variant: process.env.DRONE_STAGE_VARIANT || '',
      version: process.env.DRONE_STAGE_VERSION || '1.0.0',
    },
    step: {
      name: process.env.DRONE_STEP_NAME || 'build-storybook',
      number: process.env.DRONE_STEP_NUMBER || '1',
      status: process.env.DRONE_STEP_STATUS || 'success',
      started: process.env.DRONE_STEP_STARTED || '1640995200',
      finished: process.env.DRONE_STEP_FINISHED || '1640995500',
      dependsOn: process.env.DRONE_STEP_DEPENDS_ON?.split(',') || [],
      environment: process.env.DRONE_STEP_ENVIRONMENT || 'production',
    },
    system: {
      arch: process.env.DRONE_SYSTEM_ARCH || 'linux/amd64',
      hostname: process.env.DRONE_SYSTEM_HOSTNAME || 'drone-runner-1',
      platform: process.env.DRONE_SYSTEM_PLATFORM || 'linux',
      version: process.env.DRONE_SYSTEM_VERSION || '1.0.0',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.drone.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'drone',
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
  
  // Configurações de cache do Drone CI
  droneCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$DRONE_COMMIT_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    when: process.env.CACHE_WHEN || 'on_success',
  },
}
