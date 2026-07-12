"""
Regenerates all model files with production-grade schemas
and Python 3.9-compatible typing (Optional instead of X | None).
Run: venv\Scripts\python.exe regenerate_models.py
"""
import os

MODELS = {
    "department": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Department(FullBaseModel):
    __tablename__ = "departments"
    __table_args__ = (
        Index("ix_departments_name", "name"),
        Index("ix_departments_is_deleted", "is_deleted"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
""",

    "user": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class User(FullBaseModel):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_department_id", "department_id"),
        Index("ix_users_is_deleted", "is_deleted"),
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(512), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="employee")  # admin | manager | employee
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    points: Mapped[int] = mapped_column(default=0, server_default="0")
""",

    "category": """from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from models.base import FullBaseModel

class Category(FullBaseModel):
    __tablename__ = "categories"
    __table_args__ = (Index("ix_categories_name", "name"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # emission | activity | csr
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "emission_factor": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class EmissionFactor(FullBaseModel):
    __tablename__ = "emission_factors"
    __table_args__ = (Index("ix_ef_category_id", "category_id"),)

    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    factor_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(100), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "product_esg_profile": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class ProductESGProfile(FullBaseModel):
    __tablename__ = "product_esg_profiles"
    __table_args__ = (Index("ix_pep_department_id", "department_id"),)

    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    carbon_footprint: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    energy_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    water_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "goal": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Goal(FullBaseModel):
    __tablename__ = "goals"
    __table_args__ = (Index("ix_goals_department_id", "department_id"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    unit: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="on_track", server_default="on_track")
""",

    "carbon_transaction": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class CarbonTransaction(FullBaseModel):
    __tablename__ = "carbon_transactions"
    __table_args__ = (
        Index("ix_ct_user_id", "user_id"),
        Index("ix_ct_type", "type"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # credit | debit
    source: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "csr_activity": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class CSRActivity(FullBaseModel):
    __tablename__ = "csr_activities"
    __table_args__ = (Index("ix_csr_department_id", "department_id"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")
""",

    "employee_participation": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class EmployeeParticipation(FullBaseModel):
    __tablename__ = "employee_participations"
    __table_args__ = (
        Index("ix_ep_user_id", "user_id"),
        Index("ix_ep_activity_id", "activity_id"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    activity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    hours: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")
""",

    "challenge": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Challenge(FullBaseModel):
    __tablename__ = "challenges"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    goal: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "challenge_participation": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class ChallengeParticipation(FullBaseModel):
    __tablename__ = "challenge_participations"
    __table_args__ = (
        Index("ix_cp_user_id", "user_id"),
        Index("ix_cp_challenge_id", "challenge_id"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    challenge_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "badge": """from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from models.base import FullBaseModel

class Badge(FullBaseModel):
    __tablename__ = "badges"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    criteria: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "reward": """from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Integer
from models.base import FullBaseModel

class Reward(FullBaseModel):
    __tablename__ = "rewards"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cost: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    stock: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "user_badge": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class UserBadge(FullBaseModel):
    __tablename__ = "user_badges"
    __table_args__ = (Index("ix_ub_user_id", "user_id"),)

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    badge_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    awarded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "policy": """from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from models.base import FullBaseModel

class Policy(FullBaseModel):
    __tablename__ = "policies"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "policy_acknowledgement": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class PolicyAcknowledgement(FullBaseModel):
    __tablename__ = "policy_acknowledgements"
    __table_args__ = (
        Index("ix_pa_user_id", "user_id"),
        Index("ix_pa_policy_id", "policy_id"),
    )

    policy_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "audit": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Audit(FullBaseModel):
    __tablename__ = "audits"
    __table_args__ = (Index("ix_audit_department_id", "department_id"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    auditor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")
""",

    "compliance_issue": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class ComplianceIssue(FullBaseModel):
    __tablename__ = "compliance_issues"
    __table_args__ = (Index("ix_ci_audit_id", "audit_id"),)

    audit_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(50), default="medium")  # low | medium | high | critical
    status: Mapped[str] = mapped_column(String(50), default="open", server_default="open")
""",

    "department_score": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class DepartmentScore(FullBaseModel):
    __tablename__ = "department_scores"
    __table_args__ = (Index("ix_ds_department_period", "department_id", "month", "year"),)

    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "notification": """import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Notification(FullBaseModel):
    __tablename__ = "notifications"
    __table_args__ = (
        Index("ix_notif_user_id", "user_id"),
        Index("ix_notif_is_read", "is_read"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",

    "setting": """from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from models.base import FullBaseModel

class Setting(FullBaseModel):
    __tablename__ = "settings"
    __table_args__ = (Index("ix_settings_key", "key", unique=True),)

    key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
""",
}

# Regenerate all model files
for model_name, content in MODELS.items():
    filepath = f"models/{model_name}.py"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  ✓ {filepath}")

# Regenerate models/__init__.py
module_names = list(MODELS.keys())
class_names = {
    "department": "Department",
    "user": "User",
    "category": "Category",
    "emission_factor": "EmissionFactor",
    "product_esg_profile": "ProductESGProfile",
    "goal": "Goal",
    "carbon_transaction": "CarbonTransaction",
    "csr_activity": "CSRActivity",
    "employee_participation": "EmployeeParticipation",
    "challenge": "Challenge",
    "challenge_participation": "ChallengeParticipation",
    "badge": "Badge",
    "reward": "Reward",
    "user_badge": "UserBadge",
    "policy": "Policy",
    "policy_acknowledgement": "PolicyAcknowledgement",
    "audit": "Audit",
    "compliance_issue": "ComplianceIssue",
    "department_score": "DepartmentScore",
    "notification": "Notification",
    "setting": "Setting",
}

init_content = "from .base import Base, BaseModel, FullBaseModel\n"
for mod, cls in class_names.items():
    init_content += f"from .{mod} import {cls}\n"

with open("models/__init__.py", "w") as f:
    f.write(init_content)
print("  ✓ models/__init__.py")
print("\nAll models regenerated successfully!")
