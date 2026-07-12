"""
Governance Domain Service

Backend Responsibilities:
  - Compliance monitoring (threshold checks, issue counting)
  - Approval workflows (CSR Activity, Policy Ack)
  - Policy acknowledgement tracking

AI Integration:
  - When compliance score drops below threshold, triggers Anomaly Agent
    to explain the deviation and generate alert summaries.
  - Agents NEVER write to DB. This service persists results.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import BadRequestException, NotFoundException


# Compliance threshold below which AI anomaly analysis is triggered
COMPLIANCE_ALERT_THRESHOLD = 70.0


class GovernanceService:

    # ------------------------------------------------------------------
    # Compliance Monitoring
    # ------------------------------------------------------------------
    async def monitor_compliance(
        self,
        db: AsyncSession,
        department_id: uuid.UUID,
    ) -> dict:
        """
        Computes compliance score from audit data and open issues.
        If score < threshold, triggers AI Anomaly Agent for explanation.
        Persists the alert notification if anomaly is detected.
        """
        from repositories.audit import audit_repo
        from repositories.compliance_issue import compliance_issue_repo
        from services.domain.notification import NotificationService

        all_audits = await audit_repo.get_all(db, skip=0, limit=1000)
        dept_audits = [a for a in all_audits if str(a.department_id) == str(department_id)]

        all_issues = await compliance_issue_repo.get_all(db, skip=0, limit=1000)
        audit_ids = {str(a.id) for a in dept_audits}
        dept_issues = [i for i in all_issues if str(i.audit_id) in audit_ids]

        passed_audits = [a for a in dept_audits if str(a.status).lower() == "passed"]
        compliance_rate = len(passed_audits) / max(len(dept_audits), 1)
        open_issues = [i for i in dept_issues if str(i.status).lower() in ("open", "pending")]

        compliance_score = max(
            (compliance_rate * 100) - (len(open_issues) * 3), 0.0
        )

        result = {
            "department_id": str(department_id),
            "compliance_score": round(compliance_score, 2),
            "total_audits": len(dept_audits),
            "passed_audits": len(passed_audits),
            "open_issues": len(open_issues),
            "alert_triggered": False,
            "ai_explanation": None,
        }

        if compliance_score < COMPLIANCE_ALERT_THRESHOLD:
            ai_result = await self._trigger_anomaly_agent(
                department_id=department_id,
                compliance_score=compliance_score,
                open_issues_count=len(open_issues),
                failed_audits_count=len(dept_audits) - len(passed_audits),
            )
            result["alert_triggered"] = True
            result["ai_explanation"] = ai_result.get("structured_output", {})

            # Persist notification
            notif_svc = NotificationService()
            await notif_svc.create_system_notification(
                db=db,
                title="⚠️ Compliance Alert",
                message=(
                    f"Department compliance score dropped to {compliance_score:.1f}. "
                    f"AI analysis: {ai_result.get('structured_output', {}).get('anomalies', [])}"
                ),
            )

        return result

    async def _trigger_anomaly_agent(
        self,
        department_id: uuid.UUID,
        compliance_score: float,
        open_issues_count: int,
        failed_audits_count: int,
    ) -> dict:
        """Internal: call LangGraph Anomaly Agent for explanation."""
        from ai.orchestrator import app_graph

        initial_state = {
            "messages": [],
            "context": {
                "task_type": "detect-anomaly",
                "historical_data": [
                    {"period": "previous", "compliance_score": 85.0},
                    {"period": "3_months_ago", "compliance_score": 88.0},
                ],
                "current_data": {
                    "department_id": str(department_id),
                    "compliance_score": compliance_score,
                    "open_issues": open_issues_count,
                    "failed_audits": failed_audits_count,
                },
            },
            "retry_count": 0,
        }
        return await app_graph.ainvoke(initial_state)

    # ------------------------------------------------------------------
    # Approval Workflows
    # ------------------------------------------------------------------
    async def approve_csr_activity(
        self,
        db: AsyncSession,
        activity_id: uuid.UUID,
        approver_id: uuid.UUID,
    ) -> dict:
        """
        Approve a CSR Activity submission.
        Status changes: pending -> approved
        Triggers badge evaluation after approval.
        """
        from repositories.csr_activity import csr_activity_repo
        from repositories.employee_participation import employee_participation_repo
        from services.domain.gamification import gamification_service

        activity = await csr_activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundException(f"CSR Activity {activity_id} not found")

        if str(activity.status).lower() == "approved":
            raise BadRequestException("Activity is already approved")

        updated = await csr_activity_repo.update(db, activity, {
            "status": "approved",
            "updated_by": approver_id,
        })

        # Get all participants and award badges
        participations = await employee_participation_repo.get_all(db, skip=0, limit=1000)
        activity_participants = [p for p in participations if str(p.activity_id) == str(activity_id)]

        awarded_summary = []
        for participation in activity_participants:
            badges = await gamification_service.evaluate_and_award_badges(db, participation.user_id)
            if badges:
                awarded_summary.extend(badges)

        return {
            "activity_id": str(activity_id),
            "status": "approved",
            "approved_by": str(approver_id),
            "badges_awarded": awarded_summary,
        }

    async def reject_csr_activity(
        self,
        db: AsyncSession,
        activity_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        reason: str,
    ) -> dict:
        from repositories.csr_activity import csr_activity_repo

        activity = await csr_activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundException(f"CSR Activity {activity_id} not found")

        await csr_activity_repo.update(db, activity, {
            "status": "rejected",
            "updated_by": reviewer_id,
        })

        return {"activity_id": str(activity_id), "status": "rejected", "reason": reason}

    # ------------------------------------------------------------------
    # Policy Acknowledgement Tracking
    # ------------------------------------------------------------------
    async def acknowledge_policy(
        self,
        db: AsyncSession,
        policy_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> dict:
        from repositories.policy import policy_repo
        from repositories.policy_acknowledgement import policy_acknowledgement_repo

        policy = await policy_repo.get_by_id(db, policy_id)
        if not policy:
            raise NotFoundException(f"Policy {policy_id} not found")

        # Idempotency check
        existing = await policy_acknowledgement_repo.get_all(db, skip=0, limit=10000)
        already_acked = any(
            str(a.policy_id) == str(policy_id) and str(a.user_id) == str(user_id)
            for a in existing
        )
        if already_acked:
            return {"acknowledged": True, "policy_id": str(policy_id), "already_existed": True}

        await policy_acknowledgement_repo.create(db, {
            "policy_id": policy_id,
            "user_id": user_id,
            "acknowledged_at": datetime.now(timezone.utc),
            "status": "active",
        })

        return {"acknowledged": True, "policy_id": str(policy_id), "already_existed": False}

    async def get_policy_acknowledgement_rate(
        self,
        db: AsyncSession,
        policy_id: uuid.UUID,
    ) -> dict:
        from repositories.policy_acknowledgement import policy_acknowledgement_repo
        from repositories.user import user_repo

        total_users = len(await user_repo.get_all(db, skip=0, limit=10000))
        acks = await policy_acknowledgement_repo.get_all(db, skip=0, limit=10000)
        policy_acks = [a for a in acks if str(a.policy_id) == str(policy_id)]

        rate = len(policy_acks) / max(total_users, 1)
        return {
            "policy_id": str(policy_id),
            "total_users": total_users,
            "acknowledged_count": len(policy_acks),
            "acknowledgement_rate": round(rate, 4),
        }


governance_service = GovernanceService()
