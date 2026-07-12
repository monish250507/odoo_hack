
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.csr_activity import CSRActivityCreate, CSRActivityUpdate, CSRActivityResponse
from services.csr_activity import CSRActivityService

router = APIRouter(prefix="/csr_activities", tags=["CSRActivities"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[CSRActivityResponse])
async def read_csr_activities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CSRActivityService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=CSRActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_csr_activity(obj_in: CSRActivityCreate, db: AsyncSession = Depends(get_db)):
    return await CSRActivityService.create(db, obj_in)

@router.get("/{id}", response_model=CSRActivityResponse)
async def read_csr_activity(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await CSRActivityService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="CSRActivity not found")
    return item

@router.put("/{id}", response_model=CSRActivityResponse)
async def update_csr_activity(id: uuid.UUID, obj_in: CSRActivityUpdate, db: AsyncSession = Depends(get_db)):
    item = await CSRActivityService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="CSRActivity not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_csr_activity(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await CSRActivityService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="CSRActivity not found")