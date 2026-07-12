from pydantic import BaseModel, Field
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
