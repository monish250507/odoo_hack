import React from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { CardSkeleton } from '../components/ui/Skeleton'
import { useAuth } from '../context/AuthContext'
import { User, LogOut, Award } from 'lucide-react'
import { useBadges } from '../hooks/useQueries'

export const Profile = () => {
  const { user, logout, isLoading } = useAuth()
  const { data: badges = [] } = useBadges()

  if (isLoading) return (
    <PageTransition className="max-w-2xl mx-auto space-y-6">
      <CardSkeleton /><CardSkeleton />
    </PageTransition>
  )

  return (
    <PageTransition className="max-w-2xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Profile</h1>
        <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>Manage your personal information and preferences</p>
      </header>

      <GlassCard>
        <div className="flex items-center gap-6 mb-8">
          <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center border-2 border-primary/20 flex-shrink-0">
            <User className="w-10 h-10 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-semibold" style={{ color: 'var(--color-text-primary)' }}>{user?.full_name ?? 'Anonymous'}</h2>
            <p className="text-sm capitalize mt-0.5" style={{ color: 'var(--color-text-secondary)' }}>{user?.role}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <Award className="w-3.5 h-3.5 text-warning" />
              <span className="text-xs font-medium text-warning">{user?.points ?? 0} pts</span>
            </div>
          </div>
        </div>

        <form className="space-y-5" onSubmit={e => e.preventDefault()}>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Full Name</label>
            <Input defaultValue={user?.full_name ?? ''} aria-label="Full name" />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Email Address</label>
            <Input type="email" defaultValue={user?.email ?? ''} disabled aria-label="Email address" />
          </div>
          <div className="flex items-center justify-between pt-4">
            <Button variant="primary" type="submit">Save Changes</Button>
            <Button
              variant="ghost"
              onClick={logout}
              className="text-danger hover:text-danger hover:bg-danger/10"
              aria-label="Sign out"
            >
              <LogOut className="w-4 h-4 mr-2" /> Sign Out
            </Button>
          </div>
        </form>
      </GlassCard>

      {(badges as Array<{ id: string; name: string; description?: string }>).length > 0 && (
        <GlassCard>
          <h2 className="font-semibold mb-4" style={{ color: 'var(--color-text-primary)' }}>Earned Badges</h2>
          <div className="flex flex-wrap gap-3">
            {(badges as Array<{ id: string; name: string; description?: string }>).map(badge => (
              <div
                key={badge.id}
                title={badge.description}
                className="px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-xs font-medium"
                style={{ color: 'var(--color-primary)' }}
              >
                <Award className="w-3 h-3 inline mr-1" />
                {badge.name}
              </div>
            ))}
          </div>
        </GlassCard>
      )}
    </PageTransition>
  )
}
