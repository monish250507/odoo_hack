import os

# Create folders if they don't exist
os.makedirs("ai/schemas", exist_ok=True)
os.makedirs("ai/agents", exist_ok=True)
os.makedirs("ai/utils", exist_ok=True)

# schemas/carbon.py
with open("ai/schemas/carbon.py", "w") as f:
    f.write("""from pydantic import BaseModel, Field
from typing import List

class CarbonEstimationInput(BaseModel):
    activity_data: dict = Field(description="Dictionary of activities like {'electricity_kwh': 1500, 'flights_km': 3000}")
    industry: str = Field(description="The industry of the company")

class CarbonEstimationOutput(BaseModel):
    total_emissions_kg_co2e: float = Field(description="Total estimated emissions in kg CO2e")
    breakdown: dict = Field(description="Emissions broken down by source")
    confidence_score: float = Field(description="Confidence in the estimation (0.0 to 1.0)", ge=0.0, le=1.0)
    recommendations: List[str] = Field(description="Actionable recommendations to reduce emissions")
""")

# schemas/narrator.py
with open("ai/schemas/narrator.py", "w") as f:
    f.write("""from pydantic import BaseModel, Field

class ReportNarratorInput(BaseModel):
    data_metrics: dict = Field(description="Quantitative metrics for the reporting period")
    report_type: str = Field(description="Type of report (e.g., Annual, Quarterly, CSR)")

class ReportNarratorOutput(BaseModel):
    title: str = Field(description="Suggested title for the report")
    executive_summary: str = Field(description="A concise executive summary of the metrics")
    narrative_body: str = Field(description="The detailed narrative explanation of the metrics")
    tone_used: str = Field(description="The tone applied to the narrative (e.g., Professional, Optimistic)")
""")

# schemas/anomaly.py
with open("ai/schemas/anomaly.py", "w") as f:
    f.write("""from pydantic import BaseModel, Field
from typing import List

class AnomalyDetectionInput(BaseModel):
    historical_data: List[dict] = Field(description="Time series historical ESG data")
    current_data: dict = Field(description="Current data point to evaluate")

class AnomalyOutputItem(BaseModel):
    metric_name: str
    expected_range: str
    actual_value: float
    severity: str = Field(description="Low, Medium, High")
    explanation: str

class AnomalyDetectionOutput(BaseModel):
    is_anomalous: bool = Field(description="True if anomalies are detected")
    anomalies: List[AnomalyOutputItem] = Field(default_factory=list)
""")

# schemas/challenge.py
with open("ai/schemas/challenge.py", "w") as f:
    f.write("""from pydantic import BaseModel, Field
from typing import List

class ChallengeRecommendationInput(BaseModel):
    department_goals: dict = Field(description="Current department ESG goals")
    past_participation_rates: dict = Field(description="Past engagement metrics for different challenge types")

class ChallengeIdea(BaseModel):
    title: str
    description: str
    difficulty: str = Field(description="Beginner, Intermediate, Advanced")
    expected_impact: str

class ChallengeRecommendationOutput(BaseModel):
    recommended_challenges: List[ChallengeIdea] = Field(description="List of suggested CSR challenges")
    rationale: str = Field(description="Why these challenges were selected based on the input context")
""")

# schemas/__init__.py
with open("ai/schemas/__init__.py", "w") as f:
    f.write("""from .carbon import CarbonEstimationInput, CarbonEstimationOutput
from .narrator import ReportNarratorInput, ReportNarratorOutput
from .anomaly import AnomalyDetectionInput, AnomalyDetectionOutput
from .challenge import ChallengeRecommendationInput, ChallengeRecommendationOutput
""")

# utils/metrics.py
with open("ai/utils/metrics.py", "w") as f:
    f.write("""from typing import Dict

def calculate_confidence(response_data: dict, schema_type: str) -> float:
    # Dummy implementation for confidence scoring based on completeness
    # In production, this might involve checking certainty markers from the LLM or logprobs
    if "confidence_score" in response_data:
        return float(response_data["confidence_score"])
    return 0.85

def log_token_usage(usage_dict: Dict[str, int], agent_name: str):
    # Log to metrics system (e.g. Datadog, Prometheus)
    print(f"[{agent_name}] Token Usage: {usage_dict}")
""")

# utils/validators.py
with open("ai/utils/validators.py", "w") as f:
    f.write("""def validate_structured_output(data: dict) -> bool:
    # Perform complex semantic validation beyond Pydantic types here
    # e.g., checking if values are within realistic bounds
    if not data:
        return False
    return True
""")

# utils/__init__.py
with open("ai/utils/__init__.py", "w") as f:
    f.write("")

# agents/base.py
with open("ai/agents/base.py", "w") as f:
    f.write("""import json
from typing import Any, Type
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseAgent:
    def __init__(self, system_prompt: str, output_schema: Type[BaseModel]):
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        # Use GPT-4o or latest available
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2).with_structured_output(self.output_schema)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def invoke(self, input_context: dict) -> BaseModel:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=json.dumps(input_context))
        ]
        response = await self.llm.ainvoke(messages)
        return response
""")

