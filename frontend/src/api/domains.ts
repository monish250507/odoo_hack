import apiClient from './client'

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
}

export interface ListParams {
  skip?: number
  limit?: number
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  status?: string
}

// ── Carbon Transactions ──────────────────────────────────────────
export interface CarbonTransaction {
  id: string; user_id: string; amount: number; type: 'credit' | 'debit'
  source: string; date: string; notes?: string; status: string
  created_at: string
}

export const environmentalApi = {
  getTransactions: (params?: ListParams) =>
    apiClient.get<CarbonTransaction[]>('/api/v1/carbon-transactions', { params }).then(r => r.data),
  createTransaction: (payload: Partial<CarbonTransaction>) =>
    apiClient.post<CarbonTransaction>('/api/v1/carbon-transactions', payload).then(r => r.data),
  getDomainScore: (departmentId?: string) =>
    apiClient.get('/api/v1/domain/environmental/score', { params: { department_id: departmentId } }).then(r => r.data),
  estimateCarbon: (payload: { activity_data: Record<string, number>; industry: string }) =>
    apiClient.post('/api/v1/ai/query', { task_type: 'estimate-carbon', ...payload }).then(r => r.data),
  getEmissionFactors: () =>
    apiClient.get('/api/v1/emission-factors').then(r => r.data),
}

// ── Goals ────────────────────────────────────────────────────────
export interface Goal {
  id: string; name: string; description?: string; target_value: number
  current_value: number; unit?: string; deadline?: string
  department_id?: string; status: string; created_at: string
}

export const goalsApi = {
  getAll: (params?: ListParams) =>
    apiClient.get<Goal[]>('/api/v1/goals', { params }).then(r => r.data),
  create: (payload: Partial<Goal>) =>
    apiClient.post<Goal>('/api/v1/goals', payload).then(r => r.data),
  update: (id: string, payload: Partial<Goal>) =>
    apiClient.patch<Goal>(`/api/v1/goals/${id}`, payload).then(r => r.data),
  delete: (id: string) =>
    apiClient.delete(`/api/v1/goals/${id}`).then(r => r.data),
}

// ── CSR Activities ───────────────────────────────────────────────
export interface CSRActivity {
  id: string; title: string; description?: string; date?: string
  department_id?: string; points: number; status: string; created_at: string
}

export const socialApi = {
  getActivities: (params?: ListParams) =>
    apiClient.get<CSRActivity[]>('/api/v1/csr-activities', { params }).then(r => r.data),
  createActivity: (payload: Partial<CSRActivity>) =>
    apiClient.post<CSRActivity>('/api/v1/csr-activities', payload).then(r => r.data),
  getEngagementStats: (userId: string) =>
    apiClient.get(`/api/v1/domain/social/engagement/${userId}`).then(r => r.data),
  submitParticipation: (payload: { user_id: string; activity_id: string; hours: number }) =>
    apiClient.post('/api/v1/employee-participations', payload).then(r => r.data),
  getRecommendations: (userId: string, departmentId: string) =>
    apiClient.post('/api/v1/ai/query', { task_type: 'recommend-challenge', user_id: userId, department_id: departmentId }).then(r => r.data),
}

// ── Compliance & Governance ───────────────────────────────────────
export interface ComplianceIssue {
  id: string; audit_id?: string; description?: string
  severity: 'low' | 'medium' | 'high' | 'critical'; status: string; created_at: string
}
export interface Policy {
  id: string; title: string; content?: string; version: number; status: string
}

export const governanceApi = {
  getIssues: (params?: ListParams) =>
    apiClient.get<ComplianceIssue[]>('/api/v1/compliance-issues', { params }).then(r => r.data),
  updateIssue: (id: string, payload: Partial<ComplianceIssue>) =>
    apiClient.patch<ComplianceIssue>(`/api/v1/compliance-issues/${id}`, payload).then(r => r.data),
  getPolicies: () =>
    apiClient.get<Policy[]>('/api/v1/policies').then(r => r.data),
  acknowledgePolicy: (policyId: string, userId: string) =>
    apiClient.post('/api/v1/policy-acknowledgements', { policy_id: policyId, user_id: userId }).then(r => r.data),
  getComplianceScore: () =>
    apiClient.get('/api/v1/domain/governance/score').then(r => r.data),
}

// ── Gamification ─────────────────────────────────────────────────
export interface Challenge {
  id: string; title: string; description?: string; start_date?: string
  end_date?: string; points: number; status: string
}
export interface Badge { id: string; name: string; description?: string; image_url?: string; criteria?: string }
export interface Reward { id: string; name: string; description?: string; cost: number; stock: number }

export const gamificationApi = {
  getChallenges: (params?: ListParams) =>
    apiClient.get<Challenge[]>('/api/v1/challenges', { params }).then(r => r.data),
  joinChallenge: (challengeId: string, userId: string) =>
    apiClient.post('/api/v1/challenge-participations', { challenge_id: challengeId, user_id: userId }).then(r => r.data),
  getBadges: () =>
    apiClient.get<Badge[]>('/api/v1/badges').then(r => r.data),
  getUserBadges: (userId: string) =>
    apiClient.get('/api/v1/user-badges', { params: { user_id: userId } }).then(r => r.data),
  getRewards: () =>
    apiClient.get<Reward[]>('/api/v1/rewards').then(r => r.data),
  redeemReward: (rewardId: string, userId: string) =>
    apiClient.post(`/api/v1/rewards/${rewardId}/redeem`, { user_id: userId }).then(r => r.data),
  getLeaderboard: () =>
    apiClient.get('/api/v1/domain/gamification/leaderboard').then(r => r.data),
}

// ── Reports ───────────────────────────────────────────────────────
export const reportsApi = {
  generateNarrative: (payload: { data_metrics: Record<string, number>; report_type: string }) =>
    apiClient.post('/api/v1/ai/query', { task_type: 'narrate-report', ...payload }).then(r => r.data),
  getDepartmentScores: () =>
    apiClient.get('/api/v1/department-scores').then(r => r.data),
  getDashboardAggregation: () =>
    apiClient.get('/api/v1/domain/reporting/dashboard').then(r => r.data),
}

// ── Notifications ─────────────────────────────────────────────────
export interface Notification {
  id: string; user_id: string; title: string; message?: string
  is_read: boolean; status: string; created_at: string
}

export const notificationsApi = {
  getAll: (params?: ListParams) =>
    apiClient.get<Notification[]>('/api/v1/notifications', { params }).then(r => r.data),
  markRead: (id: string) =>
    apiClient.patch<Notification>(`/api/v1/notifications/${id}`, { is_read: true }).then(r => r.data),
  markAllRead: () =>
    apiClient.post('/api/v1/notifications/mark-all-read').then(r => r.data),
}

// ── Department Scores ─────────────────────────────────────────────
export const departmentApi = {
  getDepartments: () =>
    apiClient.get('/api/v1/departments').then(r => r.data),
  getScores: () =>
    apiClient.get('/api/v1/department-scores').then(r => r.data),
}

// ── AI Hub ────────────────────────────────────────────────────────
export const aiApi = {
  query: (payload: { task_type: string; [key: string]: unknown }) =>
    apiClient.post('/api/v1/ai/query', payload).then(r => r.data),
  detectAnomaly: (payload: { historical_data: unknown[]; current_data: Record<string, number> }) =>
    apiClient.post('/api/v1/ai/query', { task_type: 'detect-anomaly', ...payload }).then(r => r.data),
}
