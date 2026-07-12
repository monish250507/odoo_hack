
from models.user import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    pass

user_repo = UserRepository(User)