# agents/carbon.py
with open("ai/agents/carbon.py", "w") as f:
    f.write("""from ai.agents.base import BaseAgent
from ai.schemas.carbon import CarbonEstimationOutput

SYSTEM_PROMPT = \"\"\"You are an expert Carbon Accounting AI.
Given activity data and industry context, estimate the total carbon footprint in kg CO2e.
Provide a detailed breakdown and actionable recommendations.
ALWAYS return the result matching the structured output schema.\"\"\"

class CarbonAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=CarbonEstimationOutput)

carbon_agent = CarbonAgent()
""")

# agents/narrator.py
with open("ai/agents/narrator.py", "w") as f:
    f.write("""from ai.agents.base import BaseAgent
from ai.schemas.narrator import ReportNarratorOutput

SYSTEM_PROMPT = \"\"\"You are a professional ESG Report Narrator.
Given quantitative metrics, generate a compelling, professional narrative report.
ALWAYS return the result matching the structured output schema.\"\"\"

class NarratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=ReportNarratorOutput)

narrator_agent = NarratorAgent()
""")

# agents/anomaly.py
with open("ai/agents/anomaly.py", "w") as f:
    f.write("""from ai.agents.base import BaseAgent
from ai.schemas.anomaly import AnomalyDetectionOutput

SYSTEM_PROMPT = \"\"\"You are a Data Quality Anomaly Detection AI.
Compare current data points against historical trends to identify outliers.
ALWAYS return the result matching the structured output schema.\"\"\"

class AnomalyAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=AnomalyDetectionOutput)

anomaly_agent = AnomalyAgent()
""")

# agents/challenge.py
with open("ai/agents/challenge.py", "w") as f:
    f.write("""from ai.agents.base import BaseAgent
from ai.schemas.challenge import ChallengeRecommendationOutput

SYSTEM_PROMPT = \"\"\"You are an Employee Engagement AI.
Given departmental goals and past participation metrics, recommend CSR challenges.
ALWAYS return the result matching the structured output schema.\"\"\"

class ChallengeAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=ChallengeRecommendationOutput)

challenge_agent = ChallengeAgent()
""")

# agents/__init__.py
with open("ai/agents/__init__.py", "w") as f:
    f.write("""from .carbon import carbon_agent
from .narrator import narrator_agent
from .anomaly import anomaly_agent
from .challenge import challenge_agent
""")

# orchestrator.py
with open("ai/orchestrator.py", "w") as f:
    f.write("""import json
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from ai.state import GraphState
from ai.agents import carbon_agent, narrator_agent, anomaly_agent, challenge_agent
from ai.utils.validators import validate_structured_output

def supervisor_node(state: GraphState) -> GraphState:
    context = state.get("context", {})
    task_type = context.get("task_type", "")
    
    routes = {
        "estimate-carbon": "CarbonAgent",
        "narrate-report": "NarratorAgent",
        "detect-anomaly": "AnomalyAgent",
        "recommend-challenge": "ChallengeAgent"
    }
    
    next_node = routes.get(task_type)
    if not next_node:
        return {"error": f"Unknown task_type: {task_type}", "next_node": END}
        
    return {"next_node": next_node}

async def carbon_node(state: GraphState) -> GraphState:
    response = await carbon_agent.invoke(state.get("context", {}))
    return {"structured_output": response.model_dump(), "next_node": "Validator"}

async def narrator_node(state: GraphState) -> GraphState:
    response = await narrator_agent.invoke(state.get("context", {}))
    return {"structured_output": response.model_dump(), "next_node": "Validator"}

async def anomaly_node(state: GraphState) -> GraphState:
    response = await anomaly_agent.invoke(state.get("context", {}))
    return {"structured_output": response.model_dump(), "next_node": "Validator"}

async def challenge_node(state: GraphState) -> GraphState:
    response = await challenge_agent.invoke(state.get("context", {}))
    return {"structured_output": response.model_dump(), "next_node": "Validator"}

def validator_node(state: GraphState) -> GraphState:
    output = state.get("structured_output")
    is_valid = validate_structured_output(output)
    if not is_valid:
        return {"error": "Structured output validation failed", "next_node": END}
    return {"confidence_score": 0.95, "next_node": END}

# Build the Graph
workflow = StateGraph(GraphState)

workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("CarbonAgent", carbon_node)
workflow.add_node("NarratorAgent", narrator_node)
workflow.add_node("AnomalyAgent", anomaly_node)
workflow.add_node("ChallengeAgent", challenge_node)
workflow.add_node("Validator", validator_node)

workflow.set_entry_point("Supervisor")

# Add conditional edges from Supervisor
workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x.get("next_node", END),
    {
        "CarbonAgent": "CarbonAgent",
        "NarratorAgent": "NarratorAgent",
        "AnomalyAgent": "AnomalyAgent",
        "ChallengeAgent": "ChallengeAgent",
        END: END
    }
)

workflow.add_edge("CarbonAgent", "Validator")
workflow.add_edge("NarratorAgent", "Validator")
workflow.add_edge("AnomalyAgent", "Validator")
workflow.add_edge("ChallengeAgent", "Validator")

workflow.add_edge("Validator", END)

app_graph = workflow.compile()
""")

# routers.py
with open("ai/routers.py", "w") as f:
    f.write("""from fastapi import APIRouter, HTTPException
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
""")

print("Successfully generated all AI Subsystem files!")
