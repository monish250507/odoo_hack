
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.emission_factor import EmissionFactorCreate, EmissionFactorUpdate, EmissionFactorResponse
from services.emission_factor import EmissionFactorService

router = APIRouter(prefix="/emission_factors", tags=["EmissionFactors"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[EmissionFactorResponse])
async def read_emission_factors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await EmissionFactorService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=EmissionFactorResponse, status_code=status.HTTP_201_CREATED)
async def create_emission_factor(obj_in: EmissionFactorCreate, db: AsyncSession = Depends(get_db)):
    return await EmissionFactorService.create(db, obj_in)

@router.get("/{id}", response_model=EmissionFactorResponse)
async def read_emission_factor(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await EmissionFactorService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")
    return item

@router.put("/{id}", response_model=EmissionFactorResponse)
async def update_emission_factor(id: uuid.UUID, obj_in: EmissionFactorUpdate, db: AsyncSession = Depends(get_db)):
    item = await EmissionFactorService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emission_factor(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await EmissionFactorService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")