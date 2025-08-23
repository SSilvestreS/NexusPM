// Configurações de ambiente para Azure DevOps CI/CD
export const azureDevOpsCicdConfig = {
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
  
  // Configurações do Azure DevOps CI/CD
  azureDevOpsCicd: {
    organization: {
      name: process.env.SYSTEM_TEAMFOUNDATIONCOLLECTIONURI?.split('//')[1]?.split('.')[0] || 'nova-pasta',
      url: process.env.SYSTEM_TEAMFOUNDATIONCOLLECTIONURI || 'https://dev.azure.com/nova-pasta',
    },
    project: {
      id: process.env.SYSTEM_TEAMPROJECTID || '12345678-1234-1234-1234-123456789012',
      name: process.env.SYSTEM_TEAMPROJECT || 'nova-pasta',
      url: process.env.SYSTEM_TEAMPROJECTURI || 'https://dev.azure.com/nova-pasta/nova-pasta',
    },
    pipeline: {
      id: process.env.SYSTEM_PIPELINEID || '123456789',
      name: process.env.SYSTEM_PIPELINENAME || 'nova-pasta-storybook',
      displayName: process.env.SYSTEM_PIPELINEDISPLAYNAME || 'Nova Pasta Storybook',
      version: process.env.SYSTEM_PIPELINEVERSION || '1.0',
    },
    build: {
      id: process.env.BUILD_BUILDID || '123456789',
      number: process.env.BUILD_BUILDNUMBER || '1',
      uri: process.env.BUILD_BUILDURI || 'vstfs:///Build/Build/123456789',
      url: process.env.BUILD_BUILDURI || 'https://dev.azure.com/nova-pasta/nova-pasta/_build/results?buildId=123456789',
      result: process.env.BUILD_RESULT || 'Succeeded',
      reason: process.env.BUILD_REASON || 'IndividualCI',
      requestedFor: process.env.BUILD_REQUESTEDFOR || 'caspian',
      sourceVersion: process.env.BUILD_SOURCEVERSION || 'abc123def456',
      sourceBranch: process.env.BUILD_SOURCEBRANCH || 'refs/heads/main',
      sourceBranchName: process.env.BUILD_SOURCEBRANCHNAME || 'main',
      definitionName: process.env.BUILD_DEFINITIONNAME || 'nova-pasta-storybook',
      definitionId: process.env.BUILD_DEFINITIONID || '123456789',
    },
    repository: {
      name: process.env.BUILD_REPOSITORY_NAME || 'nova-pasta',
      id: process.env.BUILD_REPOSITORY_ID || '12345678-1234-1234-1234-123456789012',
      provider: process.env.BUILD_REPOSITORY_PROVIDER || 'GitHub',
      uri: process.env.BUILD_REPOSITORY_URI || 'https://github.com/caspian/nova-pasta',
      branch: process.env.BUILD_SOURCEBRANCHNAME || 'main',
      commit: process.env.BUILD_SOURCEVERSION || 'abc123def456',
    },
    agent: {
      name: process.env.AGENT_NAME || 'Azure Pipelines 1',
      id: process.env.AGENT_ID || '1',
      machineName: process.env.AGENT_MACHINENAME || 'fv-az123-456',
      os: process.env.AGENT_OS || 'Linux',
      version: process.env.AGENT_VERSION || '2.217.1',
      workingDirectory: process.env.AGENT_WORKFOLDER || '/home/vsts/work',
      tempDirectory: process.env.AGENT_TEMPDIRECTORY || '/home/vsts/work/_temp',
      homeDirectory: process.env.AGENT_HOMEDIRECTORY || '/home/vsts/agents/2.217.1',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.azure.com', '*.github.com'],
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
    provider: process.env.DEPLOY_PROVIDER || 'azure-devops',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      GIT_DEPTH: process.env.GIT_DEPTH || '1',
      GIT_STRATEGY: process.env.GIT_STRATEGY || 'clone',
      GIT_SUBMODULE_STRATEGY: process.env.GIT_SUBMODULE_STRATEGY || 'none',
    },
  },
  
  // Configurações de cache do Azure DevOps CI/CD
  azureDevOpsCicdCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BUILD_SOURCEBRANCHNAME',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
  },
}
