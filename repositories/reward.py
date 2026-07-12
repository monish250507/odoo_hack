
from models.reward import Reward
from repositories.base import BaseRepository

class RewardRepository(BaseRepository[Reward]):
    pass

reward_repo = RewardRepository(Reward)