import React, { useState } from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/Table'
import { Badge } from '../components/ui/Badge'
import { Drawer } from '../components/ui/Drawer'
import { TableSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/EmptyState'
import { ErrorBoundary } from '../components/ui/ErrorBoundary'
import { useActivities, useCreateActivity } from '../hooks/useQueries'
import { exportToCSV } from '../lib/exports'
import { Plus, Search, Download, Activity } from 'lucide-react'

export const Social = () => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [form, setForm] = useState({ title: '', description: '', participants_expected: '', date: '' })

  const { data: activities = [], isLoading } = useActivities({ search: search || undefined })
  const createActivity = useCreateActivity()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.title) return
    await createActivity.mutateAsync({ title: form.title, description: form.description, date: form.date || undefined })
    setIsDrawerOpen(false)
    setForm({ title: '', description: '', participants_expected: '', date: '' })
  }

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Social Impact</h1>
          <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>Track CSR activities, volunteering hours, and employee engagement</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => exportToCSV(activities as unknown as Record<string, unknown>[], 'csr-activities')}>
            <Download className="w-4 h-4 mr-1" /> Export
          </Button>
          <Button variant="primary" onClick={() => setIsDrawerOpen(true)} aria-label="Create new CSR activity">
            <Plus className="w-4 h-4" /> New Activity
          </Button>
        </div>
      </header>

      <ErrorBoundary>
        <GlassCard className="p-0 overflow-hidden">
          <div className="p-4 border-b" style={{ borderColor: 'var(--color-border)' }}>
            <div className="w-64">
              <Input
                icon={<Search className="w-4 h-4" />}
                placeholder="Search activities..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                aria-label="Search CSR activities"
              />
            </div>
          </div>
          {isLoading ? (
            <TableSkeleton rows={5} />
          ) : activities.length === 0 ? (
            <EmptyState
              icon={<Activity className="w-8 h-8" />}
              title="No CSR activities"
              description="Create your first CSR activity to track employee engagement."
              action={{ label: 'Create Activity', onClick: () => setIsDrawerOpen(true) }}
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Activity</TableHead>
                  <TableHead>Points</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {activities.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell className="font-medium">{row.title}</TableCell>
                    <TableCell>{row.points}</TableCell>
                    <TableCell>{row.date ? new Date(row.date).toLocaleDateString() : '-'}</TableCell>
                    <TableCell>
                      <Badge variant={row.status === 'completed' ? 'success' : row.status === 'active' ? 'default' : 'outline'}>
                        {row.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </GlassCard>
      </ErrorBoundary>

      <Drawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} title="Create CSR Activity">
        <form className="space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Activity Title</label>
            <Input placeholder="e.g., Tree Planting Drive" value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} required />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Description</label>
            <Input placeholder="Brief description..." value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Scheduled Date</label>
            <Input type="date" value={form.date} onChange={e => setForm(f => ({ ...f, date: e.target.value }))} />
          </div>
          <div className="pt-8">
            <Button variant="primary" className="w-full" type="submit" disabled={createActivity.isPending}>
              {createActivity.isPending ? 'Creating...' : 'Create Activity'}
            </Button>
          </div>
        </form>
      </Drawer>
    </PageTransition>
  )
}
