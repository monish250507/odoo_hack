
from models.user_badge import UserBadge
from repositories.base import BaseRepository

class UserBadgeRepository(BaseRepository[UserBadge]):
    pass

user_badge_repo = UserBadgeRepository(UserBadge)