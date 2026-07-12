
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from services.department import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[DepartmentResponse])
async def read_departments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await DepartmentService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(obj_in: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    return await DepartmentService.create(db, obj_in)

@router.get("/{id}", response_model=DepartmentResponse)
async def read_department(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await DepartmentService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item

@router.put("/{id}", response_model=DepartmentResponse)
async def update_department(id: uuid.UUID, obj_in: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    item = await DepartmentService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await DepartmentService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")