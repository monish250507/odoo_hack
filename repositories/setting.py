
from models.setting import Setting
from repositories.base import BaseRepository

class SettingRepository(BaseRepository[Setting]):
    pass

setting_repo = SettingRepository(Setting)