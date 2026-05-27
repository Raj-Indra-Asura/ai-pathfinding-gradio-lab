"""Breadth-First Search algorithm."""

import time
from collections import deque
from typing import Dict

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.result import SearchResult
from src.pathfinding_lab.core.types import Position


def bfs(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """
    Perform Breadth-First Search to find a path from start to goal.

    BFS explores nodes level by level, guaranteeing the shortest path
    in terms of number of steps (unweighted graph).

    Args:
        grid: The grid to search on
        start: Starting position
        goal: Goal position

    Returns:
        SearchResult with path and metrics
    """
    start_time = time.time()

    # Initialize
    queue = deque([start])
    visited = {start}
    parent: Dict[Position, Position] = {}
    visited_order = [start]

    # BFS main loop
    while queue:
        current = queue.popleft()

        # Goal check
        if current == goal:
            # Reconstruct path
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            return SearchResult(
                algorithm_name="Breadth-First Search (BFS)",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=len(path) - 1 if path else 0,
                nodes_visited=len(visited),
                runtime_ms=runtime_ms,
                message="Path found successfully"
            )

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                visited_order.append(neighbor)

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="Breadth-First Search (BFS)",
        success=False,
        visited_order=visited_order,
        nodes_visited=len(visited),
        runtime_ms=runtime_ms,
        message="No path found"
    )


def _reconstruct_path(parent: Dict[Position, Position], start: Position, goal: Position) -> list[Position]:
    """
    Reconstruct path from start to goal using parent pointers.

    Args:
        parent: Dictionary mapping position to its parent
        start: Start position
        goal: Goal position

    Returns:
        List of positions from start to goal
    """
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path
