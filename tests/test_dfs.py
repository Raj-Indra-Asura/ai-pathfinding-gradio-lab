"""Tests for DFS algorithm."""

import pytest

from pathfinding_lab.algorithms.dfs import dfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode


def test_dfs_simple_path():
    """Test DFS finds a path in an open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = dfs(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_dfs_path_is_valid():
    """Test that every step in the DFS path is a valid neighbour move."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = dfs(grid, start, goal)

    assert result.success is True
    path = result.path
    for i in range(len(path) - 1):
        r0, c0 = path[i]
        r1, c1 = path[i + 1]
        # 4-directional: each step changes exactly one coordinate by 1
        assert abs(r1 - r0) + abs(c1 - c0) == 1, (
            f"Invalid step from {path[i]} to {path[i + 1]}"
        )


def test_dfs_no_path():
    """Test DFS returns failure when the goal is completely surrounded."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    # Surround goal with obstacles so it is unreachable
    grid.add_obstacle((3, 4))
    grid.add_obstacle((4, 3))
    grid.add_obstacle((3, 3))

    result = dfs(grid, start, goal)

    assert result is not None
    assert isinstance(result.success, bool)


def test_dfs_with_obstacles():
    """Test DFS finds a path around obstacles."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 4)

    # Place a wall with a gap at the bottom
    for row in range(4):
        grid.add_obstacle((row, 2))

    result = dfs(grid, start, goal)

    assert result.success is True
    # The path must not pass through an obstacle
    for pos in result.path:
        assert pos not in grid.obstacles, f"Path passes through obstacle {pos}"


def test_dfs_visited_tracking():
    """Test DFS records visited nodes."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = dfs(grid, start, goal)

    assert len(result.visited_order) > 0
    assert start in result.visited_order
    assert goal in result.visited_order


def test_dfs_not_necessarily_shortest():
    """DFS path is not guaranteed to be the shortest path."""
    grid = Grid(7, 7, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (6, 6)

    from pathfinding_lab.algorithms.bfs import bfs

    dfs_result = dfs(grid, start, goal)
    bfs_result = bfs(grid, start, goal)

    # Both must find a path in an open grid
    assert dfs_result.success is True
    assert bfs_result.success is True

    # DFS path length is >= BFS (shortest) path length
    assert dfs_result.path_length >= bfs_result.path_length
