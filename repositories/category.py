
from models.category import Category
from repositories.base import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    pass

category_repo = CategoryRepository(Category)