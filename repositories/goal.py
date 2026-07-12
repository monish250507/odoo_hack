
from models.goal import Goal
from repositories.base import BaseRepository

class GoalRepository(BaseRepository[Goal]):
    pass

goal_repo = GoalRepository(Goal)