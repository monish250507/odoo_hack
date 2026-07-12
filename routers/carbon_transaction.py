
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.carbon_transaction import CarbonTransactionCreate, CarbonTransactionUpdate, CarbonTransactionResponse
from services.carbon_transaction import CarbonTransactionService

router = APIRouter(prefix="/carbon_transactions", tags=["CarbonTransactions"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[CarbonTransactionResponse])
async def read_carbon_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CarbonTransactionService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=CarbonTransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_carbon_transaction(obj_in: CarbonTransactionCreate, db: AsyncSession = Depends(get_db)):
    return await CarbonTransactionService.create(db, obj_in)

@router.get("/{id}", response_model=CarbonTransactionResponse)
async def read_carbon_transaction(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await CarbonTransactionService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="CarbonTransaction not found")
    return item

@router.put("/{id}", response_model=CarbonTransactionResponse)
async def update_carbon_transaction(id: uuid.UUID, obj_in: CarbonTransactionUpdate, db: AsyncSession = Depends(get_db)):
    item = await CarbonTransactionService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="CarbonTransaction not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_carbon_transaction(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await CarbonTransactionService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="CarbonTransaction not found")