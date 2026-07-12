
from models.carbon_transaction import CarbonTransaction
from repositories.base import BaseRepository

class CarbonTransactionRepository(BaseRepository[CarbonTransaction]):
    pass

carbon_transaction_repo = CarbonTransactionRepository(CarbonTransaction)