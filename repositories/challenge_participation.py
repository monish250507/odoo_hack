
from models.challenge_participation import ChallengeParticipation
from repositories.base import BaseRepository

class ChallengeParticipationRepository(BaseRepository[ChallengeParticipation]):
    pass

challenge_participation_repo = ChallengeParticipationRepository(ChallengeParticipation)