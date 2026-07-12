from ai.agents.base import BaseAgent
from ai.schemas.carbon import CarbonEstimationOutput

SYSTEM_PROMPT = """You are an expert Carbon Accounting AI.
Given activity data and industry context, estimate the total carbon footprint in kg CO2e.
Provide a detailed breakdown and actionable recommendations.
ALWAYS return the result matching the structured output schema."""

class CarbonAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=CarbonEstimationOutput)

carbon_agent = CarbonAgent()
