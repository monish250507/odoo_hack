from .environmental import router as environmental_router
from .social import router as social_router
from .governance import router as governance_router
from .gamification import router as gamification_router
from .reporting import router as reporting_router
from .notifications import router as notifications_router

__all__ = [
    "environmental_router",
    "social_router",
    "governance_router",
    "gamification_router",
    "reporting_router",
    "notifications_router",
]
