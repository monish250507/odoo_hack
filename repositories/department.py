
from models.department import Department
from repositories.base import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    pass

department_repo = DepartmentRepository(Department)