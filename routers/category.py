
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[CategoryResponse])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CategoryService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(obj_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await CategoryService.create(db, obj_in)

@router.get("/{id}", response_model=CategoryResponse)
async def read_category(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await CategoryService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found")
    return item

@router.put("/{id}", response_model=CategoryResponse)
async def update_category(id: uuid.UUID, obj_in: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    item = await CategoryService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await CategoryService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")