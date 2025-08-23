import React, { Suspense, lazy } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'
import { useTheme } from './hooks/useTheme'

// Componentes de layout
import Layout from './components/Layout/Layout'
import LoadingSpinner from './components/UI/LoadingSpinner'
import ErrorBoundary from './components/UI/ErrorBoundary'

// Componentes de autenticação
import LoginPage from './pages/Auth/LoginPage'
import RegisterPage from './pages/Auth/RegisterPage'
import ForgotPasswordPage from './pages/Auth/ForgotPasswordPage'
import ResetPasswordPage from './pages/Auth/ResetPasswordPage'

// Componentes principais (lazy loading para melhor performance)
const DashboardPage = lazy(() => import('./pages/Dashboard/DashboardPage'))
const ProjectsPage = lazy(() => import('./pages/Projects/ProjectsPage'))
const ProjectDetailPage = lazy(() => import('./pages/Projects/ProjectDetailPage'))
const TasksPage = lazy(() => import('./pages/Tasks/TasksPage'))
const TaskDetailPage = lazy(() => import('./pages/Tasks/TaskDetailPage'))
const ProfilePage = lazy(() => import('./pages/Profile/ProfilePage'))
const SettingsPage = lazy(() => import('./pages/Settings/SettingsPage'))

// Componente de fallback para loading
const PageLoader: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen">
    <LoadingSpinner size="large" />
  </div>
)

// Componente de rota protegida
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  
  if (isLoading) {
    return <PageLoader />
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

// Componente de rota pública (apenas para usuários não autenticados)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  
  if (isLoading) {
    return <PageLoader />
  }
  
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }
  
  return <>{children}</>
}

const App: React.FC = () => {
  const { theme } = useTheme()
  
  // Aplica o tema ao body
  React.useEffect(() => {
    document.body.setAttribute('data-theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])
  
  return (
    <ErrorBoundary>
      <div className={`app ${theme}`}>
        <Routes>
          {/* Rotas públicas de autenticação */}
          <Route path="/login" element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          } />
          
          <Route path="/register" element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          } />
          
          <Route path="/forgot-password" element={
            <PublicRoute>
              <ForgotPasswordPage />
            </PublicRoute>
          } />
          
          <Route path="/reset-password" element={
            <PublicRoute>
              <ResetPasswordPage />
            </PublicRoute>
          } />
          
          {/* Rotas protegidas com layout */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            {/* Redireciona para dashboard por padrão */}
            <Route index element={<Navigate to="/dashboard" replace />} />
            
            {/* Dashboard */}
            <Route path="dashboard" element={
              <Suspense fallback={<PageLoader />}>
                <DashboardPage />
              </Suspense>
            } />
            
            {/* Projetos */}
            <Route path="projects" element={
              <Suspense fallback={<PageLoader />}>
                <ProjectsPage />
              </Suspense>
            } />
            
            <Route path="projects/:projectId" element={
              <Suspense fallback={<PageLoader />}>
                <ProjectDetailPage />
              </Suspense>
            } />
            
            {/* Tarefas */}
            <Route path="tasks" element={
              <Suspense fallback={<PageLoader />}>
                <TasksPage />
              </Suspense>
            } />
            
            <Route path="tasks/:taskId" element={
              <Suspense fallback={<PageLoader />}>
                <TaskDetailPage />
              </Suspense>
            } />
            
            {/* Perfil e configurações */}
            <Route path="profile" element={
              <Suspense fallback={<PageLoader />}>
                <ProfilePage />
              </Suspense>
            } />
            
            <Route path="settings" element={
              <Suspense fallback={<PageLoader />}>
                <SettingsPage />
              </Suspense>
            } />
          </Route>
          
          {/* Rota de fallback para páginas não encontradas */}
          <Route path="*" element={
            <div className="flex items-center justify-center min-h-screen">
              <div className="text-center">
                <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  404 - Página não encontrada
                </h1>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  A página que você está procurando não existe.
                </p>
                <button
                  onClick={() => window.history.back()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Voltar
                </button>
              </div>
            </div>
          } />
        </Routes>
      </div>
    </ErrorBoundary>
  )
}

export default App
