
from models.product_esg_profile import ProductESGProfile
from repositories.base import BaseRepository

class ProductESGProfileRepository(BaseRepository[ProductESGProfile]):
    pass

product_esg_profile_repo = ProductESGProfileRepository(ProductESGProfile)