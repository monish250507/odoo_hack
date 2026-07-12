"""
Environmental Domain Service

Backend Responsibilities:
  - Persist carbon transactions
  - Aggregate raw emissions from transactions
  - Compute per-department footprint statistics

AI Integration:
  - Triggers Carbon Agent when unstructured activity data requires
    emission factor matching and qualitative reasoning.
  - Persists AI output as a new CarbonTransaction record.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException


class EnvironmentalService:

    # ------------------------------------------------------------------
    # Carbon Transaction CRUD
    # ------------------------------------------------------------------
    async def log_transaction(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        amount: float,
        type_: str,          # "credit" | "debit"
        source: str,
        notes: Optional[str] = None,
    ) -> dict:
        from repositories.carbon_transaction import carbon_transaction_repo

        txn = await carbon_transaction_repo.create(db, {
            "user_id": user_id,
            "amount": amount,
            "type": type_,
            "source": source,
            "date": datetime.now(timezone.utc),
            "status": "active",
        })
        return {"transaction_id": str(txn.id), "amount": amount, "type": type_}

    # ------------------------------------------------------------------
    # Statistics (deterministic — no AI)
    # ------------------------------------------------------------------
    async def get_department_footprint(
        self,
        db: AsyncSession,
        department_id: uuid.UUID,
    ) -> dict:
        """
        Aggregates all carbon transactions for users in a given department.
        Returns gross emissions, net emissions, and offset credits.
        """
        from repositories.carbon_transaction import carbon_transaction_repo
        from repositories.user import user_repo

        all_users = await user_repo.get_all(db, skip=0, limit=10000)
        dept_user_ids = {str(u.id) for u in all_users if str(u.department_id) == str(department_id)}

        all_txns = await carbon_transaction_repo.get_all(db, skip=0, limit=50000)
        dept_txns = [t for t in all_txns if str(t.user_id) in dept_user_ids]

        gross_emissions = sum(float(t.amount or 0) for t in dept_txns if t.type == "debit")
        credits         = sum(float(t.amount or 0) for t in dept_txns if t.type == "credit")
        net_emissions   = max(gross_emissions - credits, 0.0)

        return {
            "department_id": str(department_id),
            "gross_emissions_kg": round(gross_emissions, 2),
            "carbon_credits_kg": round(credits, 2),
            "net_emissions_kg": round(net_emissions, 2),
            "transaction_count": len(dept_txns),
        }

    # ------------------------------------------------------------------
    # AI-Powered: Estimate from unstructured activity data
    # ------------------------------------------------------------------
    async def estimate_emissions_with_ai(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        activity_data: dict,
        industry: str,
        auto_log: bool = True,
    ) -> dict:
        """
        Triggers the Carbon Agent for emission factor matching and reasoning.
        Optionally logs the AI-estimated amount as a CarbonTransaction.
        """
        from ai.orchestrator import app_graph

        initial_state = {
            "messages": [],
            "context": {
                "task_type": "estimate-carbon",
                "activity_data": activity_data,
                "industry": industry,
            },
            "retry_count": 0,
        }

        result = await app_graph.ainvoke(initial_state)
        ai_output = result.get("structured_output", {})

        if auto_log and ai_output.get("total_emissions_kg_co2e"):
            await self.log_transaction(
                db=db,
                user_id=user_id,
                amount=ai_output["total_emissions_kg_co2e"],
                type_="debit",
                source="ai_estimation",
            )

        return {
            "user_id": str(user_id),
            "ai_estimation": ai_output,
            "logged": auto_log and bool(ai_output.get("total_emissions_kg_co2e")),
            "confidence": result.get("confidence_score"),
        }

    # ------------------------------------------------------------------
    # Emission Factors (CRUD wrapper)
    # ------------------------------------------------------------------
    async def get_emission_factors(self, db: AsyncSession, category_id: Optional[uuid.UUID] = None) -> list:
        from repositories.emission_factor import emission_factor_repo
        factors = await emission_factor_repo.get_all(db, skip=0, limit=1000)
        if category_id:
            factors = [f for f in factors if str(f.category_id) == str(category_id)]
        return [
            {
                "id": str(f.id),
                "name": f.name,
                "factor_value": f.factor_value,
                "unit": f.unit,
                "status": f.status,
            }
            for f in factors
        ]


environmental_service = EnvironmentalService()
