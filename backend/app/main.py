from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from app.api.routes import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.db.session import init_db

# Setup logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    await init_db()
    yield
    # Shutdown (if needed)


api = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# API Routes
api.include_router(api_v1_router)


if __name__ == "__main__":
    run(
        api,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
