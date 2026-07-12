"""
Weighted Formula Engine - computes ESG scores from raw metrics.
Only performs deterministic math. No AI logic here.
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ESGWeights:
    """Configurable weight distribution for ESG pillars. Must sum to 1.0."""
    environmental: float = 0.40
    social: float = 0.35
    governance: float = 0.25

    def validate(self) -> None:
        total = self.environmental + self.social + self.governance
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"ESG weights must sum to 1.0, got {total:.4f}")


@dataclass
class ESGInputMetrics:
    """Raw normalized metrics per pillar (0–100 scale)."""
    # Environmental
    carbon_reduction_pct: float = 0.0       # % reduction vs baseline
    energy_efficiency_pct: float = 0.0      # % renewable usage
    waste_reduction_pct: float = 0.0

    # Social
    csr_hours_per_employee: float = 0.0
    employee_participation_rate: float = 0.0   # 0.0–1.0
    challenge_completion_rate: float = 0.0     # 0.0–1.0

    # Governance
    audit_compliance_rate: float = 0.0         # 0.0–1.0
    policy_acknowledgement_rate: float = 0.0   # 0.0–1.0
    open_compliance_issues: int = 0            # raw count


@dataclass
class PillarScore:
    raw: float
    weighted: float
    breakdown: Dict[str, float]


@dataclass
class ESGScoreResult:
    overall: float
    environmental: PillarScore
    social: PillarScore
    governance: PillarScore
    grade: str          # A+ / A / B / C / D / F
    trend: Optional[str] = None   # "improving" | "declining" | "stable"


class WeightedFormulaEngine:
    """
    Deterministic ESG score calculator.
    Produces an overall score (0–100) and per-pillar breakdown.
    """

    def __init__(self, weights: Optional[ESGWeights] = None):
        self.weights = weights or ESGWeights()
        self.weights.validate()

    # ------------------------------------------------------------------
    # Pillar sub-scorers
    # ------------------------------------------------------------------
    def _environmental_score(self, m: ESGInputMetrics) -> PillarScore:
        breakdown = {
            "carbon_reduction": min(m.carbon_reduction_pct, 100.0) * 0.50,
            "energy_efficiency": min(m.energy_efficiency_pct, 100.0) * 0.30,
            "waste_reduction":   min(m.waste_reduction_pct,  100.0) * 0.20,
        }
        raw = sum(breakdown.values())
        return PillarScore(raw=raw, weighted=raw * self.weights.environmental, breakdown=breakdown)

    def _social_score(self, m: ESGInputMetrics) -> PillarScore:
        # Normalize csr_hours: cap at 40 hrs / employee / year as "perfect"
        csr_normalized = min(m.csr_hours_per_employee / 40.0, 1.0) * 100
        breakdown = {
            "csr_hours":              csr_normalized * 0.40,
            "participation_rate":     min(m.employee_participation_rate * 100, 100) * 0.35,
            "challenge_completion":   min(m.challenge_completion_rate * 100,  100) * 0.25,
        }
        raw = sum(breakdown.values())
        return PillarScore(raw=raw, weighted=raw * self.weights.social, breakdown=breakdown)

    def _governance_score(self, m: ESGInputMetrics) -> PillarScore:
        # Penalise open compliance issues: each issue deducts 2 pts (max 20)
        issue_penalty = min(m.open_compliance_issues * 2, 20)
        breakdown = {
            "audit_compliance":      min(m.audit_compliance_rate * 100, 100) * 0.40,
            "policy_acknowledgement": min(m.policy_acknowledgement_rate * 100, 100) * 0.40,
            "compliance_issue_penalty": -issue_penalty * 0.20,
        }
        raw = max(sum(breakdown.values()), 0.0)
        return PillarScore(raw=raw, weighted=raw * self.weights.governance, breakdown=breakdown)

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 90: return "A+"
        if score >= 80: return "A"
        if score >= 70: return "B"
        if score >= 60: return "C"
        if score >= 50: return "D"
        return "F"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def compute(self, metrics: ESGInputMetrics, previous_score: Optional[float] = None) -> ESGScoreResult:
        env   = self._environmental_score(metrics)
        soc   = self._social_score(metrics)
        gov   = self._governance_score(metrics)
        overall = min(env.weighted + soc.weighted + gov.weighted, 100.0)

        trend = None
        if previous_score is not None:
            if overall > previous_score + 2:
                trend = "improving"
            elif overall < previous_score - 2:
                trend = "declining"
            else:
                trend = "stable"

        return ESGScoreResult(
            overall=round(overall, 2),
            environmental=env,
            social=soc,
            governance=gov,
            grade=self._grade(overall),
            trend=trend,
        )
