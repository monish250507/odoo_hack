import json
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
