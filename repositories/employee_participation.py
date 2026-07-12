
from models.employee_participation import EmployeeParticipation
from repositories.base import BaseRepository

class EmployeeParticipationRepository(BaseRepository[EmployeeParticipation]):
    pass

employee_participation_repo = EmployeeParticipationRepository(EmployeeParticipation)