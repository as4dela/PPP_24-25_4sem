from fastapi import FastAPI

# Импорты для API роутеров
from app.api.v1.api import api_router as api_router_v1

app = FastAPI(
    title="TSP Solver API",
    description="API для решения задачи коммивояжёра.",
    version="0.1.0"
)

# Подключение роутеров API
app.include_router(api_router_v1, prefix="/api/v1")

@app.get("/healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status": "ok"}

# В будущем здесь можно добавить обработчики событий startup/shutdown
# например, для инициализации соединений с БД или их закрытия (хотя Alembic и сессии уже это делают) 