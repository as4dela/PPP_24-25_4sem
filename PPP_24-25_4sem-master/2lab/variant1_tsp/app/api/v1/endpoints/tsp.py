from fastapi import APIRouter, HTTPException
from app.schemas.tsp import ShortestPathRequest, PathResult
from app.services.tsp_solver import find_hamiltonian_path_wrapper

router = APIRouter()

@router.post("/shortest-path/", response_model=PathResult)
async def get_shortest_path(request_data: ShortestPathRequest):
    """
    Принимает описание графа и возвращает путь, проходящий через все указанные узлы,
    и его "дистанцию" (количество узлов в пути).

    Согласно ТЗ:
    - Граф должен быть описан в виде схемы Pydantic `Graph`.
    - Ответ должен быть в виде схемы Pydantic `PathResult`.
    - `PathResult.path`: список узлов в найденном пути.
    - `PathResult.total_distance`: длина пути (количество узлов).
    """
    if not request_data.graph or not request_data.graph.nodes:
        # Если список узлов для посещения пуст, возвращаем пустой результат
        # (хотя Pydantic должен был бы уже проверить наличие nodes по схеме Graph,
        # но дополнительная проверка не повредит, особенно если nodes опционален)
        return PathResult(path=[], total_distance=0.0)

    # Логика решения задачи коммивояжера (поиска Гамильтонова пути)
    # В данном случае, мы ищем путь, который проходит через все узлы из graph.nodes
    # ровно по одному разу. "Дистанция" - это количество узлов в пути.
    
    result = find_hamiltonian_path_wrapper(request_data.graph)
    
    if not result["path"]:
        # Можно вернуть ошибку 404, если путь не найден, или пустой результат согласно ТЗ.
        # ТЗ не специфицирует поведение при ненахождении пути, но пример ответа
        # для успешного случая есть. Если следовать логике "total_distance = len(path)",
        # то пустой путь и дистанция 0.0 являются корректным ответом при ненахождении.
        # Однако, если граф невалиден (например, узлы не связаны), это может быть и ошибка.
        # Для простоты, вернем пустой результат, как если бы путь не был найден.
        return PathResult(path=[], total_distance=0.0)
        
    return PathResult(path=result["path"], total_distance=result["total_distance"]) 