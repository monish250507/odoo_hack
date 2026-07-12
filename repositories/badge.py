
from models.badge import Badge
from repositories.base import BaseRepository

class BadgeRepository(BaseRepository[Badge]):
    pass

badge_repo = BadgeRepository(Badge)