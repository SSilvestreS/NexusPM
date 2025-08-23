// Configurações de ambiente para Travis CI
export const travisConfig = {
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
  
  // Configurações do Travis CI
  travis: {
    build: {
      id: process.env.TRAVIS_BUILD_ID || '123456789',
      number: process.env.TRAVIS_BUILD_NUMBER || '1',
      jobId: process.env.TRAVIS_JOB_ID || '123456789',
      jobNumber: process.env.TRAVIS_JOB_NUMBER || '1.1',
      url: process.env.TRAVIS_BUILD_WEB_URL || 'https://travis-ci.com/caspian/nova-pasta/builds/123456789',
    },
    repository: {
      slug: process.env.TRAVIS_REPO_SLUG || 'caspian/nova-pasta',
      name: process.env.TRAVIS_REPO_SLUG?.split('/')[1] || 'nova-pasta',
      owner: process.env.TRAVIS_REPO_SLUG?.split('/')[0] || 'caspian',
      branch: process.env.TRAVIS_BRANCH || 'main',
      commit: process.env.TRAVIS_COMMIT || 'abc123def456',
      commitRange: process.env.TRAVIS_COMMIT_RANGE || 'abc123...def456',
      pullRequest: process.env.TRAVIS_PULL_REQUEST || 'false',
      pullRequestBranch: process.env.TRAVIS_PULL_REQUEST_BRANCH || '',
      pullRequestSha: process.env.TRAVIS_PULL_REQUEST_SHA || '',
    },
    environment: {
      os: process.env.TRAVIS_OS_NAME || 'linux',
      dist: process.env.TRAVIS_DIST || 'bionic',
      arch: process.env.TRAVIS_ARCH || 'amd64',
      language: process.env.TRAVIS_LANGUAGE || 'node_js',
      nodeVersion: process.env.TRAVIS_NODE_VERSION || '18',
      npmVersion: process.env.TRAVIS_NPM_VERSION || '9',
    },
    system: {
      home: process.env.TRAVIS_HOME || '/home/travis',
      root: process.env.TRAVIS_ROOT || '/',
      temp: process.env.TRAVIS_TMPDIR || '/tmp',
      cache: process.env.TRAVIS_CACHE_DIR || '/home/travis/.cache',
    },
    ci: {
      enabled: process.env.CI === 'true',
      provider: 'travis',
      eventType: process.env.TRAVIS_EVENT_TYPE || 'push',
      tag: process.env.TRAVIS_TAG || '',
      secure: process.env.TRAVIS_SECURE_ENV_VARS === 'true',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.travis-ci.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'travis',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do Travis CI
  travisCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$TRAVIS_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
