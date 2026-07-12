from pydantic import BaseModel, Field

class ReportNarratorInput(BaseModel):
    data_metrics: dict = Field(description="Quantitative metrics for the reporting period")
    report_type: str = Field(description="Type of report (e.g., Annual, Quarterly, CSR)")

class ReportNarratorOutput(BaseModel):
    title: str = Field(description="Suggested title for the report")
    executive_summary: str = Field(description="A concise executive summary of the metrics")
    narrative_body: str = Field(description="The detailed narrative explanation of the metrics")
    tone_used: str = Field(description="The tone applied to the narrative (e.g., Professional, Optimistic)")
