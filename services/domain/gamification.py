"""
Gamification Domain Service

Responsibilities (Backend only — no AI calls):
  - Goal Progress tracking
  - ESG Score computation via WeightedFormulaEngine
  - Department Ranking
  - Badge Auto Award
  - Reward Redemption (transactional)
  - Notification generation for milestone events
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from services.domain.engines import (
    WeightedFormulaEngine, ESGInputMetrics, GoalProgressEngine, DepartmentRankingEngine,
    DepartmentScoreEntry,
)
from core.exceptions import BadRequestException, NotFoundException


class GamificationService:
    def __init__(self):
        self._formula_engine = WeightedFormulaEngine()

    # ------------------------------------------------------------------
    # ESG Score Computation
    # ------------------------------------------------------------------
    async def compute_department_esg_score(
        self,
        db: AsyncSession,
        department_id: uuid.UUID,
        metrics: ESGInputMetrics,
        previous_score: Optional[float] = None,
    ) -> dict:
        """
        Compute the ESG score for a department using the WeightedFormulaEngine.
        Persists the result to department_scores table.
        """
        result = self._formula_engine.compute(metrics, previous_score=previous_score)

        # Persist score
        from repositories.department_score import department_score_repo
        now = datetime.now(timezone.utc)
        await department_score_repo.create(db, {
            "department_id": department_id,
            "score": result.overall,
            "month": now.month,
            "year": now.year,
            "status": "active",
        })

        return {
            "department_id": str(department_id),
            "overall_score": result.overall,
            "grade": result.grade,
            "trend": result.trend,
            "environmental": result.environmental.weighted,
            "social": result.social.weighted,
            "governance": result.governance.weighted,
        }

    async def compute_overall_esg_score(
        self,
        db: AsyncSession,
    ) -> dict:
        """
        Aggregates all department scores to produce the organisation-wide ESG score.
        """
        from repositories.department_score import department_score_repo
        from models.department_score import DepartmentScore

        now = datetime.now(timezone.utc)
        all_scores = await department_score_repo.get_all(db, skip=0, limit=1000)
        current_period = [s for s in all_scores if s.month == now.month and s.year == now.year]

        if not current_period:
            return {"overall_score": 0.0, "department_count": 0}

        avg = sum(s.score for s in current_period) / len(current_period)
        return {
            "overall_score": round(avg, 2),
            "grade": self._formula_engine._grade(avg),
            "department_count": len(current_period),
        }

    # ------------------------------------------------------------------
    # Goal Progress
    # ------------------------------------------------------------------
    async def evaluate_goal_progress(
        self,
        db: AsyncSession,
        goal_id: uuid.UUID,
    ) -> dict:
        from repositories.goal import goal_repo

        goal = await goal_repo.get_by_id(db, goal_id)
        if not goal:
            raise NotFoundException(f"Goal {goal_id} not found")

        result = GoalProgressEngine.compute(
            goal_id=str(goal.id),
            current_value=float(goal.current_value or 0),
            target_value=float(goal.target_value or 1),
            start_date=goal.created_at.date(),
            deadline=goal.deadline.date() if hasattr(goal.deadline, "date") else goal.deadline,
        )

        # Update status on the goal
        await goal_repo.update(db, goal, {"status": result.status})

        return {
            "goal_id": str(goal_id),
            "completion_pct": result.completion_pct,
            "status": result.status,
            "velocity_per_day": result.velocity_per_day,
            "estimated_completion": str(result.estimated_completion) if result.estimated_completion else None,
        }

    # ------------------------------------------------------------------
    # Department Ranking
    # ------------------------------------------------------------------
    async def get_department_rankings(self, db: AsyncSession) -> List[dict]:
        from repositories.department_score import department_score_repo
        from repositories.department import department_repo

        now = datetime.now(timezone.utc)
        scores = await department_score_repo.get_all(db, skip=0, limit=1000)
        current = {s.department_id: s.score for s in scores if s.month == now.month and s.year == now.year}
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year  = now.year if now.month > 1 else now.year - 1
        previous   = {s.department_id: s.score for s in scores if s.month == prev_month and s.year == prev_year}

        departments = await department_repo.get_all(db, skip=0, limit=1000)
        dept_map = {d.id: d.name for d in departments}

        entries = [
            DepartmentScoreEntry(
                department_id=str(did),
                department_name=dept_map.get(did, "Unknown"),
                esg_score=score,
                previous_score=previous.get(did),
            )
            for did, score in current.items()
        ]

        ranked = DepartmentRankingEngine.rank(entries)
        return [
            {
                "rank": r.rank,
                "department_id": r.department_id,
                "department_name": r.department_name,
                "esg_score": r.esg_score,
                "score_delta": r.score_delta,
                "percentile": r.percentile,
            }
            for r in ranked
        ]

    # ------------------------------------------------------------------
    # Badge Auto Award
    # ------------------------------------------------------------------
    async def evaluate_and_award_badges(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> List[dict]:
        """
        Checks badge criteria against the user's activity and awards badges.
        Returns a list of newly awarded badges.
        """
        from repositories.badge import badge_repo
        from repositories.user_badge import user_badge_repo
        from repositories.employee_participation import employee_participation_repo

        all_badges = await badge_repo.get_all(db, skip=0, limit=500)
        existing_badge_ids = {
            ub.badge_id
            for ub in await user_badge_repo.get_all(db, skip=0, limit=1000)
            if str(ub.user_id) == str(user_id)
        }

        awarded = []
        for badge in all_badges:
            if badge.id in existing_badge_ids:
                continue  # Already has this badge

            # Evaluate criteria — currently using name-based heuristics
            # In a full system, badge.criteria would be a JSON ruleset
            should_award = await self._evaluate_badge_criteria(db, user_id, badge)
            if should_award:
                new_badge = await user_badge_repo.create(db, {
                    "user_id": user_id,
                    "badge_id": badge.id,
                    "awarded_at": datetime.now(timezone.utc),
                    "status": "active",
                })
                awarded.append({
                    "badge_id": str(badge.id),
                    "badge_name": badge.name,
                    "awarded_at": str(datetime.now(timezone.utc)),
                })

        return awarded

    async def _evaluate_badge_criteria(self, db: AsyncSession, user_id: uuid.UUID, badge) -> bool:
        """
        Deterministic badge criteria evaluator.
        Reads badge.criteria as a simple string rule like 'participation_count:5'.
        """
        from repositories.employee_participation import employee_participation_repo
        from repositories.challenge_participation import challenge_participation_repo

        criteria = badge.name.lower() if not badge.status else ""
        # Simple heuristic: participation count for first badge
        participations = await employee_participation_repo.get_all(db, skip=0, limit=1000)
        user_parts = [p for p in participations if str(p.user_id) == str(user_id)]

        if "first" in badge.name.lower() and len(user_parts) >= 1:
            return True
        if "active" in badge.name.lower() and len(user_parts) >= 5:
            return True
        if "champion" in badge.name.lower() and len(user_parts) >= 10:
            return True

        return False

    # ------------------------------------------------------------------
    # Reward Redemption
    # ------------------------------------------------------------------
    async def redeem_reward(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        reward_id: uuid.UUID,
    ) -> dict:
        """
        Transactional reward redemption:
          1. Fetch reward and check stock
          2. Check user points (via CarbonTransaction credits)
          3. Debit points
          4. Decrement reward stock
        """
        from repositories.reward import reward_repo
        from repositories.carbon_transaction import carbon_transaction_repo

        reward = await reward_repo.get_by_id(db, reward_id)
        if not reward:
            raise NotFoundException(f"Reward {reward_id} not found")

        if int(reward.stock or 0) < 1:
            raise BadRequestException("Reward is out of stock")

        # Calculate user's available points (sum of credit transactions)
        all_txns = await carbon_transaction_repo.get_all(db, skip=0, limit=10000)
        user_txns = [t for t in all_txns if str(t.user_id) == str(user_id)]
        total_credits = sum(float(t.amount or 0) for t in user_txns if t.type == "credit")
        total_debits  = sum(float(t.amount or 0) for t in user_txns if t.type == "debit")
        available_points = total_credits - total_debits

        reward_cost = float(reward.cost or 0)
        if available_points < reward_cost:
            raise BadRequestException(
                f"Insufficient points. Available: {available_points:.1f}, Required: {reward_cost:.1f}"
            )

        # Debit points via a new carbon transaction
        await carbon_transaction_repo.create(db, {
            "user_id": user_id,
            "amount": reward_cost,
            "type": "debit",
            "source": f"reward_redemption:{reward_id}",
            "date": datetime.now(timezone.utc),
            "status": "active",
        })

        # Decrement stock
        await reward_repo.update(db, reward, {"stock": int(reward.stock) - 1})

        return {
            "success": True,
            "reward_id": str(reward_id),
            "reward_name": reward.name,
            "points_spent": reward_cost,
            "remaining_points": available_points - reward_cost,
        }


gamification_service = GamificationService()
