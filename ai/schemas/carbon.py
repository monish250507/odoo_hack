from pydantic import BaseModel, Field
from typing import List

class CarbonEstimationInput(BaseModel):
    activity_data: dict = Field(description="Dictionary of activities like {'electricity_kwh': 1500, 'flights_km': 3000}")
    industry: str = Field(description="The industry of the company")

class CarbonEstimationOutput(BaseModel):
    total_emissions_kg_co2e: float = Field(description="Total estimated emissions in kg CO2e")
    breakdown: dict = Field(description="Emissions broken down by source")
    confidence_score: float = Field(description="Confidence in the estimation (0.0 to 1.0)", ge=0.0, le=1.0)
    recommendations: List[str] = Field(description="Actionable recommendations to reduce emissions")
