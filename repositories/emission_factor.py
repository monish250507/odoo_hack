
from models.emission_factor import EmissionFactor
from repositories.base import BaseRepository

class EmissionFactorRepository(BaseRepository[EmissionFactor]):
    pass

emission_factor_repo = EmissionFactorRepository(EmissionFactor)