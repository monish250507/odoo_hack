from typing import Annotated, TypedDict, Any, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
    Represents the state of our LangGraph orchestration.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Context injected by FastAPI routers
    context: dict[str, Any]
    
    # Routing variable set by the Supervisor
    next_node: Optional[str]
    
    # Structured output from the agent
    structured_output: Optional[dict[str, Any]]
    
    # Metadata for observability and guardrails
    confidence_score: Optional[float]
    token_usage: Optional[dict[str, int]]
    error: Optional[str]
    retry_count: int
