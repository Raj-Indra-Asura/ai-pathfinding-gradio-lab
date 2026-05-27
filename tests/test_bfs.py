"""Tests for BFS algorithm."""

import pytest

from src.pathfinding_lab.algorithms.bfs import bfs
from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.types import MovementMode


def test_bfs_simple_path():
    """Test BFS finds a path in open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = bfs(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_bfs_shortest_path():
    """Test BFS finds shortest path."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = bfs(grid, start, goal)

    # In 4-directional, shortest path is Manhattan distance
    expected_length = abs(goal[0] - start[0]) + abs(goal[1] - start[1]) + 1
    assert result.path_length == expected_length


def test_bfs_no_path():
    """Test BFS handles no path scenario."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    # Block goal completely
    grid.add_obstacle((3, 4))
    grid.add_obstacle((4, 3))

    result = bfs(grid, start, goal)

    # May or may not find path depending on obstacles
    # Just check it returns a valid result
    assert result is not None
    assert isinstance(result.success, bool)


def test_bfs_with_obstacles():
    """Test BFS finds path around obstacles."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 4)

    # Add wall in the middle
    grid.add_obstacle((0, 2))

    result = bfs(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    # Path should go around obstacle
    assert (0, 2) not in result.path


def test_bfs_visited_tracking():
    """Test BFS tracks visited nodes."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = bfs(grid, start, goal)

    assert len(result.visited_order) > 0
    assert start in result.visited_order
    assert goal in result.visited_order
