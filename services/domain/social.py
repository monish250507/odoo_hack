"""
Social Domain Service

Backend Responsibilities:
  - Track CSR hours and participation counts (deterministic)
  - Aggregate employee engagement metrics

AI Integration:
  - Triggers Recommendation Agent to suggest personalised challenges
    and CSR activities based on historical participation patterns.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException


class SocialService:

    # ------------------------------------------------------------------
    # CSR Participation Tracking (deterministic)
    # ------------------------------------------------------------------
    async def submit_participation(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        activity_id: uuid.UUID,
        hours: float,
    ) -> dict:
        from repositories.employee_participation import employee_participation_repo
        from repositories.csr_activity import csr_activity_repo

        activity = await csr_activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundException(f"CSR Activity {activity_id} not found")

        record = await employee_participation_repo.create(db, {
            "user_id": user_id,
            "activity_id": activity_id,
            "hours": hours,
            "status": "pending",
        })

        return {
            "participation_id": str(record.id),
            "user_id": str(user_id),
            "activity_id": str(activity_id),
            "hours": hours,
            "status": "pending",
        }

    async def get_user_engagement_stats(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> dict:
        from repositories.employee_participation import employee_participation_repo
        from repositories.challenge_participation import challenge_participation_repo

        all_participations = await employee_participation_repo.get_all(db, skip=0, limit=10000)
        user_parts = [p for p in all_participations if str(p.user_id) == str(user_id)]
        approved_parts = [p for p in user_parts if str(p.status).lower() == "approved"]
        total_hours = sum(float(p.hours or 0) for p in approved_parts)

        all_challenges = await challenge_participation_repo.get_all(db, skip=0, limit=10000)
        user_challenges = [c for c in all_challenges if str(c.user_id) == str(user_id)]
        completed_challenges = [c for c in user_challenges if str(c.status).lower() == "completed"]

        return {
            "user_id": str(user_id),
            "total_csr_hours": round(total_hours, 2),
            "activities_participated": len(user_parts),
            "activities_approved": len(approved_parts),
            "challenges_joined": len(user_challenges),
            "challenges_completed": len(completed_challenges),
        }

    async def get_department_social_metrics(
        self,
        db: AsyncSession,
        department_id: uuid.UUID,
    ) -> dict:
        from repositories.user import user_repo
        from repositories.employee_participation import employee_participation_repo

        all_users = await user_repo.get_all(db, skip=0, limit=10000)
        dept_users = [u for u in all_users if str(u.department_id) == str(department_id)]
        dept_user_ids = {str(u.id) for u in dept_users}

        if not dept_users:
            return {"department_id": str(department_id), "total_hours": 0, "participation_rate": 0}

        all_parts = await employee_participation_repo.get_all(db, skip=0, limit=50000)
        dept_parts = [p for p in all_parts if str(p.user_id) in dept_user_ids]
        participants_set = {str(p.user_id) for p in dept_parts}
        total_hours = sum(float(p.hours or 0) for p in dept_parts if str(p.status).lower() == "approved")

        return {
            "department_id": str(department_id),
            "total_employees": len(dept_users),
            "total_csr_hours": round(total_hours, 2),
            "avg_hours_per_employee": round(total_hours / len(dept_users), 2),
            "participation_rate": round(len(participants_set) / len(dept_users), 4),
        }

    # ------------------------------------------------------------------
    # AI-Powered: Personalised Recommendations
    # ------------------------------------------------------------------
    async def get_personalised_recommendations(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        department_id: uuid.UUID,
    ) -> dict:
        """
        Triggers the Recommendation Agent with the user's engagement
        history and current department goals. Returns suggested
        challenges, CSR activities, and badge targets.
        """
        from ai.orchestrator import app_graph

        user_stats = await self.get_user_engagement_stats(db, user_id)

        from repositories.goal import goal_repo
        all_goals = await goal_repo.get_all(db, skip=0, limit=100)
        if all_goals and hasattr(all_goals[0], "department_id"):
            dept_goals = [
                {"name": g.name, "target": g.target_value, "current": g.current_value, "status": g.status}
                for g in all_goals
                if str(g.department_id) == str(department_id)
            ]
        else:
            dept_goals = []

        initial_state = {
            "messages": [],
            "context": {
                "task_type": "recommend-challenge",
                "department_goals": {
                    "department_id": str(department_id),
                    "goals": dept_goals,
                },
                "past_participation_rates": {
                    "user_id": str(user_id),
                    "total_hours": user_stats["total_csr_hours"],
                    "activities_completed": user_stats["activities_approved"],
                    "challenges_completed": user_stats["challenges_completed"],
                },
            },
            "retry_count": 0,
        }

        result = await app_graph.ainvoke(initial_state)
        return {
            "user_id": str(user_id),
            "recommendations": result.get("structured_output", {}),
            "confidence": result.get("confidence_score"),
        }


social_service = SocialService()
