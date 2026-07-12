
from models.department_score import DepartmentScore
from repositories.base import BaseRepository

class DepartmentScoreRepository(BaseRepository[DepartmentScore]):
    pass

department_score_repo = DepartmentScoreRepository(DepartmentScore)