
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.department_score import DepartmentScoreCreate, DepartmentScoreUpdate, DepartmentScoreResponse
from services.department_score import DepartmentScoreService

router = APIRouter(prefix="/department_scores", tags=["DepartmentScores"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[DepartmentScoreResponse])
async def read_department_scores(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await DepartmentScoreService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=DepartmentScoreResponse, status_code=status.HTTP_201_CREATED)
async def create_department_score(obj_in: DepartmentScoreCreate, db: AsyncSession = Depends(get_db)):
    return await DepartmentScoreService.create(db, obj_in)

@router.get("/{id}", response_model=DepartmentScoreResponse)
async def read_department_score(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await DepartmentScoreService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="DepartmentScore not found")
    return item

@router.put("/{id}", response_model=DepartmentScoreResponse)
async def update_department_score(id: uuid.UUID, obj_in: DepartmentScoreUpdate, db: AsyncSession = Depends(get_db)):
    item = await DepartmentScoreService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="DepartmentScore not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department_score(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await DepartmentScoreService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="DepartmentScore not found")