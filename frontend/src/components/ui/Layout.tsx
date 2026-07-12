import React, { Suspense } from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { useAuth } from '../../context/AuthContext'
import { useTheme } from '../../context/ThemeContext'
import { useNotifications, useMarkNotificationRead } from '../../hooks/useQueries'
import { CardSkeleton } from './Skeleton'
import { Sun, Moon, Monitor, Bell } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const modes: Array<{ key: typeof theme; icon: React.ReactNode }> = [
    { key: 'light', icon: <Sun className="w-4 h-4" /> },
    { key: 'dark', icon: <Moon className="w-4 h-4" /> },
    { key: 'system', icon: <Monitor className="w-4 h-4" /> },
  ]
  return (
    <div className="flex items-center gap-1 bg-black/5 dark:bg-white/5 rounded-lg p-1">
      {modes.map(m => (
        <button
          key={m.key}
          onClick={() => setTheme(m.key)}
          aria-label={`Switch to ${m.key} mode`}
          className={`relative p-2 rounded-md transition-all ${theme === m.key ? 'text-primary' : 'text-textSecondary hover:text-textPrimary'}`}
        >
          {theme === m.key && (
            <motion.div
              layoutId="theme-pill"
              className="absolute inset-0 bg-white dark:bg-white/10 rounded-md shadow-sm"
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
          <span className="relative z-10">{m.icon}</span>
        </button>
      ))}
    </div>
  )
}

function NotificationBell() {
  const [open, setOpen] = useState(false)
  const { data: notifications = [] } = useNotifications({ limit: 10 })
  const markRead = useMarkNotificationRead()
  const unread = notifications.filter((n: { is_read: boolean }) => !n.is_read)

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="relative p-2 rounded-lg text-textSecondary hover:text-textPrimary hover:bg-black/5 transition-colors"
        aria-label={`Notifications ${unread.length > 0 ? `(${unread.length} unread)` : ''}`}
      >
        <Bell className="w-5 h-5" />
        {unread.length > 0 && (
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-danger" />
        )}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-12 w-80 glass rounded-xl shadow-2xl z-50 overflow-hidden"
          >
            <div className="px-4 py-3 border-b border-border flex items-center justify-between">
              <span className="text-sm font-semibold text-textPrimary">Notifications</span>
              {unread.length > 0 && (
                <button className="text-xs text-primary hover:underline">Mark all read</button>
              )}
            </div>
            <div className="max-h-72 overflow-y-auto divide-y divide-border">
              {notifications.length === 0 ? (
                <p className="text-sm text-textSecondary text-center py-8">No notifications</p>
              ) : (
                notifications.slice(0, 8).map((n: { id: string; is_read: boolean; title: string; message?: string; created_at: string }) => (
                  <div
                    key={n.id}
                    onClick={() => markRead.mutate(n.id)}
                    className={`px-4 py-3 cursor-pointer hover:bg-black/5 transition-colors ${!n.is_read ? 'bg-primary/5' : ''}`}
                  >
                    <p className={`text-sm ${!n.is_read ? 'font-medium text-textPrimary' : 'text-textSecondary'}`}>{n.title}</p>
                    {n.message && <p className="text-xs text-textSecondary mt-0.5 line-clamp-1">{n.message}</p>}
                    <p className="text-xs text-muted mt-1">{new Date(n.created_at).toLocaleDateString()}</p>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export const Layout = () => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="premium-bg" />
        <div className="w-8 h-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
      </div>
    )
  }

  if (!isAuthenticated) return <Navigate to="/auth" replace />

  return (
    <div className="flex min-h-screen bg-transparent relative">
      <div className="premium-bg" />
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header */}
        <header className="h-14 glass border-b border-border px-6 flex items-center justify-between sticky top-0 z-30">
          <div className="flex-1" />
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <NotificationBell />
          </div>
        </header>

        <main className="flex-1 p-8 overflow-y-auto">
          <Suspense fallback={
            <div className="grid grid-cols-3 gap-6">
              <CardSkeleton /><CardSkeleton /><CardSkeleton />
            </div>
          }>
            <Outlet />
          </Suspense>
        </main>
      </div>
    </div>
  )
}
