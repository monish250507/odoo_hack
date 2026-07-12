"""
Reporting Router — dashboard, activity feed, and AI executive report generation.
"""
import uuid

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.reporting import reporting_service

router = APIRouter(prefix="/reporting", tags=["Reporting"])


async def get_db():
    async with async_session_maker() as session:
        yield session


class GenerateReportRequest(BaseModel):
    report_type: str = "Quarterly"


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)):
    """Full deterministic organisation-wide ESG dashboard aggregation."""
    return await reporting_service.get_dashboard_data(db)


@router.get("/activity-feed")
async def recent_activity_feed(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Paginated recent activity feed across all ESG modules."""
    return await reporting_service.get_recent_activity_feed(db, limit=limit)


@router.post("/generate-report")
async def generate_executive_report(
    body: GenerateReportRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    AI-powered report generation.
    Aggregates dashboard data → triggers Report Agent → returns executive narrative.
    """
    return await reporting_service.generate_executive_report(db, body.report_type)
