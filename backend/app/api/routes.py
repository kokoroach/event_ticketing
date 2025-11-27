from fastapi import APIRouter

from app.api.v1.routers.event_router import router as event_router
from app.api.v1.routers.health_router import router as health_router


api_v1_router = APIRouter(prefix="/api/v1", tags=["API v1"])

api_v1_router.include_router(health_router, prefix="/health-check", tags=["Health"])
api_v1_router.include_router(event_router, prefix="/events", tags=["Events"])
