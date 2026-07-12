
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.product_esg_profile import ProductESGProfileCreate, ProductESGProfileUpdate, ProductESGProfileResponse
from services.product_esg_profile import ProductESGProfileService

router = APIRouter(prefix="/product_esg_profiles", tags=["ProductESGProfiles"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[ProductESGProfileResponse])
async def read_product_esg_profiles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ProductESGProfileService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=ProductESGProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_product_esg_profile(obj_in: ProductESGProfileCreate, db: AsyncSession = Depends(get_db)):
    return await ProductESGProfileService.create(db, obj_in)

@router.get("/{id}", response_model=ProductESGProfileResponse)
async def read_product_esg_profile(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await ProductESGProfileService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="ProductESGProfile not found")
    return item

@router.put("/{id}", response_model=ProductESGProfileResponse)
async def update_product_esg_profile(id: uuid.UUID, obj_in: ProductESGProfileUpdate, db: AsyncSession = Depends(get_db)):
    item = await ProductESGProfileService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="ProductESGProfile not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_esg_profile(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await ProductESGProfileService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ProductESGProfile not found")