// Configurações de ambiente para GitHub Pages
export const githubPagesConfig = {
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
  
  // Configurações do GitHub Pages
  githubPages: {
    repository: {
      owner: process.env.GITHUB_REPOSITORY_OWNER || 'caspian',
      name: process.env.GITHUB_REPOSITORY_NAME || 'nova-pasta',
      url: process.env.GITHUB_REPOSITORY_URL || 'https://github.com/caspian/nova-pasta',
    },
    deployment: {
      branch: process.env.GITHUB_PAGES_BRANCH || 'gh-pages',
      environment: process.env.GITHUB_PAGES_ENVIRONMENT || 'github-pages',
      url: process.env.GITHUB_PAGES_URL || 'https://caspian.github.io/nova-pasta',
    },
    workflow: {
      file: process.env.GITHUB_WORKFLOW_FILE || '.github/workflows/deploy-storybook.yml',
      runId: process.env.GITHUB_RUN_ID || '1234567890',
      runNumber: process.env.GITHUB_RUN_NUMBER || '1',
      actor: process.env.GITHUB_ACTOR || 'caspian',
      event: process.env.GITHUB_EVENT_NAME || 'push',
    },
    actions: {
      workspace: process.env.GITHUB_WORKSPACE || '/home/runner/work/nova-pasta/nova-pasta',
      temp: process.env.RUNNER_TEMP || '/home/runner/work/_temp',
      toolCache: process.env.RUNNER_TOOL_CACHE || '/opt/hostedtoolcache',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.github.io', '*.github.com'],
  },
  
  // Configurações de build
  build: {
    command: process.env.BUILD_COMMAND || 'npm run build:storybook',
    outputDir: process.env.OUTPUT_DIR || '../storybook-static',
    sourceDir: process.env.SOURCE_DIR || '../src',
    publicDir: process.env.PUBLIC_DIR || '../public',
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'github-pages',
    branch: process.env.DEPLOY_BRANCH || 'gh-pages',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    message: process.env.DEPLOY_MESSAGE || 'Deploy Storybook to GitHub Pages',
    force: process.env.DEPLOY_FORCE === 'true',
  },
  
  // Configurações de Jekyll
  jekyll: {
    enabled: process.env.JEKYLL_ENABLED === 'true',
    configFile: process.env.JEKYLL_CONFIG_FILE || '_config.yml',
    sourceDir: process.env.JEKYLL_SOURCE_DIR || '../storybook-static',
    destinationDir: process.env.JEKYLL_DESTINATION_DIR || '../storybook-static',
    plugins: process.env.JEKYLL_PLUGINS?.split(',') || ['jekyll-seo-tag', 'jekyll-sitemap'],
  },
}
