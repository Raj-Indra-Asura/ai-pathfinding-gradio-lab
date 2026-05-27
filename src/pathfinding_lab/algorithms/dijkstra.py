"""Dijkstra's algorithm."""

import heapq
import time
from typing import Dict

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def dijkstra(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """
    Perform Dijkstra's algorithm to find the shortest path from start to goal.

    Dijkstra's algorithm finds the shortest path considering edge weights.
    It explores nodes in order of increasing cost from the start.

    Args:
        grid: The grid to search on
        start: Starting position
        goal: Goal position

    Returns:
        SearchResult with path and metrics
    """
    start_time = time.time()

    # Initialize
    # Priority queue: (cost, position)
    pq = [(0.0, start)]
    cost_so_far: Dict[Position, float] = {start: 0.0}
    parent: Dict[Position, Position] = {}
    visited_order = []

    # Dijkstra main loop
    while pq:
        current_cost, current = heapq.heappop(pq)

        # Skip if we've already processed this node with a better cost
        if current_cost > cost_so_far.get(current, float('inf')):
            continue

        visited_order.append(current)

        # Goal check
        if current == goal:
            # Reconstruct path
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            return SearchResult(
                algorithm_name="Dijkstra's Algorithm",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=cost_so_far[goal],
                nodes_visited=len(visited_order),
                runtime_ms=runtime_ms,
                message="Optimal path found"
            )

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            # Calculate new cost
            move_cost = grid.get_movement_cost(current, neighbor)
            new_cost = current_cost + move_cost

            # If this path is better, update
            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="Dijkstra's Algorithm",
        success=False,
        visited_order=visited_order,
        nodes_visited=len(visited_order),
        runtime_ms=runtime_ms,
        message="No path found"
    )


def _reconstruct_path(parent: Dict[Position, Position], start: Position, goal: Position) -> list[Position]:
    """Reconstruct path from start to goal using parent pointers."""
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path
