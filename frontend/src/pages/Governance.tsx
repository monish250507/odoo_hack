import React from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/Table'
import { Badge } from '../components/ui/Badge'
import { TableSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/EmptyState'
import { ErrorBoundary } from '../components/ui/ErrorBoundary'
import { useComplianceIssues, useUpdateComplianceIssue, usePolicies } from '../hooks/useQueries'
import { exportToCSV } from '../lib/exports'
import { ShieldCheck, Download } from 'lucide-react'

const SEVERITY_VARIANT: Record<string, 'danger' | 'warning' | 'default' | 'outline'> = {
  critical: 'danger',
  high: 'danger',
  medium: 'warning',
  low: 'outline',
}

export const Governance = () => {
  const { data: issues = [], isLoading: issuesLoading } = useComplianceIssues({ limit: 50 })
  const { data: policies = [], isLoading: policiesLoading } = usePolicies()
  const updateIssue = useUpdateComplianceIssue()

  const handleResolve = (id: string) => {
    updateIssue.mutate({ id, payload: { status: 'resolved' } })
  }

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Governance & Compliance</h1>
          <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>Audit logs, compliance issues, and policy acknowledgements</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => exportToCSV(issues as unknown as Record<string, unknown>[], 'compliance-issues')}>
            <Download className="w-4 h-4 mr-1" /> Export
          </Button>
          <Button variant="outline">
            <ShieldCheck className="w-4 h-4 mr-2" /> Run Check
          </Button>
        </div>
      </header>

      <ErrorBoundary>
        <GlassCard className="p-0 overflow-hidden">
          <div className="p-4 border-b" style={{ borderColor: 'var(--color-border)' }}>
            <h2 className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>Compliance Issues</h2>
          </div>
          {issuesLoading ? <TableSkeleton rows={4} /> : issues.length === 0 ? (
            <EmptyState icon={<ShieldCheck className="w-8 h-8" />} title="No compliance issues" description="All policies are up to date." />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Issue</TableHead>
                  <TableHead>Severity</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {issues.map((issue) => (
                  <TableRow key={issue.id}>
                    <TableCell className="max-w-xs truncate font-medium">{issue.description ?? 'No description'}</TableCell>
                    <TableCell><Badge variant={SEVERITY_VARIANT[issue.severity] ?? 'outline'}>{issue.severity}</Badge></TableCell>
                    <TableCell><Badge variant={issue.status === 'resolved' ? 'success' : 'outline'}>{issue.status}</Badge></TableCell>
                    <TableCell>{new Date(issue.created_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      {issue.status !== 'resolved' && (
                        <Button variant="ghost" size="sm" onClick={() => handleResolve(issue.id)}>
                          Resolve
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </GlassCard>
      </ErrorBoundary>

      <ErrorBoundary>
        <GlassCard className="p-0 overflow-hidden">
          <div className="p-4 border-b" style={{ borderColor: 'var(--color-border)' }}>
            <h2 className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>Active Policies</h2>
          </div>
          {policiesLoading ? <TableSkeleton rows={3} /> : policies.length === 0 ? (
            <EmptyState icon={<ShieldCheck className="w-8 h-8" />} title="No policies configured" description="Add policies for employees to acknowledge." />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Policy Title</TableHead>
                  <TableHead>Version</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {policies.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell className="font-medium">{p.title}</TableCell>
                    <TableCell>v{p.version}</TableCell>
                    <TableCell><Badge variant={p.status === 'active' ? 'success' : 'outline'}>{p.status}</Badge></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </GlassCard>
      </ErrorBoundary>
    </PageTransition>
  )
}
