
from models.csr_activity import CSRActivity
from repositories.base import BaseRepository

class CSRActivityRepository(BaseRepository[CSRActivity]):
    pass

csr_activity_repo = CSRActivityRepository(CSRActivity)