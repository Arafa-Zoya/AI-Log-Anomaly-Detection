from fastapi import APIRouter

from app.api.v1.endpoints import health, predict, train

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(predict.router)
api_router.include_router(train.router)
