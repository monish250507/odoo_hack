import os
from jinja2 import Template

MODULES = [
    {"name": "Department", "plural": "Departments", "lower": "department", "plural_lower": "departments"},
    {"name": "User", "plural": "Users", "lower": "user", "plural_lower": "users"},
    {"name": "Category", "plural": "Categories", "lower": "category", "plural_lower": "categories"},
    {"name": "EmissionFactor", "plural": "EmissionFactors", "lower": "emission_factor", "plural_lower": "emission_factors"},
    {"name": "ProductESGProfile", "plural": "ProductESGProfiles", "lower": "product_esg_profile", "plural_lower": "product_esg_profiles"},
    {"name": "Goal", "plural": "Goals", "lower": "goal", "plural_lower": "goals"},
    {"name": "CarbonTransaction", "plural": "CarbonTransactions", "lower": "carbon_transaction", "plural_lower": "carbon_transactions"},
    {"name": "CSRActivity", "plural": "CSRActivities", "lower": "csr_activity", "plural_lower": "csr_activities"},
    {"name": "EmployeeParticipation", "plural": "EmployeeParticipations", "lower": "employee_participation", "plural_lower": "employee_participations"},
    {"name": "Challenge", "plural": "Challenges", "lower": "challenge", "plural_lower": "challenges"},
    {"name": "ChallengeParticipation", "plural": "ChallengeParticipations", "lower": "challenge_participation", "plural_lower": "challenge_participations"},
    {"name": "Badge", "plural": "Badges", "lower": "badge", "plural_lower": "badges"},
    {"name": "Reward", "plural": "Rewards", "lower": "reward", "plural_lower": "rewards"},
    {"name": "UserBadge", "plural": "UserBadges", "lower": "user_badge", "plural_lower": "user_badges"},
    {"name": "Policy", "plural": "Policies", "lower": "policy", "plural_lower": "policies"},
    {"name": "PolicyAcknowledgement", "plural": "PolicyAcknowledgements", "lower": "policy_acknowledgement", "plural_lower": "policy_acknowledgements"},
    {"name": "Audit", "plural": "Audits", "lower": "audit", "plural_lower": "audits"},
    {"name": "ComplianceIssue", "plural": "ComplianceIssues", "lower": "compliance_issue", "plural_lower": "compliance_issues"},
    {"name": "DepartmentScore", "plural": "DepartmentScores", "lower": "department_score", "plural_lower": "department_scores"},
    {"name": "Notification", "plural": "Notifications", "lower": "notification", "plural_lower": "notifications"},
    {"name": "Setting", "plural": "Settings", "lower": "setting", "plural_lower": "settings"},
]

MODEL_TEMPLATE = Template("""
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from models.base import FullBaseModel

class {{ name }}(FullBaseModel):
    __tablename__ = "{{ plural_lower }}"
    
    # Generic generic fields for demonstration
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
""")

SCHEMA_TEMPLATE = Template("""
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class {{ name }}Base(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class {{ name }}Create({{ name }}Base):
    pass

class {{ name }}Update({{ name }}Base):
    pass

class {{ name }}Response({{ name }}Base):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True
""")

REPO_TEMPLATE = Template("""
from models.{{ lower }} import {{ name }}
from repositories.base import BaseRepository

class {{ name }}Repository(BaseRepository[{{ name }}]):
    pass

{{ lower }}_repo = {{ name }}Repository({{ name }})
""")

SERVICE_TEMPLATE = Template("""
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.{{ lower }} import {{ lower }}_repo
from schemas.{{ lower }} import {{ name }}Create, {{ name }}Update
from models.{{ lower }} import {{ name }}

class {{ name }}Service:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[{{ name }}]:
        return await {{ lower }}_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[{{ name }}]:
        return await {{ lower }}_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: {{ name }}Create) -> {{ name }}:
        return await {{ lower }}_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: {{ name }}Update) -> Optional[{{ name }}]:
        db_obj = await {{ lower }}_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await {{ lower }}_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await {{ lower }}_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await {{ lower }}_repo.delete(db, id)
        return True
""")

ROUTER_TEMPLATE = Template("""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.{{ lower }} import {{ name }}Create, {{ name }}Update, {{ name }}Response
from services.{{ lower }} import {{ name }}Service

router = APIRouter(prefix="/{{ plural_lower }}", tags=["{{ plural }}"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[{{ name }}Response])
async def read_{{ plural_lower }}(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await {{ name }}Service.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model={{ name }}Response, status_code=status.HTTP_201_CREATED)
async def create_{{ lower }}(obj_in: {{ name }}Create, db: AsyncSession = Depends(get_db)):
    return await {{ name }}Service.create(db, obj_in)

@router.get("/{id}", response_model={{ name }}Response)
async def read_{{ lower }}(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await {{ name }}Service.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="{{ name }} not found")
    return item

@router.put("/{id}", response_model={{ name }}Response)
async def update_{{ lower }}(id: uuid.UUID, obj_in: {{ name }}Update, db: AsyncSession = Depends(get_db)):
    item = await {{ name }}Service.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="{{ name }} not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{{ lower }}(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await {{ name }}Service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="{{ name }} not found")
""")

for module in MODULES:
    with open(f"models/{module['lower']}.py", "w") as f:
        f.write(MODEL_TEMPLATE.render(**module))
    with open(f"schemas/{module['lower']}.py", "w") as f:
        f.write(SCHEMA_TEMPLATE.render(**module))
    with open(f"repositories/{module['lower']}.py", "w") as f:
        f.write(REPO_TEMPLATE.render(**module))
    with open(f"services/{module['lower']}.py", "w") as f:
        f.write(SERVICE_TEMPLATE.render(**module))
    with open(f"routers/{module['lower']}.py", "w") as f:
        f.write(ROUTER_TEMPLATE.render(**module))

# Write __init__ files
models_init = "from .base import Base, BaseModel, FullBaseModel\n" + "\n".join([f"from .{m['lower']} import {m['name']}" for m in MODULES])
with open("models/__init__.py", "w") as f:
    f.write(models_init)
    
schemas_init = "\n".join([f"from .{m['lower']} import {m['name']}Create, {m['name']}Update, {m['name']}Response" for m in MODULES])
with open("schemas/__init__.py", "w") as f:
    f.write(schemas_init)

repos_init = "\n".join([f"from .{m['lower']} import {m['lower']}_repo, {m['name']}Repository" for m in MODULES])
with open("repositories/__init__.py", "w") as f:
    f.write(repos_init)

services_init = "\n".join([f"from .{m['lower']} import {m['name']}Service" for m in MODULES])
with open("services/__init__.py", "w") as f:
    f.write(services_init)

routers_init = "\n".join([f"from .{m['lower']} import router as {m['lower']}_router" for m in MODULES])
with open("routers/__init__.py", "w") as f:
    f.write(routers_init)

# Write main API router
api_router = "from fastapi import APIRouter\n" + "\n".join([f"from routers.{m['lower']} import router as {m['lower']}_router" for m in MODULES])
api_router += "\n\napi_router = APIRouter()\n"
for m in MODULES:
    api_router += f"api_router.include_router({m['lower']}_router)\n"

with open("api/routers.py", "w") as f:
    f.write(api_router)
    
print("Successfully generated all modules!")
