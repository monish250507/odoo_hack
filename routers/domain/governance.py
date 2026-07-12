"""
Governance Router — compliance monitoring, approval workflows, policy acknowledgements.
"""
import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.governance import governance_service

router = APIRouter(prefix="/governance", tags=["Governance"])


async def get_db():
    async with async_session_maker() as session:
        yield session


class ApproveActivityRequest(BaseModel):
    approver_id: uuid.UUID


class RejectActivityRequest(BaseModel):
    reviewer_id: uuid.UUID
    reason: str = Field(..., min_length=5)


class AcknowledgePolicyRequest(BaseModel):
    user_id: uuid.UUID


@router.get("/departments/{department_id}/compliance")
async def compliance_monitoring(
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Computes compliance score. Triggers AI Anomaly Agent automatically
    if the score drops below threshold.
    """
    return await governance_service.monitor_compliance(db, department_id)


@router.post("/activities/{activity_id}/approve", status_code=status.HTTP_200_OK)
async def approve_csr_activity(
    activity_id: uuid.UUID,
    body: ApproveActivityRequest,
    db: AsyncSession = Depends(get_db),
):
    """Approves a CSR activity and auto-awards eligible badges."""
    return await governance_service.approve_csr_activity(db, activity_id, body.approver_id)


@router.post("/activities/{activity_id}/reject", status_code=status.HTTP_200_OK)
async def reject_csr_activity(
    activity_id: uuid.UUID,
    body: RejectActivityRequest,
    db: AsyncSession = Depends(get_db),
):
    return await governance_service.reject_csr_activity(
        db, activity_id, body.reviewer_id, body.reason
    )


@router.post("/policies/{policy_id}/acknowledge", status_code=status.HTTP_200_OK)
async def acknowledge_policy(
    policy_id: uuid.UUID,
    body: AcknowledgePolicyRequest,
    db: AsyncSession = Depends(get_db),
):
    return await governance_service.acknowledge_policy(db, policy_id, body.user_id)


@router.get("/policies/{policy_id}/acknowledgement-rate")
async def policy_acknowledgement_rate(
    policy_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    return await governance_service.get_policy_acknowledgement_rate(db, policy_id)
