// Configurações de ambiente para Jenkins
export const jenkinsConfig = {
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
  
  // Configurações do Jenkins
  jenkins: {
    server: {
      url: process.env.JENKINS_URL || 'http://localhost:8080',
      name: process.env.JENKINS_NAME || 'Jenkins',
      version: process.env.JENKINS_VERSION || '2.387.3',
    },
    job: {
      name: process.env.JOB_NAME || 'nova-pasta-storybook',
      displayName: process.env.JOB_DISPLAY_NAME || 'Nova Pasta Storybook',
      url: process.env.JOB_URL || 'http://localhost:8080/job/nova-pasta-storybook',
      buildNumber: process.env.BUILD_NUMBER || '1',
      buildId: process.env.BUILD_ID || '1',
      buildTag: process.env.BUILD_TAG || 'jenkins-nova-pasta-storybook-1',
      buildUrl: process.env.BUILD_URL || 'http://localhost:8080/job/nova-pasta-storybook/1',
      buildDisplayName: process.env.BUILD_DISPLAY_NAME || '#1',
      buildTimestamp: process.env.BUILD_TIMESTAMP || '2024-01-01_00-00-00',
      buildDate: process.env.BUILD_DATE || '2024-01-01 00:00:00',
    },
    workspace: {
      path: process.env.WORKSPACE || '/var/lib/jenkins/workspace/nova-pasta-storybook',
      name: process.env.WORKSPACE_NAME || 'nova-pasta-storybook',
      url: process.env.WORKSPACE_URL || 'http://localhost:8080/job/nova-pasta-storybook/ws',
    },
    executor: {
      number: process.env.EXECUTOR_NUMBER || '0',
      name: process.env.EXECUTOR_NAME || 'executor-0',
      workspace: process.env.EXECUTOR_WORKSPACE || '/var/lib/jenkins/workspace/nova-pasta-storybook',
    },
    node: {
      name: process.env.NODE_NAME || 'master',
      labels: process.env.NODE_LABELS || 'master',
      host: process.env.NODE_HOST || 'localhost',
      port: process.env.NODE_PORT || '8080',
    },
    git: {
      branch: process.env.GIT_BRANCH || 'main',
      commit: process.env.GIT_COMMIT || 'abc123def456',
      previousCommit: process.env.GIT_PREVIOUS_COMMIT || 'def456abc789',
      url: process.env.GIT_URL || 'https://github.com/caspian/nova-pasta.git',
      remoteUrl: process.env.GIT_REMOTE_URL || 'https://github.com/caspian/nova-pasta.git',
      localBranch: process.env.GIT_LOCAL_BRANCH || 'main',
    },
    svn: {
      revision: process.env.SVN_REVISION || '1',
      url: process.env.SVN_URL || '',
    },
    cvs: {
      branch: process.env.CVS_BRANCH || '',
      tag: process.env.CVS_TAG || '',
    },
    environment: {
      home: process.env.HOME || '/var/lib/jenkins',
      user: process.env.USER || 'jenkins',
      shell: process.env.SHELL || '/bin/bash',
      path: process.env.PATH || '/usr/local/bin:/usr/bin:/bin',
      javaHome: process.env.JAVA_HOME || '/usr/lib/jvm/java-11-openjdk',
      mavenHome: process.env.MAVEN_HOME || '/usr/share/maven',
      gradleHome: process.env.GRADLE_HOME || '/usr/share/gradle',
      nodeHome: process.env.NODE_HOME || '/usr/local/node',
      npmHome: process.env.NPM_HOME || '/usr/local/npm',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.jenkins.com', '*.localhost'],
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
      archive: process.env.ARTIFACT_ARCHIVE === 'true',
      fingerprint: process.env.ARTIFACT_FINGERPRINT === 'true',
    },
  },
  
  // Configurações de deploy
  deploy: {
    enabled: process.env.DEPLOY_ENABLED === 'true',
    provider: process.env.DEPLOY_PROVIDER || 'jenkins',
    directory: process.env.DEPLOY_DIRECTORY || '../storybook-static',
    script: process.env.DEPLOY_SCRIPT || 'deploy.sh',
    environment: process.env.DEPLOY_ENVIRONMENT || 'production',
    variables: {
      DEPLOY_USER: process.env.DEPLOY_USER || 'jenkins',
      DEPLOY_PASSWORD: process.env.DEPLOY_PASSWORD || '',
      DEPLOY_KEY: process.env.DEPLOY_KEY || '',
      DEPLOY_HOST: process.env.DEPLOY_HOST || 'localhost',
      DEPLOY_PORT: process.env.DEPLOY_PORT || '22',
    },
  },
  
  // Configurações de cache do Jenkins
  jenkinsCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$JOB_NAME',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    maxAge: parseInt(process.env.CACHE_MAX_AGE || '86400'),
  },
  
  // Configurações de notificação
  notification: {
    enabled: process.env.NOTIFICATION_ENABLED === 'true',
    email: process.env.NOTIFICATION_EMAIL || 'caspian@example.com',
    slack: process.env.NOTIFICATION_SLACK || '',
    teams: process.env.NOTIFICATION_TEAMS || '',
    webhook: process.env.NOTIFICATION_WEBHOOK || '',
  },
}
