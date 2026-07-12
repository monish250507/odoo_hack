
from models.policy import Policy
from repositories.base import BaseRepository

class PolicyRepository(BaseRepository[Policy]):
    pass

policy_repo = PolicyRepository(Policy)