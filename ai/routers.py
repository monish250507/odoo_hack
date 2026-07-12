from fastapi import APIRouter, HTTPException
from ai.schemas import (
    CarbonEstimationInput, CarbonEstimationOutput,
    ReportNarratorInput, ReportNarratorOutput,
    AnomalyDetectionInput, AnomalyDetectionOutput,
    ChallengeRecommendationInput, ChallengeRecommendationOutput
)
from ai.orchestrator import app_graph

ai_router = APIRouter(prefix="/ai", tags=["AI Subsystem"])

async def execute_graph(task_type: str, input_data: dict) -> dict:
    initial_state = {
        "messages": [],
        "context": {"task_type": task_type, **input_data},
        "retry_count": 0
    }
    
    result = await app_graph.ainvoke(initial_state)
    
    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result.get("structured_output", {})

@ai_router.post("/estimate-carbon", response_model=CarbonEstimationOutput)
async def estimate_carbon(payload: CarbonEstimationInput):
    return await execute_graph("estimate-carbon", payload.model_dump())

@ai_router.post("/narrate-report", response_model=ReportNarratorOutput)
async def narrate_report(payload: ReportNarratorInput):
    return await execute_graph("narrate-report", payload.model_dump())

@ai_router.post("/detect-anomaly", response_model=AnomalyDetectionOutput)
async def detect_anomaly(payload: AnomalyDetectionInput):
    return await execute_graph("detect-anomaly", payload.model_dump())

@ai_router.post("/recommend-challenge", response_model=ChallengeRecommendationOutput)
async def recommend_challenge(payload: ChallengeRecommendationInput):
    return await execute_graph("recommend-challenge", payload.model_dump())
