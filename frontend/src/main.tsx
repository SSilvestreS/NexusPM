import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { HelmetProvider } from 'react-helmet-async'
import { Toaster } from 'react-hot-toast'

import App from './App.tsx'
import { store } from './store'
import { ThemeProvider } from './contexts/ThemeContext'
import { AuthProvider } from './contexts/AuthContext'
import { SocketProvider } from './contexts/SocketContext'

import './index.css'

// Cria o cliente do React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
    mutations: {
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* Provedor do Redux Store */}
    <Provider store={store}>
      {/* Provedor do React Query */}
      <QueryClientProvider client={queryClient}>
        {/* Provedor do React Router */}
        <BrowserRouter>
          {/* Provedor do React Helmet para SEO */}
          <HelmetProvider>
            {/* Provedor do tema (claro/escuro) */}
            <ThemeProvider>
              {/* Provedor de autenticação */}
              <AuthProvider>
                {/* Provedor de WebSocket */}
                <SocketProvider>
                  {/* Aplicação principal */}
                  <App />
                  
                  {/* Componente de notificações toast */}
                  <Toaster
                    position="top-right"
                    toastOptions={{
                      duration: 4000,
                      style: {
                        background: 'var(--toast-bg)',
                        color: 'var(--toast-color)',
                        border: '1px solid var(--toast-border)',
                      },
                    }}
                  />
                </SocketProvider>
              </AuthProvider>
            </ThemeProvider>
          </HelmetProvider>
        </BrowserRouter>
      </QueryClientProvider>
    </Provider>
  </React.StrictMode>,
)
