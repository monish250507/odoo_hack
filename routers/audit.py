
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.audit import AuditCreate, AuditUpdate, AuditResponse
from services.audit import AuditService

router = APIRouter(prefix="/audits", tags=["Audits"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[AuditResponse])
async def read_audits(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await AuditService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=AuditResponse, status_code=status.HTTP_201_CREATED)
async def create_audit(obj_in: AuditCreate, db: AsyncSession = Depends(get_db)):
    return await AuditService.create(db, obj_in)

@router.get("/{id}", response_model=AuditResponse)
async def read_audit(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await AuditService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Audit not found")
    return item

@router.put("/{id}", response_model=AuditResponse)
async def update_audit(id: uuid.UUID, obj_in: AuditUpdate, db: AsyncSession = Depends(get_db)):
    item = await AuditService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Audit not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audit(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await AuditService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Audit not found")