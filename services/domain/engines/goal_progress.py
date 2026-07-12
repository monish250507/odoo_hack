"""
Goal Progress Engine - deterministic tracking of ESG goal progress.
Computes completion percentage, velocity, and ETA.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class GoalProgressResult:
    goal_id: str
    current_value: float
    target_value: float
    completion_pct: float       # 0–100
    is_complete: bool
    velocity_per_day: float     # average daily progress
    estimated_completion: Optional[date]   # None if unreachable
    status: str                 # on_track | at_risk | off_track | complete


class GoalProgressEngine:
    """
    Tracks deterministic goal progress given raw numeric values and time context.
    """

    @staticmethod
    def compute(
        goal_id: str,
        current_value: float,
        target_value: float,
        start_date: date,
        deadline: date,
        today: Optional[date] = None,
    ) -> GoalProgressResult:
        today = today or date.today()

        # Guard against zero target
        if target_value == 0:
            completion_pct = 100.0 if current_value >= 0 else 0.0
        else:
            completion_pct = min((current_value / target_value) * 100, 100.0)

        is_complete = completion_pct >= 100.0

        # Velocity: units of progress per day since start
        days_elapsed = max((today - start_date).days, 1)
        velocity = current_value / days_elapsed

        # ETA calculation
        remaining = target_value - current_value
        if is_complete:
            estimated_completion = today
        elif velocity > 0:
            days_needed = remaining / velocity
            estimated_completion = today + timedelta(days=days_needed)
        else:
            estimated_completion = None

        # Status determination
        days_total = max((deadline - start_date).days, 1)
        days_left  = (deadline - today).days
        expected_pct = ((days_elapsed / days_total) * 100)

        if is_complete:
            status = "complete"
        elif estimated_completion and estimated_completion <= deadline:
            # ETA is within deadline window
            if completion_pct >= expected_pct - 10:
                status = "on_track"
            else:
                status = "at_risk"
        else:
            if days_left <= 0:
                status = "off_track"
            elif completion_pct < expected_pct - 20:
                status = "off_track"
            else:
                status = "at_risk"

        return GoalProgressResult(
            goal_id=goal_id,
            current_value=round(current_value, 4),
            target_value=round(target_value, 4),
            completion_pct=round(completion_pct, 2),
            is_complete=is_complete,
            velocity_per_day=round(velocity, 4),
            estimated_completion=estimated_completion,
            status=status,
        )
