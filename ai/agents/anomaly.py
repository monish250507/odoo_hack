from ai.agents.base import BaseAgent
from ai.schemas.anomaly import AnomalyDetectionOutput

SYSTEM_PROMPT = """You are a Data Quality Anomaly Detection AI.
Compare current data points against historical trends to identify outliers.
ALWAYS return the result matching the structured output schema."""

class AnomalyAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, output_schema=AnomalyDetectionOutput)

anomaly_agent = AnomalyAgent()
