import pytest
import uuid
from unittest.mock import AsyncMock, patch
from config.settings import settings
from ai.providers.provider_factory import LLMProviderFactory
from ai.providers.openrouter_provider import OpenRouterLLMProvider
from ai.agents.base import BaseAgent
from ai.agents.carbon import carbon_agent
from ai.agents.narrator import narrator_agent
from ai.agents.anomaly import anomaly_agent
from ai.agents.challenge import challenge_agent
from ai.orchestrator import app_graph
from ai.schemas.carbon import CarbonEstimationOutput
from ai.schemas.narrator import ReportNarratorOutput
from ai.schemas.anomaly import AnomalyDetectionOutput
from ai.schemas.challenge import ChallengeRecommendationOutput

def test_settings_validation():
    # Test valid config
    settings.OPENROUTER_API_KEY = "test-key"
    settings.validate_ai_config() # Should not raise
    
    # Test invalid config
    original_key = settings.OPENROUTER_API_KEY
    settings.OPENROUTER_API_KEY = ""
    with pytest.raises(ValueError):
        settings.validate_ai_config()
    settings.OPENROUTER_API_KEY = original_key

def test_provider_factory():
    LLMProviderFactory._provider = None # Reset cached provider to ensure test isolation
    provider = LLMProviderFactory.get_provider()
    assert isinstance(provider, OpenRouterLLMProvider)
    assert provider.api_key == settings.OPENROUTER_API_KEY
    assert provider.base_url == settings.OPENROUTER_BASE_URL

    # Verify singleton behavior
    provider2 = LLMProviderFactory.get_provider()
    assert provider is provider2

def test_agent_models():
    assert carbon_agent.model_name == settings.CARBON_MODEL
    assert narrator_agent.model_name == settings.REPORT_MODEL
    assert anomaly_agent.model_name == settings.ANOMALY_MODEL
    assert challenge_agent.model_name == settings.RECOMMENDATION_MODEL

@pytest.mark.asyncio
async def test_langgraph_carbon_flow():
    mock_response = CarbonEstimationOutput(
        total_emissions_kg_co2e=1200.5,
        breakdown={"electricity": 800.0, "travel": 400.5},
        confidence_score=0.9,
        recommendations=["Switch to LED", "Reduce air travel"]
    )
    
    with patch.object(carbon_agent, "invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_response
        
        initial_state = {
            "messages": [],
            "context": {
                "task_type": "estimate-carbon",
                "activity_data": {"electricity_kwh": 2000},
                "industry": "technology"
            },
            "retry_count": 0
        }
        
        result = await app_graph.ainvoke(initial_state)
        
        assert "error" not in result or result["error"] is None
        assert result["structured_output"] == mock_response.model_dump()
        assert result["confidence_score"] == 0.95

@pytest.mark.asyncio
async def test_langgraph_narrator_flow():
    mock_response = ReportNarratorOutput(
        title="EcoSphere ESG Report Q2",
        executive_summary="Summary of ESG performance",
        narrative_body="Narrative details...",
        tone_used="Professional"
    )
    with patch.object(narrator_agent, "invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_response
        
        initial_state = {
            "messages": [],
            "context": {
                "task_type": "narrate-report",
                "data_metrics": {"emissions": 1200},
                "report_type": "Quarterly"
            },
            "retry_count": 0
        }
        
        result = await app_graph.ainvoke(initial_state)
        assert result["structured_output"] == mock_response.model_dump()

@pytest.mark.asyncio
async def test_langgraph_anomaly_flow():
    mock_response = AnomalyDetectionOutput(
        is_anomalous=False,
        anomalies=[]
    )
    with patch.object(anomaly_agent, "invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_response
        
        initial_state = {
            "messages": [],
            "context": {
                "task_type": "detect-anomaly",
                "historical_data": [{"compliance": 85.0}],
                "current_data": {"compliance": 84.5}
            },
            "retry_count": 0
        }
        
        result = await app_graph.ainvoke(initial_state)
        assert result["structured_output"] == mock_response.model_dump()

@pytest.mark.asyncio
async def test_langgraph_challenge_flow():
    mock_response = ChallengeRecommendationOutput(
        recommended_challenges=[],
        rationale="Engaging team goals"
    )
    with patch.object(challenge_agent, "invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_response
        
        initial_state = {
            "messages": [],
            "context": {
                "task_type": "recommend-challenge",
                "department_goals": {},
                "past_participation_rates": {}
            },
            "retry_count": 0
        }
        
        result = await app_graph.ainvoke(initial_state)
        assert result["structured_output"] == mock_response.model_dump()
