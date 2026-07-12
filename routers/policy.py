
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse
from services.policy import PolicyService

router = APIRouter(prefix="/policies", tags=["Policies"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[PolicyResponse])
async def read_policies(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await PolicyService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(obj_in: PolicyCreate, db: AsyncSession = Depends(get_db)):
    return await PolicyService.create(db, obj_in)

@router.get("/{id}", response_model=PolicyResponse)
async def read_policy(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await PolicyService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Policy not found")
    return item

@router.put("/{id}", response_model=PolicyResponse)
async def update_policy(id: uuid.UUID, obj_in: PolicyUpdate, db: AsyncSession = Depends(get_db)):
    item = await PolicyService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Policy not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await PolicyService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Policy not found")