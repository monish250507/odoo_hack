"""
Environmental Router — exposes carbon transaction, footprint, and AI estimation endpoints.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.environmental import environmental_service

router = APIRouter(prefix="/environmental", tags=["Environmental"])


async def get_db():
    async with async_session_maker() as session:
        yield session


# ── Schemas ──────────────────────────────────────────────────────────────────

class LogTransactionRequest(BaseModel):
    user_id: uuid.UUID
    amount: float = Field(..., gt=0)
    type_: str = Field(..., pattern="^(credit|debit)$")
    source: str


class EstimateEmissionsRequest(BaseModel):
    user_id: uuid.UUID
    activity_data: dict
    industry: str
    auto_log: bool = True


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def log_carbon_transaction(
    body: LogTransactionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await environmental_service.log_transaction(
        db, body.user_id, body.amount, body.type_, body.source
    )


@router.get("/departments/{department_id}/footprint")
async def department_footprint(
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    return await environmental_service.get_department_footprint(db, department_id)


@router.post("/estimate-emissions")
async def estimate_emissions_ai(
    body: EstimateEmissionsRequest,
    db: AsyncSession = Depends(get_db),
):
    """AI-powered emission estimation via Carbon Agent."""
    return await environmental_service.estimate_emissions_with_ai(
        db, body.user_id, body.activity_data, body.industry, body.auto_log
    )


@router.get("/emission-factors")
async def list_emission_factors(
    category_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    return await environmental_service.get_emission_factors(db, category_id)
