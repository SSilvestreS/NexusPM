// Configurações de ambiente para GitLab CI/CD
export const gitlabCicdConfig = {
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
  
  // Configurações do GitLab CI/CD
  gitlabCicd: {
    project: {
      id: process.env.CI_PROJECT_ID || '12345678',
      name: process.env.CI_PROJECT_NAME || 'nova-pasta',
      path: process.env.CI_PROJECT_PATH || 'caspian/nova-pasta',
      url: process.env.CI_PROJECT_URL || 'https://gitlab.com/caspian/nova-pasta',
      namespace: process.env.CI_PROJECT_NAMESPACE || 'caspian',
      description: process.env.CI_PROJECT_DESCRIPTION || 'Nova Pasta Project',
    },
    pipeline: {
      id: process.env.CI_PIPELINE_ID || '123456789',
      url: process.env.CI_PIPELINE_URL || 'https://gitlab.com/caspian/nova-pasta/-/pipelines/123456789',
      source: process.env.CI_PIPELINE_SOURCE || 'push',
      trigger: process.env.CI_PIPELINE_TRIGGER_ID || '',
      user: process.env.GITLAB_USER_NAME || 'caspian',
      userEmail: process.env.GITLAB_USER_EMAIL || 'caspian@example.com',
      userLogin: process.env.GITLAB_USER_LOGIN || 'caspian',
    },
    job: {
      id: process.env.CI_JOB_ID || '123456789',
      name: process.env.CI_JOB_NAME || 'build-storybook',
      stage: process.env.CI_JOB_STAGE || 'build',
      url: process.env.CI_JOB_URL || 'https://gitlab.com/caspian/nova-pasta/-/jobs/123456789',
      manual: process.env.CI_JOB_MANUAL === 'true',
      when: process.env.CI_JOB_WHEN || 'on_success',
      allowFailure: process.env.CI_JOB_ALLOW_FAILURE === 'true',
    },
    commit: {
      sha: process.env.CI_COMMIT_SHA || 'abc123def456',
      shortSha: process.env.CI_COMMIT_SHORT_SHA || 'abc123',
      beforeSha: process.env.CI_COMMIT_BEFORE_SHA || 'def456abc123',
      ref: process.env.CI_COMMIT_REF_NAME || 'main',
      refSlug: process.env.CI_COMMIT_REF_SLUG || 'main',
      tag: process.env.CI_COMMIT_TAG || '',
      message: process.env.CI_COMMIT_MESSAGE || 'Build Storybook',
      author: process.env.CI_COMMIT_AUTHOR || 'caspian <caspian@example.com>',
      timestamp: process.env.CI_COMMIT_TIMESTAMP || '2024-01-01T00:00:00Z',
    },
    repository: {
      url: process.env.CI_REPOSITORY_URL || 'https://gitlab.com/caspian/nova-pasta.git',
      name: process.env.CI_REPOSITORY_NAME || 'caspian/nova-pasta',
      path: process.env.CI_REPOSITORY_PATH || 'caspian/nova-pasta',
      branch: process.env.CI_COMMIT_REF_NAME || 'main',
      tag: process.env.CI_COMMIT_TAG || '',
      defaultBranch: process.env.CI_DEFAULT_BRANCH || 'main',
    },
    runner: {
      id: process.env.CI_RUNNER_ID || '123456',
      description: process.env.CI_RUNNER_DESCRIPTION || 'gitlab-runner',
      tags: process.env.CI_RUNNER_TAGS?.split(',') || ['docker', 'linux'],
      executor: process.env.CI_RUNNER_EXECUTOR_ARCH || 'linux/amd64',
      version: process.env.CI_RUNNER_VERSION || '15.0.0',
    },
    environment: {
      name: process.env.CI_ENVIRONMENT_NAME || 'production',
      url: process.env.CI_ENVIRONMENT_URL || 'https://nova-pasta.example.com',
      action: process.env.CI_ENVIRONMENT_ACTION || 'start',
      tier: process.env.CI_ENVIRONMENT_TIER || 'production',
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
      expireIn: process.env.ARTIFACT_EXPIRE_IN || '1 week',
      reports: {
        junit: process.env.JUNIT_REPORT_PATH || 'junit.xml',
        coverage: process.env.COVERAGE_REPORT_PATH || 'coverage.xml',
      },
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'gitlab',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
      GIT_CLEAN_FLAGS: process.env.GIT_CLEAN_FLAGS || '-ffdx',
      GIT_FETCH_EXTRA_FLAGS: process.env.GIT_FETCH_EXTRA_FLAGS || '',
    },
  },
  
  // Configurações de cache do GitLab CI/CD
  gitlabCicdCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$CI_COMMIT_REF_SLUG',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    when: process.env.CACHE_WHEN || 'on_success',
  },
}
