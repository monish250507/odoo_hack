
from models.challenge import Challenge
from repositories.base import BaseRepository

class ChallengeRepository(BaseRepository[Challenge]):
    pass

challenge_repo = ChallengeRepository(Challenge)