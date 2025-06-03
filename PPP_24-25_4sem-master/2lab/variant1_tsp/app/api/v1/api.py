from fastapi import APIRouter
from app.api.v1.endpoints import tsp

api_router = APIRouter()

# Подключаем роутер для задачи коммивояжера
api_router.include_router(tsp.router, prefix="/tsp", tags=["TSP Solver"])

# В будущем здесь можно будет добавить другие роутеры, например, для аутентификации, если она понадобится
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"]) 