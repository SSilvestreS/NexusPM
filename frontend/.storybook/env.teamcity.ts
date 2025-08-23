// Configurações de ambiente para TeamCity
export const teamcityConfig = {
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
  
  // Configurações do TeamCity
  teamcity: {
    server: {
      url: process.env.TEAMCITY_SERVER_URL || 'http://teamcity.example.com',
      name: process.env.TEAMCITY_SERVER_NAME || 'TeamCity',
      version: process.env.TEAMCITY_VERSION || '2023.11',
    },
    project: {
      id: process.env.TEAMCITY_PROJECT_ID || 'NovaPasta_Storybook',
      name: process.env.TEAMCITY_PROJECT_NAME || 'Nova Pasta Storybook',
      displayName: process.env.TEAMCITY_PROJECT_NAME || 'Nova Pasta Storybook',
    },
    build: {
      id: process.env.TEAMCITY_BUILD_ID || '123456789',
      number: process.env.TEAMCITY_BUILD_NUMBER || '1',
      type: process.env.TEAMCITY_BUILD_TYPE_ID || 'NovaPasta_Storybook_Build',
      typeName: process.env.TEAMCITY_BUILD_TYPE_NAME || 'Build Storybook',
      url: process.env.TEAMCITY_BUILD_URL || 'http://teamcity.example.com/viewLog.html?buildId=123456789',
      timestamp: process.env.TEAMCITY_BUILD_TIMESTAMP || '2024-01-01T00:00:00Z',
      duration: process.env.TEAMCITY_BUILD_DURATION || '300000',
      result: process.env.TEAMCITY_BUILD_RESULT || 'SUCCESS',
    },
    agent: {
      name: process.env.TEAMCITY_AGENT_NAME || 'build-agent-1',
      os: process.env.TEAMCITY_AGENT_OS || 'linux',
      host: process.env.TEAMCITY_AGENT_HOST || 'build-agent-1.example.com',
      port: process.env.TEAMCITY_AGENT_PORT || '9090',
    },
    vcs: {
      branch: process.env.TEAMCITY_VCS_BRANCH || 'main',
      commit: process.env.TEAMCITY_VCS_COMMIT || 'abc123def456',
      root: process.env.TEAMCITY_VCS_ROOT || 'nova-pasta',
      url: process.env.TEAMCITY_VCS_ROOT_URL || 'https://github.com/caspian/nova-pasta.git',
    },
    environment: {
      home: process.env.TEAMCITY_AGENT_HOME || '/opt/teamcity-agent',
      working: process.env.TEAMCITY_AGENT_WORK_DIR || '/opt/teamcity-agent/work',
      temp: process.env.TEAMCITY_AGENT_TEMP || '/tmp',
      system: process.env.TEAMCITY_AGENT_SYSTEM_DIR || '/opt/teamcity-agent/system',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.teamcity.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'teamcity',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do TeamCity
  teamcityCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$TEAMCITY_VCS_BRANCH',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
