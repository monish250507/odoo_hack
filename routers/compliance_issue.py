
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.compliance_issue import ComplianceIssueCreate, ComplianceIssueUpdate, ComplianceIssueResponse
from services.compliance_issue import ComplianceIssueService

router = APIRouter(prefix="/compliance_issues", tags=["ComplianceIssues"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[ComplianceIssueResponse])
async def read_compliance_issues(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ComplianceIssueService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=ComplianceIssueResponse, status_code=status.HTTP_201_CREATED)
async def create_compliance_issue(obj_in: ComplianceIssueCreate, db: AsyncSession = Depends(get_db)):
    return await ComplianceIssueService.create(db, obj_in)

@router.get("/{id}", response_model=ComplianceIssueResponse)
async def read_compliance_issue(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await ComplianceIssueService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="ComplianceIssue not found")
    return item

@router.put("/{id}", response_model=ComplianceIssueResponse)
async def update_compliance_issue(id: uuid.UUID, obj_in: ComplianceIssueUpdate, db: AsyncSession = Depends(get_db)):
    item = await ComplianceIssueService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="ComplianceIssue not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_compliance_issue(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await ComplianceIssueService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ComplianceIssue not found")