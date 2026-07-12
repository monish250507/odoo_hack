
from models.notification import Notification
from repositories.base import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    pass

notification_repo = NotificationRepository(Notification)