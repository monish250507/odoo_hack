"""
Reporting & Dashboard Domain Service

Backend Responsibilities:
  - Aggregate all statistics for dashboard (deterministic)
  - Compile recent activity feed
  - Persist generated reports

AI Integration:
  - Triggers Report Agent with aggregated dashboard data to produce
    an executive ESG summary, sustainability insights, and action recommendations.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class ReportingService:

    # ------------------------------------------------------------------
    # Dashboard Aggregation (deterministic)
    # ------------------------------------------------------------------
    async def get_dashboard_data(self, db: AsyncSession) -> dict:
        """
        Aggregates all key ESG metrics for the organisation dashboard.
        No AI here — pure DB reads and math.
        """
        from repositories.carbon_transaction import carbon_transaction_repo
        from repositories.csr_activity import csr_activity_repo
        from repositories.compliance_issue import compliance_issue_repo
        from repositories.challenge import challenge_repo
        from repositories.user import user_repo
        from repositories.department_score import department_score_repo
        from services.domain.gamification import gamification_service

        now = datetime.now(timezone.utc)

        # Carbon stats
        all_txns = await carbon_transaction_repo.get_all(db, skip=0, limit=50000)
        total_emissions = sum(float(t.amount or 0) for t in all_txns if t.type == "debit")
        total_credits   = sum(float(t.amount or 0) for t in all_txns if t.type == "credit")

        # Social stats
        all_users = await user_repo.get_all(db, skip=0, limit=10000)
        all_activities = await csr_activity_repo.get_all(db, skip=0, limit=1000)
        approved_activities = [a for a in all_activities if str(a.status).lower() == "approved"]

        # Governance stats
        all_issues = await compliance_issue_repo.get_all(db, skip=0, limit=1000)
        open_issues = [i for i in all_issues if str(i.status).lower() in ("open", "pending")]

        # ESG Scores
        all_scores = await department_score_repo.get_all(db, skip=0, limit=1000)
        current_scores = [s for s in all_scores if s.month == now.month and s.year == now.year]
        avg_score = sum(s.score for s in current_scores) / max(len(current_scores), 1)

        # Challenges
        all_challenges = await challenge_repo.get_all(db, skip=0, limit=500)
        active_challenges = [c for c in all_challenges if str(c.status).lower() == "active"]

        return {
            "generated_at": now.isoformat(),
            "environmental": {
                "total_emissions_kg": round(total_emissions, 2),
                "total_credits_kg": round(total_credits, 2),
                "net_emissions_kg": round(max(total_emissions - total_credits, 0), 2),
            },
            "social": {
                "total_employees": len(all_users),
                "approved_csr_activities": len(approved_activities),
                "active_challenges": len(active_challenges),
            },
            "governance": {
                "open_compliance_issues": len(open_issues),
            },
            "esg_score": {
                "average_score": round(avg_score, 2),
                "departments_scored": len(current_scores),
            },
        }

    # ------------------------------------------------------------------
    # Recent Activity Feed
    # ------------------------------------------------------------------
    async def get_recent_activity_feed(
        self,
        db: AsyncSession,
        limit: int = 20,
    ) -> List[dict]:
        """
        Aggregates the most recent actions across all modules into
        a unified activity timeline, sorted by timestamp desc.
        """
        from repositories.carbon_transaction import carbon_transaction_repo
        from repositories.employee_participation import employee_participation_repo
        from repositories.policy_acknowledgement import policy_acknowledgement_repo
        from repositories.user_badge import user_badge_repo
        from repositories.notification import notification_repo

        feed: List[dict] = []

        # Carbon transactions
        txns = await carbon_transaction_repo.get_all(db, skip=0, limit=50)
        for t in txns:
            feed.append({
                "type": "carbon_transaction",
                "description": f"{t.type.title()} of {t.amount} kg CO₂e from {t.source}",
                "timestamp": t.created_at.isoformat() if t.created_at else "",
                "entity_id": str(t.id),
            })

        # Participations
        parts = await employee_participation_repo.get_all(db, skip=0, limit=50)
        for p in parts:
            feed.append({
                "type": "csr_participation",
                "description": f"Employee submitted {p.hours}h for CSR activity",
                "timestamp": p.created_at.isoformat() if p.created_at else "",
                "entity_id": str(p.id),
            })

        # Badge awards
        badges = await user_badge_repo.get_all(db, skip=0, limit=50)
        for b in badges:
            feed.append({
                "type": "badge_awarded",
                "description": "A badge was awarded",
                "timestamp": b.created_at.isoformat() if b.created_at else "",
                "entity_id": str(b.id),
            })

        # Sort by timestamp descending and return limit
        feed.sort(key=lambda x: x["timestamp"], reverse=True)
        return feed[:limit]

    # ------------------------------------------------------------------
    # AI-Powered: Executive ESG Report Generation
    # ------------------------------------------------------------------
    async def generate_executive_report(
        self,
        db: AsyncSession,
        report_type: str = "Quarterly",
    ) -> dict:
        """
        1. Aggregates dashboard data (deterministic)
        2. Sends context to Report Agent for narrative + insights
        3. Persists the generated report summary
        Returns structured AI report.
        """
        from ai.orchestrator import app_graph

        dashboard = await self.get_dashboard_data(db)

        initial_state = {
            "messages": [],
            "context": {
                "task_type": "narrate-report",
                "data_metrics": dashboard,
                "report_type": report_type,
            },
            "retry_count": 0,
        }

        result = await app_graph.ainvoke(initial_state)
        ai_report = result.get("structured_output", {})

        return {
            "report_type": report_type,
            "dashboard_snapshot": dashboard,
            "ai_narrative": ai_report,
            "confidence": result.get("confidence_score"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


reporting_service = ReportingService()
