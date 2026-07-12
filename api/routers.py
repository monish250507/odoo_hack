from fastapi import APIRouter
from routers.department import router as department_router
from routers.user import router as user_router
from routers.category import router as category_router
from routers.emission_factor import router as emission_factor_router
from routers.product_esg_profile import router as product_esg_profile_router
from routers.goal import router as goal_router
from routers.carbon_transaction import router as carbon_transaction_router
from routers.csr_activity import router as csr_activity_router
from routers.employee_participation import router as employee_participation_router
from routers.challenge import router as challenge_router
from routers.challenge_participation import router as challenge_participation_router
from routers.badge import router as badge_router
from routers.reward import router as reward_router
from routers.user_badge import router as user_badge_router
from routers.policy import router as policy_router
from routers.policy_acknowledgement import router as policy_acknowledgement_router
from routers.audit import router as audit_router
from routers.compliance_issue import router as compliance_issue_router
from routers.department_score import router as department_score_router
from routers.notification import router as notification_router
from routers.setting import router as setting_router
from ai.routers import ai_router
from routers.domain import (
    environmental_router,
    social_router,
    governance_router,
    gamification_router,
    reporting_router,
    notifications_router,
)


api_router = APIRouter()
api_router.include_router(department_router)

api_router.include_router(user_router)
api_router.include_router(category_router)
api_router.include_router(emission_factor_router)
api_router.include_router(product_esg_profile_router)
api_router.include_router(goal_router)
api_router.include_router(carbon_transaction_router)
api_router.include_router(csr_activity_router)
api_router.include_router(employee_participation_router)
api_router.include_router(challenge_router)
api_router.include_router(challenge_participation_router)
api_router.include_router(badge_router)
api_router.include_router(reward_router)
api_router.include_router(user_badge_router)
api_router.include_router(policy_router)
api_router.include_router(policy_acknowledgement_router)
api_router.include_router(audit_router)
api_router.include_router(compliance_issue_router)
api_router.include_router(department_score_router)
api_router.include_router(notification_router)
api_router.include_router(setting_router)
api_router.include_router(ai_router)

# ── Domain (Intelligence) Routers ──────────────────────────────────────────
api_router.include_router(environmental_router, prefix="/domain")
api_router.include_router(social_router, prefix="/domain")
api_router.include_router(governance_router, prefix="/domain")
api_router.include_router(gamification_router, prefix="/domain")
api_router.include_router(reporting_router, prefix="/domain")
api_router.include_router(notifications_router, prefix="/domain")
