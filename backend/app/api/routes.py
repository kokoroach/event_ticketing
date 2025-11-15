from functools import partial

from app.api.v1.routers.event_router import router as event_router
from fastapi import APIRouter


def _api_prefix(version: str, resource: str) -> str:
    return f"/api/{version}/{resource}"


api_v1 = partial(_api_prefix, "v1")

api_v1_router = APIRouter()
api_v1_router.include_router(event_router, prefix=api_v1("events"), tags=["Events"])
