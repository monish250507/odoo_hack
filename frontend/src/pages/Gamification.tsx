import React from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { CardSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/EmptyState'
import { ErrorBoundary } from '../components/ui/ErrorBoundary'
import { useChallenges, useJoinChallenge, useLeaderboard, useRewards, useRedeemReward } from '../hooks/useQueries'
import { useAuth } from '../context/AuthContext'
import { Award, Star, Trophy, Gift } from 'lucide-react'

export const Gamification = () => {
  const { user } = useAuth()
  const { data: challenges = [], isLoading: challengesLoading } = useChallenges({ status: 'active' })
  const { data: leaderboard = [], isLoading: leaderboardLoading } = useLeaderboard()
  const { data: rewards = [], isLoading: rewardsLoading } = useRewards()
  const joinChallenge = useJoinChallenge()
  const redeemReward = useRedeemReward()

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight" style={{ color: 'var(--color-text-primary)' }}>Gamification</h1>
        <p className="mt-1 text-sm" style={{ color: 'var(--color-text-secondary)' }}>Challenges, leaderboards, and rewards for ESG engagement</p>
      </header>

      {/* Challenges */}
      <section aria-label="Active Challenges">
        <h2 className="text-lg font-semibold mb-4" style={{ color: 'var(--color-text-primary)' }}>Active Challenges</h2>
        {challengesLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <CardSkeleton /><CardSkeleton /><CardSkeleton />
          </div>
        ) : challenges.length === 0 ? (
          <EmptyState icon={<Award className="w-8 h-8" />} title="No active challenges" description="Check back later for new sustainability challenges." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {challenges.map(challenge => (
              <ErrorBoundary key={challenge.id}>
                <GlassCard>
                  <div className="w-10 h-10 rounded-xl bg-warning/10 flex items-center justify-center mb-3">
                    <Award className="w-5 h-5 text-warning" />
                  </div>
                  <h3 className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>{challenge.title}</h3>
                  {challenge.description && (
                    <p className="text-sm mt-2 line-clamp-2" style={{ color: 'var(--color-text-secondary)' }}>{challenge.description}</p>
                  )}
                  <div className="flex items-center justify-between mt-4">
                    <div className="flex items-center gap-1.5">
                      <Star className="w-4 h-4 text-warning" />
                      <span className="text-sm font-semibold" style={{ color: 'var(--color-text-primary)' }}>{challenge.points} pts</span>
                    </div>
                    <Badge variant={challenge.status === 'active' ? 'success' : 'outline'}>{challenge.status}</Badge>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    className="w-full mt-4"
                    disabled={joinChallenge.isPending}
                    onClick={() => user && joinChallenge.mutate({ challengeId: challenge.id, userId: user.id })}
                    aria-label={`Join ${challenge.title}`}
                  >
                    Join Challenge
                  </Button>
                </GlassCard>
              </ErrorBoundary>
            ))}
          </div>
        )}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Leaderboard */}
        <section aria-label="Leaderboard">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2" style={{ color: 'var(--color-text-primary)' }}>
            <Trophy className="w-5 h-5 text-warning" /> Leaderboard
          </h2>
          <GlassCard className="p-0 overflow-hidden">
            {leaderboardLoading ? (
              <div className="p-4 space-y-3">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded-full bg-black/5 animate-pulse" />
                    <div className="flex-1 h-4 rounded bg-black/5 animate-pulse" />
                    <div className="w-16 h-4 rounded bg-black/5 animate-pulse" />
                  </div>
                ))}
              </div>
            ) : (leaderboard as Array<{ user_id: string; full_name: string; points: number }>).length === 0 ? (
              <EmptyState icon={<Trophy className="w-8 h-8" />} title="No leaderboard data" description="Participate in challenges to appear here." />
            ) : (
              <div className="divide-y" style={{ borderColor: 'var(--color-border)' }}>
                {(leaderboard as Array<{ user_id: string; full_name: string; points: number }>).slice(0, 10).map((entry, index) => (
                  <div key={entry.user_id} className="flex items-center gap-4 px-4 py-3 hover:bg-black/5 transition-colors">
                    <span className={`text-sm font-bold w-6 text-center ${index === 0 ? 'text-warning' : index === 1 ? 'text-textSecondary' : 'text-muted'}`}>
                      #{index + 1}
                    </span>
                    <div className="flex-1">
                      <p className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>{entry.full_name}</p>
                    </div>
                    <span className="text-sm font-semibold" style={{ color: 'var(--color-primary)' }}>{entry.points} pts</span>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>
        </section>

        {/* Rewards */}
        <section aria-label="Rewards">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2" style={{ color: 'var(--color-text-primary)' }}>
            <Gift className="w-5 h-5 text-accent" /> Rewards
          </h2>
          {rewardsLoading ? (
            <div className="space-y-4"><CardSkeleton /><CardSkeleton /></div>
          ) : (rewards as Array<{ id: string; name: string; description?: string; cost: number; stock: number }>).length === 0 ? (
            <EmptyState icon={<Gift className="w-8 h-8" />} title="No rewards available" description="Rewards will be added by your admin." />
          ) : (
            <div className="space-y-3">
              {(rewards as Array<{ id: string; name: string; description?: string; cost: number; stock: number }>).map(reward => (
                <GlassCard key={reward.id} className="flex items-center justify-between py-3 px-4">
                  <div>
                    <p className="font-medium text-sm" style={{ color: 'var(--color-text-primary)' }}>{reward.name}</p>
                    {reward.description && <p className="text-xs mt-0.5" style={{ color: 'var(--color-text-secondary)' }}>{reward.description}</p>}
                    <p className="text-xs mt-1 font-semibold" style={{ color: 'var(--color-primary)' }}>{reward.cost} pts · {reward.stock} left</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={redeemReward.isPending || reward.stock === 0}
                    onClick={() => user && redeemReward.mutate({ rewardId: reward.id, userId: user.id })}
                    aria-label={`Redeem ${reward.name}`}
                  >
                    Redeem
                  </Button>
                </GlassCard>
              ))}
            </div>
          )}
        </section>
      </div>
    </PageTransition>
  )
}
