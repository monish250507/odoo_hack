from pydantic import BaseModel, Field
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
