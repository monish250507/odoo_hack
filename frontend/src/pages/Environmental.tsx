import React, { useState } from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/Table'
import { Badge } from '../components/ui/Badge'
import { Modal } from '../components/ui/Modal'
import { TableSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/EmptyState'
import { ErrorBoundary } from '../components/ui/ErrorBoundary'
import { useTransactions, useCreateTransaction } from '../hooks/useQueries'
import { exportToCSV, exportToExcel, exportToPDF } from '../lib/exports'
import { Plus, Search, Download, Leaf } from 'lucide-react'

export const Environmental = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [form, setForm] = useState({ source: '', amount: '', type: 'debit', notes: '' })

  const { data: transactions = [], isLoading } = useTransactions({
    search: search || undefined,
    status: status || undefined,
    limit: 50,
  })
  const createTx = useCreateTransaction()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.source || !form.amount) return
    await createTx.mutateAsync({ source: form.source, amount: parseFloat(form.amount), type: form.type as 'credit' | 'debit', notes: form.notes })
    setIsModalOpen(false)
    setForm({ source: '', amount: '', type: 'debit', notes: '' })
  }

  const exportData = transactions.map(t => ({ Source: t.source, Amount: t.amount, Type: t.type, Date: t.date, Status: t.status }))

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Environmental</h1>
          <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>Manage carbon emissions, energy usage, and footprint data</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => exportToCSV(exportData, 'emissions')}>
            <Download className="w-4 h-4 mr-1" /> CSV
          </Button>
          <Button variant="outline" size="sm" onClick={() => exportToExcel(exportData, 'emissions')}>
            <Download className="w-4 h-4 mr-1" /> Excel
          </Button>
          <Button variant="outline" size="sm" onClick={() => exportToPDF('Emissions Report', exportData, 'emissions')}>
            <Download className="w-4 h-4 mr-1" /> PDF
          </Button>
          <Button variant="primary" onClick={() => setIsModalOpen(true)} aria-label="Log new emission">
            <Plus className="w-4 h-4" /> Log Emission
          </Button>
        </div>
      </header>

      <ErrorBoundary>
        <GlassCard className="p-0 overflow-hidden">
          <div className="p-4 border-b flex flex-wrap gap-3 items-center justify-between" style={{ borderColor: 'var(--color-border)' }}>
            <div className="w-64">
              <Input
                icon={<Search className="w-4 h-4" />}
                placeholder="Search emissions..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                aria-label="Search emission logs"
              />
            </div>
            <Select value={status} onChange={e => setStatus(e.target.value)} className="w-36" aria-label="Filter by status">
              <option value="">All statuses</option>
              <option value="verified">Verified</option>
              <option value="pending">Pending</option>
            </Select>
          </div>

          {isLoading ? (
            <TableSkeleton rows={6} />
          ) : transactions.length === 0 ? (
            <EmptyState
              icon={<Leaf className="w-8 h-8" />}
              title="No emissions logged"
              description="Start by logging your first carbon emission entry."
              action={{ label: 'Log Emission', onClick: () => setIsModalOpen(true) }}
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Source</TableHead>
                  <TableHead>Amount (units)</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell className="font-medium">{row.source}</TableCell>
                    <TableCell>{row.amount}</TableCell>
                    <TableCell>
                      <Badge variant={row.type === 'credit' ? 'success' : 'default'}>{row.type}</Badge>
                    </TableCell>
                    <TableCell>{row.date ? new Date(row.date).toLocaleDateString() : '-'}</TableCell>
                    <TableCell>
                      <Badge variant={row.status === 'verified' ? 'success' : 'warning'}>{row.status}</Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </GlassCard>
      </ErrorBoundary>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Log Carbon Emission">
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Emission Source</label>
            <Input
              placeholder="e.g., Electricity, Fleet"
              value={form.source}
              onChange={e => setForm(f => ({ ...f, source: e.target.value }))}
              required
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Amount</label>
            <Input
              type="number"
              placeholder="0.00"
              value={form.amount}
              onChange={e => setForm(f => ({ ...f, amount: e.target.value }))}
              required
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Type</label>
            <Select value={form.type} onChange={e => setForm(f => ({ ...f, type: e.target.value }))}>
              <option value="debit">Debit (Emission)</option>
              <option value="credit">Credit (Offset)</option>
            </Select>
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>Notes (optional)</label>
            <Input
              placeholder="Additional context..."
              value={form.notes}
              onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button variant="ghost" type="button" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button variant="primary" type="submit" disabled={createTx.isPending}>
              {createTx.isPending ? 'Saving...' : 'Submit Log'}
            </Button>
          </div>
        </form>
      </Modal>
    </PageTransition>
  )
}
