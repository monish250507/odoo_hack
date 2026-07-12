
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.policy_acknowledgement import PolicyAcknowledgementCreate, PolicyAcknowledgementUpdate, PolicyAcknowledgementResponse
from services.policy_acknowledgement import PolicyAcknowledgementService

router = APIRouter(prefix="/policy_acknowledgements", tags=["PolicyAcknowledgements"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[PolicyAcknowledgementResponse])
async def read_policy_acknowledgements(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await PolicyAcknowledgementService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=PolicyAcknowledgementResponse, status_code=status.HTTP_201_CREATED)
async def create_policy_acknowledgement(obj_in: PolicyAcknowledgementCreate, db: AsyncSession = Depends(get_db)):
    return await PolicyAcknowledgementService.create(db, obj_in)

@router.get("/{id}", response_model=PolicyAcknowledgementResponse)
async def read_policy_acknowledgement(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await PolicyAcknowledgementService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="PolicyAcknowledgement not found")
    return item

@router.put("/{id}", response_model=PolicyAcknowledgementResponse)
async def update_policy_acknowledgement(id: uuid.UUID, obj_in: PolicyAcknowledgementUpdate, db: AsyncSession = Depends(get_db)):
    item = await PolicyAcknowledgementService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="PolicyAcknowledgement not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy_acknowledgement(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await PolicyAcknowledgementService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="PolicyAcknowledgement not found")