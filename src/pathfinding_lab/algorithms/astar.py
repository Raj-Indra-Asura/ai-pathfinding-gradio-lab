"""A* Search algorithm."""

import heapq
import time
from typing import Callable, Dict

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def astar(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float]
) -> SearchResult:
    """
    Perform A* Search to find the optimal path from start to goal.

    A* combines Dijkstra's algorithm with a heuristic. It expands nodes
    based on f(n) = g(n) + h(n), where:
    - g(n) is the cost from start to n
    - h(n) is the estimated cost from n to goal (heuristic)

    With an admissible heuristic, A* guarantees optimal paths.

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
    # Priority queue: (f_cost, g_cost, position)
    # We include g_cost to break ties in favor of nodes closer to start
    h_start = heuristic(start, goal)
    pq = [(h_start, 0.0, start)]

    g_cost: Dict[Position, float] = {start: 0.0}
    parent: Dict[Position, Position] = {}
    visited_order = []
    closed_set = set()

    # A* main loop
    while pq:
        f, current_g, current = heapq.heappop(pq)

        # Skip if already processed
        if current in closed_set:
            continue

        closed_set.add(current)
        visited_order.append(current)

        # Goal check
        if current == goal:
            # Reconstruct path
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            return SearchResult(
                algorithm_name="A* Search",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=g_cost[goal],
                nodes_visited=len(visited_order),
                runtime_ms=runtime_ms,
                message="Optimal path found"
            )

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue

            # Calculate tentative g cost
            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = current_g + move_cost

            # If this path is better, update
            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                h = heuristic(neighbor, goal)
                f_cost = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, tentative_g, neighbor))

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="A* Search",
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
