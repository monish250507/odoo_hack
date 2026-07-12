
from models.audit import Audit
from repositories.base import BaseRepository

class AuditRepository(BaseRepository[Audit]):
    pass

audit_repo = AuditRepository(Audit)