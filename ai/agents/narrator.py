from ai.agents.base import BaseAgent
from ai.schemas.narrator import ReportNarratorOutput

SYSTEM_PROMPT = """You are a professional ESG Report Narrator.
Given quantitative metrics, generate a compelling, professional narrative report.
ALWAYS return the result matching the structured output schema."""

class NarratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=ReportNarratorOutput)

narrator_agent = NarratorAgent()
