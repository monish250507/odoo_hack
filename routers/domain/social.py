"""
Social Router — CSR participation, engagement stats, and AI personalisation.
"""
import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.social import social_service

router = APIRouter(prefix="/social", tags=["Social"])


async def get_db():
    async with async_session_maker() as session:
        yield session


class SubmitParticipationRequest(BaseModel):
    user_id: uuid.UUID
    activity_id: uuid.UUID
    hours: float = Field(..., gt=0)


@router.post("/participations", status_code=status.HTTP_201_CREATED)
async def submit_csr_participation(
    body: SubmitParticipationRequest,
    db: AsyncSession = Depends(get_db),
):
    return await social_service.submit_participation(db, body.user_id, body.activity_id, body.hours)


@router.get("/users/{user_id}/engagement")
async def user_engagement_stats(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    return await social_service.get_user_engagement_stats(db, user_id)


@router.get("/departments/{department_id}/metrics")
async def department_social_metrics(
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    return await social_service.get_department_social_metrics(db, department_id)


@router.get("/users/{user_id}/recommendations")
async def personalised_recommendations(
    user_id: uuid.UUID,
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """AI-powered personalised challenge and CSR recommendations."""
    return await social_service.get_personalised_recommendations(db, user_id, department_id)
