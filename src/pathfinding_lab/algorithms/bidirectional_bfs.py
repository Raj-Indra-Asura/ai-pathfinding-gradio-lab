"""Bidirectional Breadth-First Search algorithm."""

import time
from collections import deque
from typing import Dict, Set

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.result import SearchResult
from src.pathfinding_lab.core.types import Position


def bidirectional_bfs(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """
    Perform Bidirectional BFS to find a path from start to goal.

    Bidirectional BFS searches from both start and goal simultaneously,
    meeting in the middle. This can be faster than regular BFS.

    Args:
        grid: The grid to search on
        start: Starting position
        goal: Goal position

    Returns:
        SearchResult with path and metrics
    """
    start_time = time.time()

    # Initialize forward search (from start)
    queue_forward = deque([start])
    visited_forward: Set[Position] = {start}
    parent_forward: Dict[Position, Position] = {}

    # Initialize backward search (from goal)
    queue_backward = deque([goal])
    visited_backward: Set[Position] = {goal}
    parent_backward: Dict[Position, Position] = {}

    visited_order = [start, goal]
    meeting_point = None

    # Bidirectional BFS main loop
    while queue_forward and queue_backward:
        # Expand forward search
        if queue_forward:
            current_forward = queue_forward.popleft()

            for neighbor in grid.get_neighbors(current_forward):
                if neighbor in visited_forward:
                    continue

                visited_forward.add(neighbor)
                parent_forward[neighbor] = current_forward
                queue_forward.append(neighbor)
                visited_order.append(neighbor)

                # Check if we met the backward search
                if neighbor in visited_backward:
                    meeting_point = neighbor
                    break

            if meeting_point:
                break

        # Expand backward search
        if queue_backward:
            current_backward = queue_backward.popleft()

            for neighbor in grid.get_neighbors(current_backward):
                if neighbor in visited_backward:
                    continue

                visited_backward.add(neighbor)
                parent_backward[neighbor] = current_backward
                queue_backward.append(neighbor)
                visited_order.append(neighbor)

                # Check if we met the forward search
                if neighbor in visited_forward:
                    meeting_point = neighbor
                    break

            if meeting_point:
                break

    # Check if path was found
    if meeting_point:
        # Reconstruct path from both directions
        path = _reconstruct_bidirectional_path(
            parent_forward, parent_backward, start, goal, meeting_point
        )
        runtime_ms = (time.time() - start_time) * 1000

        return SearchResult(
            algorithm_name="Bidirectional BFS",
            success=True,
            path=path,
            visited_order=visited_order,
            path_cost=len(path) - 1 if path else 0,
            nodes_visited=len(visited_forward) + len(visited_backward),
            runtime_ms=runtime_ms,
            message="Path found successfully"
        )

    # No path found
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="Bidirectional BFS",
        success=False,
        visited_order=visited_order,
        nodes_visited=len(visited_forward) + len(visited_backward),
        runtime_ms=runtime_ms,
        message="No path found"
    )


def _reconstruct_bidirectional_path(
    parent_forward: Dict[Position, Position],
    parent_backward: Dict[Position, Position],
    start: Position,
    goal: Position,
    meeting_point: Position
) -> list[Position]:
    """
    Reconstruct path from bidirectional search.

    Args:
        parent_forward: Parent pointers from start
        parent_backward: Parent pointers from goal
        start: Start position
        goal: Goal position
        meeting_point: Position where searches met

    Returns:
        Complete path from start to goal
    """
    # Build path from start to meeting point
    path_forward = []
    current = meeting_point
    while current != start:
        path_forward.append(current)
        current = parent_forward[current]
    path_forward.append(start)
    path_forward.reverse()

    # Build path from meeting point to goal
    path_backward = []
    current = meeting_point
    while current in parent_backward:
        current = parent_backward[current]
        path_backward.append(current)

    # Combine paths
    return path_forward + path_backward
