import React from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { AreaChart } from '../components/charts/AreaChart'
import { BarChart } from '../components/charts/BarChart'
import { Badge } from '../components/ui/Badge'
import { CardSkeleton, ChartSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/EmptyState'
import { useDashboardAggregation, useDepartmentScores } from '../hooks/useQueries'
import { exportToCSV } from '../lib/exports'
import { Leaf, Activity, ShieldCheck, Zap, Download, TrendingUp } from 'lucide-react'

// Fallback mock data when backend is offline
const MOCK_TREND = [
  { name: 'Jan', emissions: 4200, offset: 2400 },
  { name: 'Feb', emissions: 3800, offset: 2800 },
  { name: 'Mar', emissions: 3100, offset: 3100 },
  { name: 'Apr', emissions: 2780, offset: 3500 },
  { name: 'May', emissions: 2400, offset: 3800 },
  { name: 'Jun', emissions: 2100, offset: 4100 },
]

const MOCK_DEPT = [
  { name: 'Engineering', score: 82 },
  { name: 'Marketing', score: 71 },
  { name: 'Operations', score: 90 },
  { name: 'HR', score: 88 },
]

export const Dashboard = () => {
  const { data: dashData, isLoading: dashLoading } = useDashboardAggregation()
  const { data: deptScores, isLoading: deptLoading } = useDepartmentScores()

  const trendData = dashData?.trend_data ?? MOCK_TREND
  const deptData = (deptScores ?? MOCK_DEPT) as Array<{ name: string; score: number }>

  const stats = [
    {
      label: 'Total ESG Score',
      value: dashData?.esg_score?.average_score ?? '84.2',
      change: '+2.4%',
      variant: 'success' as const,
      icon: <Zap className="w-4 h-4 text-primary" />,
      bg: 'bg-primary/10',
    },
    {
      label: 'Carbon Emissions',
      value: dashData?.total_emissions ? `${(dashData.total_emissions / 1000).toFixed(1)}k tCO2e` : '1.2k tCO2e',
      change: '+5.1%',
      variant: 'danger' as const,
      icon: <Leaf className="w-4 h-4 text-danger" />,
      bg: 'bg-danger/10',
    },
    {
      label: 'CSR Hours',
      value: dashData?.total_csr_hours ? `${dashData.total_csr_hours} hrs` : '450 hrs',
      change: '+12.4%',
      variant: 'success' as const,
      icon: <Activity className="w-4 h-4 text-accent" />,
      bg: 'bg-accent/10',
    },
    {
      label: 'Compliance Rate',
      value: dashData?.compliance_rate ? `${dashData.compliance_rate}%` : '98.5%',
      change: '+0.2%',
      variant: 'success' as const,
      icon: <ShieldCheck className="w-4 h-4 text-success" />,
      bg: 'bg-success/10',
    },
  ]

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Overview</h1>
          <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>
            High-level summary of your ESG performance
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => exportToCSV(trendData, 'esg-trend')}
            aria-label="Export data to CSV"
          >
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
          <Button variant="primary" size="sm">
            Generate AI Insights
          </Button>
        </div>
      </header>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-5">
        {dashLoading
          ? Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)
          : stats.map((stat) => (
              <GlassCard key={stat.label} className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium" style={{ color: 'var(--color-text-secondary)' }}>{stat.label}</span>
                  <div className={`w-8 h-8 rounded-full ${stat.bg} flex items-center justify-center`}>{stat.icon}</div>
                </div>
                <span className="text-2xl font-bold" style={{ color: 'var(--color-text-primary)' }}>{stat.value}</span>
                <div className="flex items-center gap-2">
                  <Badge variant={stat.variant}>{stat.change}</Badge>
                  <span className="text-xs" style={{ color: 'var(--color-muted)' }}>vs last month</span>
                </div>
              </GlassCard>
            ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold" style={{ color: 'var(--color-text-primary)' }}>Emissions Trend</h2>
            <TrendingUp className="w-4 h-4" style={{ color: 'var(--color-text-secondary)' }} />
          </div>
          {dashLoading ? <ChartSkeleton /> : trendData.length === 0 ? (
            <EmptyState icon={<Leaf />} title="No emissions data" description="Log your first emission entry to see the trend." />
          ) : (
            <AreaChart
              data={trendData}
              xAxisKey="name"
              series={[
                { key: 'emissions', color: '#0F766E', name: 'Gross Emissions' },
                { key: 'offset', color: '#2563EB', name: 'Offset' },
              ]}
            />
          )}
        </GlassCard>

        <GlassCard>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold" style={{ color: 'var(--color-text-primary)' }}>Department ESG Scores</h2>
          </div>
          {deptLoading ? <ChartSkeleton /> : deptData.length === 0 ? (
            <EmptyState icon={<Activity />} title="No department scores" description="Add departments to see score breakdowns." />
          ) : (
            <BarChart
              data={deptData}
              xAxisKey="name"
              series={[{ key: 'score', color: '#0F766E', name: 'ESG Score' }]}
            />
          )}
        </GlassCard>
      </div>
    </PageTransition>
  )
}
