from fastapi import APIRouter

from app.api.v1.routers.event_router import router as event_router
from app.api.v1.routers.health_router import router as health_router
from app.core.config import settings

api_v1_router = APIRouter(prefix=settings.API_V1_PREFIX, tags=["API v1"])

api_v1_router.include_router(health_router, prefix="/health-check", tags=["Health"])
api_v1_router.include_router(event_router, prefix="/events", tags=["Events"])
