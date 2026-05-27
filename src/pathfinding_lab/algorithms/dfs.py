"""Depth-First Search algorithm."""

import time
from typing import Dict, Set

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.result import SearchResult
from src.pathfinding_lab.core.types import Position


def dfs(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """
    Perform Depth-First Search to find a path from start to goal.

    DFS explores as far as possible along each branch before backtracking.
    It does NOT guarantee the shortest path.

    Args:
        grid: The grid to search on
        start: Starting position
        goal: Goal position

    Returns:
        SearchResult with path and metrics
    """
    start_time = time.time()

    # Initialize
    stack = [start]
    visited: Set[Position] = set()
    parent: Dict[Position, Position] = {}
    visited_order = []

    # DFS main loop
    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        # Goal check
        if current == goal:
            # Reconstruct path
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            return SearchResult(
                algorithm_name="Depth-First Search (DFS)",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=len(path) - 1 if path else 0,
                nodes_visited=len(visited),
                runtime_ms=runtime_ms,
                message="Path found (not guaranteed to be shortest)"
            )

        # Explore neighbors (reversed to maintain left-to-right priority)
        neighbors = grid.get_neighbors(current)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                stack.append(neighbor)

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="Depth-First Search (DFS)",
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
