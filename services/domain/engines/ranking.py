"""
Department Ranking Engine - deterministic ranking of departments by ESG score.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class DepartmentScoreEntry:
    department_id: str
    department_name: str
    esg_score: float
    previous_score: Optional[float] = None


@dataclass
class RankedDepartment:
    rank: int
    department_id: str
    department_name: str
    esg_score: float
    score_delta: Optional[float]    # change from previous period
    percentile: float               # 0–100


class DepartmentRankingEngine:
    """Ranks departments by ESG score and computes score deltas and percentiles."""

    @staticmethod
    def rank(entries: List[DepartmentScoreEntry]) -> List[RankedDepartment]:
        if not entries:
            return []

        sorted_entries = sorted(entries, key=lambda e: e.esg_score, reverse=True)
        total = len(sorted_entries)

        ranked = []
        for i, entry in enumerate(sorted_entries):
            delta = None
            if entry.previous_score is not None:
                delta = round(entry.esg_score - entry.previous_score, 2)
            percentile = round(((total - i - 1) / max(total - 1, 1)) * 100, 1)

            ranked.append(RankedDepartment(
                rank=i + 1,
                department_id=entry.department_id,
                department_name=entry.department_name,
                esg_score=round(entry.esg_score, 2),
                score_delta=delta,
                percentile=percentile,
            ))

        return ranked
