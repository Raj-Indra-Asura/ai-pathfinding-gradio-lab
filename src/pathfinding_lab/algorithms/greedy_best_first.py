"""Greedy Best-First Search algorithm."""

import heapq
import time
from typing import Callable, Dict

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def greedy_best_first(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float]
) -> SearchResult:
    """
    Perform Greedy Best-First Search to find a path from start to goal.

    Greedy Best-First Search always expands the node that appears closest
    to the goal according to the heuristic. It does NOT guarantee optimal paths.

    Args:
        grid: The grid to search on
        start: Starting position
        goal: Goal position
        heuristic: Heuristic function to estimate distance to goal

    Returns:
        SearchResult with path and metrics
    """
    start_time = time.time()

    # Initialize
    # Priority queue: (h_cost, position)
    h_start = heuristic(start, goal)
    pq = [(h_start, start)]
    visited = set()
    parent: Dict[Position, Position] = {}
    visited_order = []

    # Greedy Best-First main loop
    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        # Goal check
        if current == goal:
            # Reconstruct path
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            # Calculate actual path cost
            path_cost = 0.0
            for i in range(len(path) - 1):
                path_cost += grid.get_movement_cost(path[i], path[i + 1])

            return SearchResult(
                algorithm_name="Greedy Best-First Search",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=path_cost,
                nodes_visited=len(visited),
                runtime_ms=runtime_ms,
                message="Path found (not guaranteed to be optimal)"
            )

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                h_cost = heuristic(neighbor, goal)
                heapq.heappush(pq, (h_cost, neighbor))

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="Greedy Best-First Search",
        success=False,
        visited_order=visited_order,
        nodes_visited=len(visited),
        runtime_ms=runtime_ms,
        message="No path found"
    )


def _reconstruct_path(parent: Dict[Position, Position], start: Position, goal: Position) -> list[Position]:
    """Reconstruct path from start to goal using parent pointers."""
    path = []
    current = goal

    while current != start:
        path.append(current)
        if current not in parent:
            break
        current = parent[current]

    path.append(start)
    path.reverse()
    return path
