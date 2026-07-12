"""
Gamification Router — ESG scoring, goal tracking, rankings, badges, and reward redemption.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.gamification import gamification_service
from services.domain.engines import ESGInputMetrics

router = APIRouter(prefix="/gamification", tags=["Gamification"])


async def get_db():
    async with async_session_maker() as session:
        yield session


class ComputeScoreRequest(BaseModel):
    metrics: ESGInputMetrics
    previous_score: Optional[float] = None


class RedeemRewardRequest(BaseModel):
    user_id: uuid.UUID


@router.post("/departments/{department_id}/score", status_code=status.HTTP_200_OK)
async def compute_department_score(
    department_id: uuid.UUID,
    body: ComputeScoreRequest,
    db: AsyncSession = Depends(get_db),
):
    """Runs the WeightedFormulaEngine and persists the department ESG score."""
    return await gamification_service.compute_department_esg_score(
        db, department_id, body.metrics, body.previous_score
    )


@router.get("/score/overall")
async def overall_esg_score(db: AsyncSession = Depends(get_db)):
    """Organisation-wide ESG score aggregated from all departments."""
    return await gamification_service.compute_overall_esg_score(db)


@router.get("/rankings")
async def department_rankings(db: AsyncSession = Depends(get_db)):
    """Department leaderboard with rank, score delta, and percentile."""
    return await gamification_service.get_department_rankings(db)


@router.post("/goals/{goal_id}/progress", status_code=status.HTTP_200_OK)
async def evaluate_goal_progress(
    goal_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Evaluates goal progress with velocity and ETA. Updates goal status."""
    return await gamification_service.evaluate_goal_progress(db, goal_id)


@router.post("/users/{user_id}/badges/evaluate", status_code=status.HTTP_200_OK)
async def evaluate_badges(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Evaluates all badge criteria and auto-awards qualifying badges."""
    return await gamification_service.evaluate_and_award_badges(db, user_id)


@router.post("/rewards/{reward_id}/redeem", status_code=status.HTTP_200_OK)
async def redeem_reward(
    reward_id: uuid.UUID,
    body: RedeemRewardRequest,
    db: AsyncSession = Depends(get_db),
):
    """Transactional reward redemption — deducts points and decrements stock."""
    return await gamification_service.redeem_reward(db, body.user_id, reward_id)
