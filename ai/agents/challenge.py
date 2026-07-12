from ai.agents.base import BaseAgent
from ai.schemas.challenge import ChallengeRecommendationOutput
from config.settings import settings

SYSTEM_PROMPT = """You are an Employee Engagement AI.
Given departmental goals and past participation metrics, recommend CSR challenges.
ALWAYS return the result matching the structured output schema."""

class ChallengeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=SYSTEM_PROMPT,
            output_schema=ChallengeRecommendationOutput,
            model_name=settings.RECOMMENDATION_MODEL
        )

challenge_agent = ChallengeAgent()
