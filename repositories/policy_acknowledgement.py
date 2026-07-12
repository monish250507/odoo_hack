
from models.policy_acknowledgement import PolicyAcknowledgement
from repositories.base import BaseRepository

class PolicyAcknowledgementRepository(BaseRepository[PolicyAcknowledgement]):
    pass

policy_acknowledgement_repo = PolicyAcknowledgementRepository(PolicyAcknowledgement)