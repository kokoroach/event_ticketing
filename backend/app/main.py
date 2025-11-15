from app.api.routes import api_v1_router
from fastapi import FastAPI
from uvicorn import run

api = FastAPI()

# API Routes
api.include_router(api_v1_router)


if __name__ == "__main__":
    run(api, host="0.0.0.0", port=8000)
