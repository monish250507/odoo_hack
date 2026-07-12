
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.employee_participation import EmployeeParticipationCreate, EmployeeParticipationUpdate, EmployeeParticipationResponse
from services.employee_participation import EmployeeParticipationService

router = APIRouter(prefix="/employee_participations", tags=["EmployeeParticipations"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[EmployeeParticipationResponse])
async def read_employee_participations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await EmployeeParticipationService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=EmployeeParticipationResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_participation(obj_in: EmployeeParticipationCreate, db: AsyncSession = Depends(get_db)):
    return await EmployeeParticipationService.create(db, obj_in)

@router.get("/{id}", response_model=EmployeeParticipationResponse)
async def read_employee_participation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await EmployeeParticipationService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="EmployeeParticipation not found")
    return item

@router.put("/{id}", response_model=EmployeeParticipationResponse)
async def update_employee_participation(id: uuid.UUID, obj_in: EmployeeParticipationUpdate, db: AsyncSession = Depends(get_db)):
    item = await EmployeeParticipationService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="EmployeeParticipation not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_participation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await EmployeeParticipationService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="EmployeeParticipation not found")