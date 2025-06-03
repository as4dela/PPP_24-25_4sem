from typing import List, Dict, Set, Optional
from app.schemas.tsp import Graph
import collections

def find_hamiltonian_path_wrapper(graph_data: Graph) -> Dict[str, any]:
    """
    Обертка для поиска Гамильтонова пути.
    Принимает данные графа и возвращает путь и его длину (количество узлов).
    """
    nodes_to_visit: List[int] = graph_data.nodes
    raw_edges: List[List[int]] = graph_data.edges

    if not nodes_to_visit:
        return {"path": [], "total_distance": 0.0}

    adj: Dict[int, Set[int]] = collections.defaultdict(set)
    all_graph_nodes: Set[int] = set()

    for u, v in raw_edges:
        adj[u].add(v)
        adj[v].add(u) # Предполагаем неориентированный граф
        all_graph_nodes.add(u)
        all_graph_nodes.add(v)

    # Убедимся, что все nodes_to_visit действительно существуют как узлы в ребрах,
    # или если nodes_to_visit - единственный узел, он считается существующим.
    # Это также проверяет, что nodes_to_visit являются подмножеством узлов, определенных ребрами,
    # если только nodes_to_visit не состоит из одного узла, не имеющего ребер.
    target_node_set = set(nodes_to_visit)
    if not target_node_set.issubset(all_graph_nodes) and len(nodes_to_visit) > 1:
        # Если какой-то из целевых узлов отсутствует в определениях ребер (и их > 1)
        # или если нет ребер вообще, а целевых узлов > 1, то путь невозможен.
        # Если целевой узел один, путь из одного узла всегда возможен.
        pass # Дальнейшая логика поиска пути обработает это

    if len(nodes_to_visit) == 1:
        # Если нужно посетить только один узел, и он существует в графе (проверяется неявно дальше, если он не в adj)
        # или если он просто указан как единственный узел для посещения.
        # Согласно ТЗ total_distance = len(path)
        return {"path": [nodes_to_visit[0]], "total_distance": 1.0}

    path: List[int] = []
    visited_in_path: Set[int] = set()
    # Храним сам путь, найденный функцией
    solution_path: List[List[int]] = [[]] # Используем список для передачи по ссылке и изменения

    def backtrack(current_node: int):
        path.append(current_node)
        visited_in_path.add(current_node)

        if len(path) == len(target_node_set): # Посетили все требуемые узлы
            # Проверяем, что все узлы в path действительно из target_node_set
            if set(path) == target_node_set:
                solution_path[0] = list(path) # Сохраняем копию
                return True # Путь найден
            # Иначе, это не тот путь, который нам нужен (например, если граф больше, чем target_node_set)

        # Перебираем соседей
        # Важно: current_node должен быть в adj, иначе у него нет соседей
        if current_node in adj:
            for neighbor in sorted(list(adj[current_node])): # Сортировка для детерминизма (не обязательно)
                if neighbor in target_node_set and neighbor not in visited_in_path:
                    if backtrack(neighbor):
                        return True # Прекращаем поиск, если путь найден
        
        # Если не удалось найти продолжение пути из current_node
        visited_in_path.remove(current_node)
        path.pop()
        return False

    # Пытаемся начать поиск из каждого узла в nodes_to_visit
    # Убедимся, что начинаем только с тех узлов, которые действительно нужно посетить
    for start_node in sorted(list(target_node_set)): # Сортировка для детерминизма
        # Сброс path и visited_in_path для новой начальной точки
        path.clear()
        visited_in_path.clear()
        solution_path[0] = []
        
        if backtrack(start_node):
            found_path = solution_path[0]
            return {"path": found_path, "total_distance": float(len(found_path))}
    
    return {"path": [], "total_distance": 0.0} # Путь не найден 