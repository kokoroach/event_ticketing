from fastapi import FastAPI
from uvicorn import run

from app.api.routes import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()


api = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)
api.include_router(api_v1_router)


if __name__ == "__main__":
    run(
        api,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
