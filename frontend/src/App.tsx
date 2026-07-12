import React, { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { Layout } from './components/ui/Layout'
import { CardSkeleton } from './components/ui/Skeleton'
import { AIWidget } from './components/ai/AIWidget'
import { ErrorBoundary } from './components/ui/ErrorBoundary'

// Lazy-loaded pages for bundle splitting
const Auth = lazy(() => import('./pages/Auth').then(m => ({ default: m.Auth })))
const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default: m.Dashboard })))
const Environmental = lazy(() => import('./pages/Environmental').then(m => ({ default: m.Environmental })))
const Social = lazy(() => import('./pages/Social').then(m => ({ default: m.Social })))
const Governance = lazy(() => import('./pages/Governance').then(m => ({ default: m.Governance })))
const Gamification = lazy(() => import('./pages/Gamification').then(m => ({ default: m.Gamification })))
const Reports = lazy(() => import('./pages/Reports').then(m => ({ default: m.Reports })))
const Profile = lazy(() => import('./pages/Profile').then(m => ({ default: m.Profile })))
const Settings = lazy(() => import('./pages/Settings').then(m => ({ default: m.Settings })))

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 2,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30_000),
    },
    mutations: { retry: 1 },
  },
})

const PageFallback = () => (
  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
    <CardSkeleton /><CardSkeleton /><CardSkeleton />
  </div>
)

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <BrowserRouter>
            <ErrorBoundary>
              <Routes>
                <Route
                  path="/auth"
                  element={
                    <Suspense fallback={<PageFallback />}>
                      <Auth />
                    </Suspense>
                  }
                />
                <Route element={<Layout />}>
                  <Route path="/" element={<Suspense fallback={<PageFallback />}><Dashboard /></Suspense>} />
                  <Route path="/environmental" element={<Suspense fallback={<PageFallback />}><Environmental /></Suspense>} />
                  <Route path="/social" element={<Suspense fallback={<PageFallback />}><Social /></Suspense>} />
                  <Route path="/governance" element={<Suspense fallback={<PageFallback />}><Governance /></Suspense>} />
                  <Route path="/gamification" element={<Suspense fallback={<PageFallback />}><Gamification /></Suspense>} />
                  <Route path="/reports" element={<Suspense fallback={<PageFallback />}><Reports /></Suspense>} />
                  <Route path="/profile" element={<Suspense fallback={<PageFallback />}><Profile /></Suspense>} />
                  <Route path="/settings" element={<Suspense fallback={<PageFallback />}><Settings /></Suspense>} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
              </Routes>

              <AIWidget />
            </ErrorBoundary>
          </BrowserRouter>

          <Toaster
            position="bottom-right"
            toastOptions={{
              style: {
                background: 'var(--color-surface)',
                color: 'var(--color-text-primary)',
                border: '1px solid var(--color-border)',
                backdropFilter: 'blur(18px)',
                fontSize: '14px',
              },
              success: { iconTheme: { primary: '#16A34A', secondary: '#fff' } },
              error: { iconTheme: { primary: '#DC2626', secondary: '#fff' } },
            }}
          />
          <ReactQueryDevtools initialIsOpen={false} />
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
