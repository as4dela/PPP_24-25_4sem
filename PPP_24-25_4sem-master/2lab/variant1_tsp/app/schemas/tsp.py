from pydantic import BaseModel
from typing import List, Tuple

class Graph(BaseModel):
    nodes: List[int]
    edges: List[List[int]] # Список ребер, где каждое ребро - это список из двух узлов [u, v]

class ShortestPathRequest(BaseModel):
    graph: Graph

class PathResult(BaseModel):
    path: List[int]
    total_distance: float 