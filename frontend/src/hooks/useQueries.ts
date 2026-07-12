import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { environmentalApi, goalsApi, socialApi, governanceApi, gamificationApi, reportsApi, notificationsApi, departmentApi, aiApi } from '../api/domains'
import type { ListParams } from '../api/domains'
import toast from 'react-hot-toast'

// ── Query Keys ────────────────────────────────────────────────────
export const QUERY_KEYS = {
  transactions: (params?: ListParams) => ['carbon-transactions', params],
  goals: (params?: ListParams) => ['goals', params],
  activities: (params?: ListParams) => ['csr-activities', params],
  complianceIssues: (params?: ListParams) => ['compliance-issues', params],
  policies: () => ['policies'],
  challenges: (params?: ListParams) => ['challenges', params],
  badges: () => ['badges'],
  rewards: () => ['rewards'],
  leaderboard: () => ['leaderboard'],
  notifications: (params?: ListParams) => ['notifications', params],
  departments: () => ['departments'],
  dashboardAggregation: () => ['dashboard-aggregation'],
  departmentScores: () => ['department-scores'],
  engagementStats: (userId: string) => ['engagement-stats', userId],
}

// ── Environmental ─────────────────────────────────────────────────
export const useTransactions = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.transactions(params), queryFn: () => environmentalApi.getTransactions(params), staleTime: 30_000 })

export const useCreateTransaction = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: environmentalApi.createTransaction,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['carbon-transactions'] }); toast.success('Emission logged') },
    onError: () => toast.error('Failed to log emission'),
  })
}

export const useEstimateCarbon = () =>
  useMutation({ mutationFn: environmentalApi.estimateCarbon })

// ── Goals ─────────────────────────────────────────────────────────
export const useGoals = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.goals(params), queryFn: () => goalsApi.getAll(params), staleTime: 30_000 })

export const useCreateGoal = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: goalsApi.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['goals'] }); toast.success('Goal created') },
    onError: () => toast.error('Failed to create goal'),
  })
}

export const useUpdateGoal = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Parameters<typeof goalsApi.update>[1] }) =>
      goalsApi.update(id, payload),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['goals'] }); toast.success('Goal updated') },
    onError: () => toast.error('Failed to update goal'),
  })
}

// ── Social ────────────────────────────────────────────────────────
export const useActivities = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.activities(params), queryFn: () => socialApi.getActivities(params), staleTime: 30_000 })

export const useCreateActivity = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: socialApi.createActivity,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['csr-activities'] }); toast.success('Activity created') },
    onError: () => toast.error('Failed to create activity'),
  })
}

export const useEngagementStats = (userId: string) =>
  useQuery({ queryKey: QUERY_KEYS.engagementStats(userId), queryFn: () => socialApi.getEngagementStats(userId), enabled: !!userId })

export const useChallengeRecommendations = () =>
  useMutation({ mutationFn: ({ userId, departmentId }: { userId: string; departmentId: string }) => socialApi.getRecommendations(userId, departmentId) })

// ── Governance ────────────────────────────────────────────────────
export const useComplianceIssues = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.complianceIssues(params), queryFn: () => governanceApi.getIssues(params), staleTime: 30_000 })

export const useUpdateComplianceIssue = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Parameters<typeof governanceApi.updateIssue>[1] }) =>
      governanceApi.updateIssue(id, payload),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['compliance-issues'] }); toast.success('Issue updated') },
    onError: () => toast.error('Failed to update issue'),
  })
}

export const usePolicies = () =>
  useQuery({ queryKey: QUERY_KEYS.policies(), queryFn: governanceApi.getPolicies })

// ── Gamification ──────────────────────────────────────────────────
export const useChallenges = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.challenges(params), queryFn: () => gamificationApi.getChallenges(params), staleTime: 30_000 })

export const useJoinChallenge = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ challengeId, userId }: { challengeId: string; userId: string }) =>
      gamificationApi.joinChallenge(challengeId, userId),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['challenges'] }); toast.success('Joined challenge!') },
    onError: () => toast.error('Failed to join challenge'),
  })
}

export const useBadges = () =>
  useQuery({ queryKey: QUERY_KEYS.badges(), queryFn: gamificationApi.getBadges })

export const useRewards = () =>
  useQuery({ queryKey: QUERY_KEYS.rewards(), queryFn: gamificationApi.getRewards })

export const useRedeemReward = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ rewardId, userId }: { rewardId: string; userId: string }) =>
      gamificationApi.redeemReward(rewardId, userId),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['rewards'] }); toast.success('Reward redeemed!') },
    onError: () => toast.error('Failed to redeem reward'),
  })
}

export const useLeaderboard = () =>
  useQuery({ queryKey: QUERY_KEYS.leaderboard(), queryFn: gamificationApi.getLeaderboard })

// ── Reports ───────────────────────────────────────────────────────
export const useDashboardAggregation = () =>
  useQuery({ queryKey: QUERY_KEYS.dashboardAggregation(), queryFn: reportsApi.getDashboardAggregation, staleTime: 60_000 })

export const useDepartmentScores = () =>
  useQuery({ queryKey: QUERY_KEYS.departmentScores(), queryFn: reportsApi.getDepartmentScores })

export const useGenerateNarrative = () =>
  useMutation({ mutationFn: reportsApi.generateNarrative })

// ── Notifications ─────────────────────────────────────────────────
export const useNotifications = (params?: ListParams) =>
  useQuery({ queryKey: QUERY_KEYS.notifications(params), queryFn: () => notificationsApi.getAll(params), staleTime: 15_000 })

export const useMarkNotificationRead = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: notificationsApi.markRead,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notifications'] }),
  })
}

// ── Departments ───────────────────────────────────────────────────
export const useDepartments = () =>
  useQuery({ queryKey: QUERY_KEYS.departments(), queryFn: departmentApi.getDepartments })

// ── AI ────────────────────────────────────────────────────────────
export const useAIQuery = () =>
  useMutation({ mutationFn: aiApi.query })

export const useDetectAnomaly = () =>
  useMutation({ mutationFn: aiApi.detectAnomaly })
