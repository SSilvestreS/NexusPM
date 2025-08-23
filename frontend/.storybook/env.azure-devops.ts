// Configurações de ambiente para Azure DevOps
export const azureDevOpsConfig = {
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
  
  // Configurações do Azure DevOps
  azureDevOps: {
    organization: {
      name: process.env.SYSTEM_COLLECTIONURI?.split('/').pop() || 'nova-pasta',
      url: process.env.SYSTEM_COLLECTIONURI || 'https://dev.azure.com/nova-pasta',
    },
    project: {
      id: process.env.SYSTEM_TEAMPROJECTID || '12345',
      name: process.env.SYSTEM_TEAMPROJECT || 'nova-pasta',
      url: process.env.SYSTEM_TEAMPROJECTURI || 'https://dev.azure.com/nova-pasta/nova-pasta',
    },
    build: {
      id: process.env.BUILD_BUILDID || '12345',
      number: process.env.BUILD_BUILDNUMBER || '2024.1.1',
      definitionId: process.env.BUILD_DEFINITIONID || '12345',
      definitionName: process.env.BUILD_DEFINITIONNAME || 'nova-pasta-storybook',
      repository: {
        id: process.env.BUILD_REPOSITORY_ID || '12345',
        name: process.env.BUILD_REPOSITORY_NAME || 'nova-pasta',
        provider: process.env.BUILD_REPOSITORY_PROVIDER || 'GitHub',
        uri: process.env.BUILD_REPOSITORY_URI || 'https://github.com/caspian/nova-pasta',
        branch: process.env.BUILD_SOURCEBRANCHNAME || 'main',
        commit: process.env.BUILD_SOURCEVERSION || 'abc123def456',
        clean: process.env.BUILD_REPOSITORY_CLEAN === 'true',
      },
      sourceBranch: process.env.BUILD_SOURCEBRANCH || 'refs/heads/main',
      sourceVersion: process.env.BUILD_SOURCEVERSION || 'abc123def456',
      sourceVersionMessage: process.env.BUILD_SOURCEVERSIONMESSAGE || 'Update storybook',
      sourceVersionAuthor: process.env.BUILD_SOURCEVERSIONAUTHOR || 'Caspian <caspian@example.com>',
      sourceVersionDate: process.env.BUILD_SOURCEVERSIONDATE || '2024-01-01T00:00:00Z',
      requestedFor: process.env.BUILD_REQUESTEDFOR || 'Caspian <caspian@example.com>',
      requestedForId: process.env.BUILD_REQUESTEDFORID || '12345',
      reason: process.env.BUILD_REASON || 'IndividualCI',
      queueTime: process.env.BUILD_QUEUETIME || '2024-01-01T00:00:00Z',
      startTime: process.env.BUILD_STARTTIME || '2024-01-01T00:00:00Z',
      finishTime: process.env.BUILD_FINISHTIME || '2024-01-01T00:00:00Z',
      result: process.env.BUILD_RESULT || 'Succeeded',
      status: process.env.BUILD_STATUS || 'Completed',
      uri: process.env.BUILD_URI || 'vstfs:///Build/Build/12345',
      url: process.env.BUILD_URL || 'https://dev.azure.com/nova-pasta/nova-pasta/_build/results?buildId=12345',
    },
    release: {
      id: process.env.RELEASE_RELEASEID || '12345',
      name: process.env.RELEASE_RELEASENAME || 'Release-2024.1.1',
      definitionId: process.env.RELEASE_DEFINITIONID || '12345',
      definitionName: process.env.RELEASE_DEFINITIONNAME || 'nova-pasta-storybook',
      environment: process.env.RELEASE_ENVIRONMENTNAME || 'Production',
      environmentId: process.env.RELEASE_ENVIRONMENTID || '12345',
      environmentUrl: process.env.RELEASE_ENVIRONMENTURL || 'https://dev.azure.com/nova-pasta/nova-pasta/_release?releaseId=12345',
      releaseUri: process.env.RELEASE_RELEASEURI || 'vstfs:///ReleaseManagement/Release/12345',
      releaseUrl: process.env.RELEASE_RELEASEURL || 'https://dev.azure.com/nova-pasta/nova-pasta/_release?releaseId=12345',
      requestedFor: process.env.RELEASE_REQUESTEDFOR || 'Caspian <caspian@example.com>',
      requestedForId: process.env.RELEASE_REQUESTEDFORID || '12345',
      reason: process.env.RELEASE_REASON || 'Manual',
      releaseWebUrl: process.env.RELEASE_RELEASEWEBURL || 'https://dev.azure.com/nova-pasta/nova-pasta/_release?releaseId=12345',
    },
    agent: {
      id: process.env.AGENT_ID || '12345',
      name: process.env.AGENT_NAME || 'Azure Pipelines 1',
      machineName: process.env.AGENT_MACHINENAME || 'fv-az123-456',
      os: process.env.AGENT_OS || 'Linux',
      architecture: process.env.AGENT_OSARCHITECTURE || 'X64',
      version: process.env.AGENT_VERSION || '2.217.2',
      jobName: process.env.AGENT_JOBNAME || 'Job',
      jobStatus: process.env.AGENT_JOBSTATUS || 'Succeeded',
      workFolder: process.env.AGENT_WORKFOLDER || '/home/vsts/work',
      tempDirectory: process.env.AGENT_TEMPDIRECTORY || '/home/vsts/work/_temp',
      toolsDirectory: process.env.AGENT_TOOLSDIRECTORY || '/opt/hostedtoolcache',
      homeDirectory: process.env.AGENT_HOMEDIRECTORY || '/home/vsts',
      serverOMDirectory: process.env.AGENT_SERVEROMDIRECTORY || '/opt/vsts/agent/agent/serverOM',
      diagnostic: process.env.AGENT_DIAGNOSTIC === 'true',
    },
    system: {
      accessToken: process.env.SYSTEM_ACCESSTOKEN || '',
      defaultWorkingDirectory: process.env.SYSTEM_DEFAULTWORKINGDIRECTORY || '/home/vsts/work/1/s',
      debug: process.env.SYSTEM_DEBUG === 'true',
      hostType: process.env.SYSTEM_HOSTTYPE || 'build',
      jobDisplayName: process.env.SYSTEM_JOBDISPLAYNAME || 'Job',
      jobId: process.env.SYSTEM_JOBID || '12345',
      jobName: process.env.SYSTEM_JOBNAME || 'Job',
      jobParallelismTag: process.env.SYSTEM_JOBPARALLELISMTAG || 'Public',
      jobPositionInPhase: process.env.SYSTEM_JOBPOSITIONINPHASE || '1',
      jobStatus: process.env.SYSTEM_JOBSTATUS || 'Succeeded',
      phaseAttempt: process.env.SYSTEM_PHASEATTEMPT || '1',
      phaseDisplayName: process.env.SYSTEM_PHASEDISPLAYNAME || 'Phase 1',
      phaseId: process.env.SYSTEM_PHASEID || '12345',
      phaseName: process.env.SYSTEM_PHASENAME || 'Phase1',
      planId: process.env.SYSTEM_PLANID || '12345',
      pullRequestId: process.env.SYSTEM_PULLREQUEST_PULLREQUESTID || '',
      pullRequestSourceBranch: process.env.SYSTEM_PULLREQUEST_SOURCEBRANCH || '',
      pullRequestTargetBranch: process.env.SYSTEM_PULLREQUEST_TARGETBRANCH || '',
      pullRequestSourceRepositoryURI: process.env.SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI || '',
      pullRequestMergedAt: process.env.SYSTEM_PULLREQUEST_MERGEDAT || '',
      pullRequestIsFork: process.env.SYSTEM_PULLREQUEST_ISFORK === 'true',
      stageAttempt: process.env.SYSTEM_STAGEATTEMPT || '1',
      stageDisplayName: process.env.SYSTEM_STAGEDISPLAYNAME || 'Stage 1',
      stageId: process.env.SYSTEM_STAGEID || '12345',
      stageName: process.env.SYSTEM_STAGENAME || 'Stage1',
      taskDisplayName: process.env.SYSTEM_TASKDISPLAYNAME || 'Task',
      taskInstanceId: process.env.SYSTEM_TASKINSTANCEID || '12345',
      timelineId: process.env.SYSTEM_TIMELINEID || '12345',
      totalPhaseCount: process.env.SYSTEM_TOTALPHASECOUNT || '1',
      workingDirectory: process.env.SYSTEM_WORKINGDIRECTORY || '/home/vsts/work/1/s',
    },
  },
  
  // Configurações de rede
  network: {
    host: process.env.HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '6006'),
    allowedHosts: process.env.ALLOWED_HOSTS?.split(',') || ['*.azure.com', '*.dev.azure.com'],
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
      publishLocation: process.env.ARTIFACT_PUBLISH_LOCATION || 'Container',
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
      DEPLOY_USER: process.env.DEPLOY_USER || 'vsts',
      DEPLOY_KEY: process.env.DEPLOY_KEY || '',
      DEPLOY_HOST: process.env.DEPLOY_HOST || 'localhost',
      DEPLOY_PORT: process.env.DEPLOY_PORT || '22',
    },
  },
  
  // Configurações de cache do Azure DevOps
  azureDevOpsCache: {
    enabled: process.env.CACHE_ENABLED === 'true',
    key: process.env.CACHE_KEY || 'storybook-$BUILD_SOURCEBRANCHNAME',
    paths: process.env.CACHE_PATHS?.split(',') || ['node_modules', '.npm'],
    policy: process.env.CACHE_POLICY || 'pull-push',
    restoreKeys: process.env.CACHE_RESTORE_KEYS?.split(',') || ['storybook-'],
  },
}
