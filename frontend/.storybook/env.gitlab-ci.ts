// Configurações de ambiente para GitLab CI
export const gitlabCiConfig = {
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
  
  // Configurações do GitLab CI
  gitlabCi: {
    project: {
      id: process.env.CI_PROJECT_ID || '12345',
      name: process.env.CI_PROJECT_NAME || 'nova-pasta',
      path: process.env.CI_PROJECT_PATH || 'caspian/nova-pasta',
      url: process.env.CI_PROJECT_URL || 'https://gitlab.com/caspian/nova-pasta',
      namespace: process.env.CI_PROJECT_NAMESPACE || 'caspian',
      title: process.env.CI_PROJECT_TITLE || 'Nova Pasta',
    },
    pipeline: {
      id: process.env.CI_PIPELINE_ID || '12345',
      url: process.env.CI_PIPELINE_URL || 'https://gitlab.com/caspian/nova-pasta/-/pipelines/12345',
      source: process.env.CI_PIPELINE_SOURCE || 'push',
      trigger: process.env.CI_PIPELINE_TRIGGER || 'push',
    },
    job: {
      id: process.env.CI_JOB_ID || '12345',
      name: process.env.CI_JOB_NAME || 'build-storybook',
      stage: process.env.CI_JOB_STAGE || 'build',
      url: process.env.CI_JOB_URL || 'https://gitlab.com/caspian/nova-pasta/-/jobs/12345',
      manual: process.env.CI_JOB_MANUAL === 'true',
      when: process.env.CI_JOB_WHEN || 'on_success',
    },
    commit: {
      sha: process.env.CI_COMMIT_SHA || 'abc123def456',
      shortSha: process.env.CI_COMMIT_SHORT_SHA || 'abc123',
      refName: process.env.CI_COMMIT_REF_NAME || 'main',
      refSlug: process.env.CI_COMMIT_REF_SLUG || 'main',
      title: process.env.CI_COMMIT_TITLE || 'Update storybook',
      message: process.env.CI_COMMIT_MESSAGE || 'Update storybook configuration',
      author: process.env.CI_COMMIT_AUTHOR || 'Caspian <caspian@example.com>',
      timestamp: process.env.CI_COMMIT_TIMESTAMP || '2024-01-01T00:00:00Z',
    },
    repository: {
      url: process.env.CI_REPOSITORY_URL || 'https://gitlab.com/caspian/nova-pasta.git',
      name: process.env.CI_REPOSITORY_NAME || 'nova-pasta',
      description: process.env.CI_REPOSITORY_DESCRIPTION || 'Nova Pasta Project',
      homepage: process.env.CI_REPOSITORY_HOMEPAGE || 'https://gitlab.com/caspian/nova-pasta',
      language: process.env.CI_REPOSITORY_LANGUAGE || 'TypeScript',
    },
    runner: {
      id: process.env.CI_RUNNER_ID || '12345',
      description: process.env.CI_RUNNER_DESCRIPTION || 'GitLab Runner',
      tags: process.env.CI_RUNNER_TAGS?.split(',') || ['docker', 'linux'],
      version: process.env.CI_RUNNER_VERSION || '15.0.0',
      executor: process.env.CI_RUNNER_EXECUTOR || 'docker',
    },
    environment: {
      name: process.env.CI_ENVIRONMENT_NAME || 'production',
      url: process.env.CI_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
      tier: process.env.CI_ENVIRONMENT_TIER || 'production',
    },
    variables: {
      gitDepth: process.env.GIT_DEPTH || '1',
      gitStrategy: process.env.GIT_STRATEGY || 'clone',
      gitSubmoduleStrategy: process.env.GIT_SUBMODULE_STRATEGY || 'none',
      gitFetchExtraFlags: process.env.GIT_FETCH_EXTRA_FLAGS || '',
      gitLfsSkipSmudge: process.env.GIT_LFS_SKIP_SMUDGE || '0',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.gitlab.com', '*.gitlab.io'],
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
      expireIn: process.env.ARTIFACT_EXPIRE_IN || '30 days',
      reports: process.env.ARTIFACT_REPORTS?.split(',') || [],
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'gitlab-ci',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      DEPLOY_USER: process.env.DEPLOY_USER || 'gitlab-runner',
      DEPLOY_KEY: process.env.DEPLOY_KEY || '',
      DEPLOY_HOST: process.env.DEPLOY_HOST || 'localhost',
      DEPLOY_PORT: process.env.DEPLOY_PORT || '22',
    },
  },
  
  // Configurações de cache do GitLab CI
  gitlabCiCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CI_COMMIT_REF_SLUG',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    when: process.env.CACHE_WHEN || 'on_success',
  },
}
